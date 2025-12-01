import random

from fpdf import FPDF

# Define text excerpts
excerpts = [
    "To be or not to be, that is the question.",
    "All the world's a stage, and all the men and women merely players.",
    "Something is rotten in the state of Denmark.",
    "Brevity is the soul of wit.",
    "What a piece of work is man!",
    "Though this be madness, yet there is method in't.",
    "The lady doth protest too much, methinks.",
    "There are more things in heaven and earth, Horatio, than are dreamt of in your philosophy.",
    "Neither a borrower nor a lender be; for loan oft loses both itself and friend.",
    "This above all: to thine own self be true.",
    "When sorrows come, they come not single spies, but in battalions.",
    "Uneasy lies the head that wears a crown.",
    "Give every man thy ear, but few thy voice.",
    "Delays have dangerous ends.",
    "The better part of valor is discretion.",
    "O brave new world that has such people in't!",
    "What's done cannot be undone.",
    "Parting is such sweet sorrow, that I shall say goodnight till it be morrow.",
    "Love all, trust a few, do wrong to none.",
    "All that glitters is not gold.",
]

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

# Generate 20 pages
for page_num in range(1, 21):
    pdf.add_page()
    pdf.set_xy(10, 10)
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, f"Page {page_num}", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    for _ in range(15):  # Add 15 random excerpts per page
        pdf.multi_cell(0, 10, random.choice(excerpts), align="L")
        pdf.ln(2)

# Save the PDF
output_path = (
    "Projects/python/translate-poppler-qm-files/pdfs_original/random_excerpts4.pdf"
)
pdf.output(output_path)
print(f"PDF saved as {output_path}")
