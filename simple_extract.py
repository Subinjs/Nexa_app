"""
Simple PDF Text Extractor
Quick script to see what's in your PDF brochure
"""

import fitz  # PyMuPDF
import sys
from pathlib import Path

OUTPUT_DIR = Path("extracted")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf_text(pdf_path):
    """Extract and print all text from PDF"""
    try:
        doc = fitz.open(pdf_path)
        print(f"📄 PDF: {pdf_path}")
        print(f"📊 Total Pages: {len(doc)}\n")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            print(f"\n{'='*60}")
            print(f"PAGE {page_num + 1}")
            print('='*60)
            print(text)
            
            # Also save to file
            with open(OUTPUT_DIR / f"page_{page_num + 1}.txt", 'w', encoding='utf-8') as f:
                f.write(text)
        
        doc.close()
        print(f"\n✅ Text saved to extracted/page_*.txt files")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_extract.py <pdf_file>")
        print("Example: python simple_extract.py brochures/baleno.pdf")
    else:
        extract_pdf_text(sys.argv[1])
