# PDF Translation Tool

## Overview

This tool processes PDF files by extracting text (using OCR as a fallback), translating the text into another language using a MarianMT model from Hugging Face, and recreating the PDF with the original and translated text.

## Features

- Extracts text from PDFs, including images with embedded text (OCR fallback).
- Translates text into a target language using a pre-trained MarianMT model.
- Recreates the PDF with both the original and translated text for side-by-side comparison.
- Skips files that are already translated to avoid redundant processing.
- Supports custom fonts for translated text in the recreated PDF.
- Logs detailed progress and errors for debugging.
- Added a script to generate random sample PDFs and included 5 sample PDFs for demonstration.
- Includes logic to skip already-translated files, enhancing efficiency.

## Requirements

### Python Packages

- `fitz` (PyMuPDF)
- `pytesseract`
- `torch`
- `fpdf`
- `Pillow`
- `transformers`

Install the required packages with:

```bash
pip install pymupdf pytesseract torch fpdf pillow transformers
```

### Additional Requirements

#### Tesseract OCR

This script requires Tesseract OCR to extract text from images in PDF files. Follow the steps below to install and configure Tesseract:

1. **Download and Install Tesseract**

   - For Windows:

     - Download the installer from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
     - Install it to your system (e.g., `C:\Users\user\AppData\Local\Programs\Tesseract-OCR`).

   - For Linux:

     ```bash
     sudo apt update
     sudo apt install tesseract-ocr
     ```

   - For macOS:
     ```bash
     brew install tesseract
     ```

2. **Add Tesseract to PATH** (for Windows):

   - Locate the Tesseract installation directory (e.g., `C:\Users\user\AppData\Local\Programs\Tesseract-OCR`).
   - Add this directory to your system's PATH environment variable:
     - Open "Environment Variables" via the Start menu.
     - Edit the `Path` variable under System Variables.
     - Add the path to your Tesseract installation folder.
     - Save and restart your terminal.

3. **Verify Installation**
   - Open your terminal or command prompt and run:
     ```bash
     tesseract --version
     ```
   - You should see the version information for Tesseract.

**Note**: If Tesseract is not correctly installed or added to PATH, the script will raise an error.

### Fonts

Ensure the required font files (e.g., Alegreya Sans SC) are available in the specified `fonts` directory.

## Folder Structure

```
project-directory/
|— pdfs_original/      # Folder containing input PDF files
|— pdfs_translated/    # Folder where translated PDFs will be saved
|— fonts/             # Folder containing custom fonts
|— translation_log.txt # Log file for processing and error details
```

## Usage

1. Place the PDF files you want to translate in the `pdfs_original/` directory.
2. Run the script:
   ```bash
   python translate_pdf.py
   ```
3. Translated PDFs will be saved in the `pdfs_translated/` directory.

### Generating Sample PDFs

To generate random sample PDFs for testing:

1. Run the sample generation script:
   ```bash
   python generate_samples.py
   ```
2. Sample PDFs will be saved in the `pdfs_samples/` directory.

## Configuration

### Model

The script uses the MarianMT model for translation. By default, it is set to:

```python
model_name = "Helsinki-NLP/opus-mt-tc-big-en-tr"
```

You can change the model to a different one supported by Hugging Face if needed.

### Device

The script automatically detects whether a GPU (CUDA) is available and uses it for processing. If no GPU is available, it defaults to CPU:

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
```

### Font

Specify the font file path for the recreated PDF. Update the font path in the script if using a different font:

```python
font_path = os.path.join(base_dir, "fonts", "alegreya-sans-sc", "AlegreyaSansSC-Regular.ttf")
```

## Added Note

This project was created to help a friend of mine. To avoid copyright issues, class PDFs have been replaced with public domain documents. Dummy PDFs (e.g., "The Declaration of Independence" and "Pride and Prejudice") have been added to showcase the project functionality.

## Limitations

- **Batch Size Management**: If GPU memory is insufficient, the batch size is dynamically reduced, which might slow down processing.
- **OCR Limitations**: OCR accuracy depends on the quality of the images in the PDF.
- **Languages Supported**: Translation is limited to the languages supported by the Hugging Face MarianMT model.

## Logging

The script logs all activities to `translation_log.txt`, including errors and processing times. This helps in debugging and monitoring progress.

## Note on Performance

While the script initially explored GPU-based multiprocessing to enhance performance, it was found that this approach introduced bugs and complexities. Given the current processing speed of around 15 seconds per file, further optimization was deemed unnecessary.

## Future Enhancements

- Support for multiprocessing if needed for very large datasets.
- Enhanced font customization options.
- Improved OCR fallback for better accuracy.

## License

This tool is provided "as-is" without any guarantees. Feel free to modify and distribute as needed.
