import PyPDF2
import json
import re
from pathlib import Path

# Extract offer data from PDF
pdf = PyPDF2.PdfReader(open('brochures/Copy of S3 Jan\'26 - Offer Summary.pdf', 'rb'))

# Extract all text
all_text = ""
for page in pdf.pages:
    all_text += page.extract_text() + "\n"

print("EXTRACTED TEXT:")
print("="*80)
print(all_text)
print("="*80)

# Try to parse offers structure
offers = {}

# Save raw text for manual inspection (always under extracted/)
OUTPUT_DIR = Path("extracted")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_DIR / 'offer_text.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)

print("\nSaved raw text to extracted/offer_text.txt")
print("Please review the text structure to create proper parsing logic.")
