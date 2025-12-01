import logging
import os
import re
import time
from io import BytesIO

import fitz  # PyMuPDF
import pytesseract
import torch
from fpdf import FPDF
from PIL import Image
from transformers import MarianMTModel, MarianTokenizer

# Set up logging
base_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(base_dir, "translation_log.txt")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
)

# Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")

# Load model and tokenizer
model_name = os.path.join("Helsinki-NLP/opus-mt-tc-big-en-tr")
logging.info(f"Loading model: {model_name}")
model = MarianMTModel.from_pretrained(model_name).to(device)
tokenizer = MarianTokenizer.from_pretrained(model_name)

# Define paths
input_folder = os.path.join(base_dir, "pdfs_original")
output_folder = os.path.join(base_dir, "pdfs_translated")
os.makedirs(output_folder, exist_ok=True)


# Function to extract text from PDF using OCR (fallback for images)
def extract_text_with_ocr(page):
    logging.info("Using OCR for text extraction")
    pix = page.get_pixmap()
    img = Image.open(BytesIO(pix.tobytes()))
    ocr_text = pytesseract.image_to_string(img)
    return ocr_text


# Function to extract text from a PDF per page
def extract_text_from_pdf_per_page(pdf_path):
    logging.info(f"Extracting text from {pdf_path}")
    doc = fitz.open(pdf_path)
    page_texts = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if not text.strip():
            text = extract_text_with_ocr(page)
        page_texts.append(text)
    return page_texts


# Function to split text into sentences properly
def split_text_into_sentences(text):
    # Split on periods, question marks, and exclamation points
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


# Function to translate text in batches
def translate_text(text, initial_batch_size=4):
    sentences = split_text_into_sentences(text)
    translated_texts = []
    logging.info(f"Total sentences to translate: {len(sentences)}")
    batch_size = initial_batch_size

    for i in range(0, len(sentences), batch_size):
        batch = sentences[i : i + batch_size]
        try:
            inputs = tokenizer(
                batch, return_tensors="pt", padding=True, truncation=True
            ).to(device)
            translated_tokens = model.generate(**inputs)
            translated_batch = tokenizer.batch_decode(
                translated_tokens, skip_special_tokens=True
            )
            translated_texts.extend(translated_batch)
        except RuntimeError as e:
            if "out of memory" in str(e):
                logging.warning("Out of memory error detected. Reducing batch size.")
                torch.cuda.empty_cache()
                batch_size = max(1, batch_size // 2)
                continue
            else:
                logging.error(f"Unexpected error during translation: {e}")
                raise e
        except Exception as e:
            logging.error(f"Translation failed for batch {i}: {e}")
            continue
    return "\n".join(translated_texts)


# Function to recreate a PDF with original and translated text
def recreate_pdf(input_pdf_path, translated_pages, output_pdf_path):
    logging.info(f"Recreating PDF for {input_pdf_path}")
    doc = fitz.open(input_pdf_path)
    pdf = FPDF()

    font_path = os.path.join(
        base_dir, "fonts", "alegreya-sans-sc", "AlegreyaSansSC-Regular.ttf"
    )
    pdf.add_font("AlegreyaSansSC", "", font_path, uni=True)
    pdf.set_font("AlegreyaSansSC", size=12)

    for page_num in range(len(doc)):
        # Add original page
        pdf.add_page()
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(BytesIO(pix.tobytes()))
        img_path = os.path.join(base_dir, f"temp_page_{page_num}.png")
        img.save(img_path)
        pdf.image(img_path, x=10, y=10, w=190)
        os.remove(img_path)

        # Add translated page
        pdf.add_page()
        pdf.set_xy(10, 10)
        translated_page_text = (
            translated_pages[page_num] if page_num < len(translated_pages) else ""
        )
        pdf.multi_cell(0, 10, translated_page_text)

    pdf.output(output_pdf_path)
    logging.info(f"PDF saved as {output_pdf_path}")


# Main process for a single PDF file
def process_pdf(pdf_file):
    input_pdf_path = os.path.join(input_folder, pdf_file)
    output_pdf_path = os.path.join(output_folder, f"TR_{pdf_file}")

    logging.info(f"Processing {pdf_file}")
    start_time = time.time()
    try:
        page_texts = extract_text_from_pdf_per_page(input_pdf_path)
        translated_pages = [translate_text(page) for page in page_texts]
        if not any(translated_pages):
            logging.error("Translation resulted in empty text. Skipping PDF creation.")
            return
        recreate_pdf(input_pdf_path, translated_pages, output_pdf_path)
        end_time = time.time()
        logging.info(f"Completed {pdf_file} in {end_time - start_time:.2f} seconds")
    except Exception as e:
        logging.error(f"An error occurred while processing {pdf_file}: {e}")


# Example usage
pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
for pdf_file in pdf_files:
    translated_file_path = os.path.join(output_folder, f"TR_{pdf_file}")
    if os.path.exists(translated_file_path):
        logging.info(
            f"Skipping {pdf_file} as it already exists in the translated folder."
        )
        continue
    process_pdf(pdf_file)
