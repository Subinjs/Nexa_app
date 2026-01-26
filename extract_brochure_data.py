"""
NEXA Brochure Data Extraction Tool
Extracts tables and text from PDF brochures using PaddleOCR and PyMuPDF
"""

import fitz  # PyMuPDF
import pandas as pd
from paddleocr import PaddleOCR
import json
import re
from pathlib import Path

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extract_tables_from_pdf(pdf_path):
    """
    Extract tables from PDF using PyMuPDF's text extraction
    """
    doc = fitz.open(pdf_path)
    all_tables = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract text with layout preservation
        text = page.get_text("text")
        blocks = page.get_text("dict")["blocks"]
        
        print(f"\n--- Page {page_num + 1} ---")
        print(text[:500])  # Preview
        
        all_tables.append({
            'page': page_num + 1,
            'text': text,
            'blocks': blocks
        })
    
    doc.close()
    return all_tables


def extract_with_ocr(pdf_path):
    """
    Extract text using OCR (useful for image-based PDFs)
    """
    doc = fitz.open(pdf_path)
    results = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Convert page to image
        pix = page.get_pixmap(dpi=300)
        img_path = f"temp_page_{page_num}.png"
        pix.save(img_path)
        
        # OCR the image
        ocr_result = ocr.ocr(img_path, cls=True)
        
        # Extract text
        page_text = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result[0]:
                text = line[1][0]
                confidence = line[1][1]
                page_text.append({
                    'text': text,
                    'confidence': confidence
                })
        
        results.append({
            'page': page_num + 1,
            'ocr_data': page_text
        })
        
        # Cleanup temp image
        Path(img_path).unlink(missing_ok=True)
        
        print(f"Page {page_num + 1} OCR complete")
    
    doc.close()
    return results


def parse_engine_specs(text):
    """
    Parse engine specifications from extracted text
    """
    specs = {}
    
    # Extract displacement (cc)
    displacement_match = re.search(r'(\d{4})\s*cc', text, re.IGNORECASE)
    if displacement_match:
        specs['displacement'] = displacement_match.group(1) + 'cc'
    
    # Extract power (PS/bhp)
    power_match = re.search(r'(\d+)\s*PS.*?@\s*(\d+)\s*rpm', text, re.IGNORECASE)
    if power_match:
        specs['power_ps'] = int(power_match.group(1))
        specs['power_rpm'] = int(power_match.group(2))
        specs['power_text'] = f"{power_match.group(1)}PS @ {power_match.group(2)} rpm"
    
    # Extract torque (Nm)
    torque_match = re.search(r'(\d+)\s*Nm.*?@\s*(\d+)', text, re.IGNORECASE)
    if torque_match:
        specs['torque_nm'] = int(torque_match.group(1))
        specs['torque_rpm'] = int(torque_match.group(2))
        specs['torque_text'] = f"{torque_match.group(1)}Nm @ {torque_match.group(2)} rpm"
    
    # Extract mileage
    mileage_match = re.search(r'(\d+\.?\d*)\s*km[/]?(?:pl|kg)', text, re.IGNORECASE)
    if mileage_match:
        specs['mileage'] = mileage_match.group(1)
    
    return specs


def convert_to_json_format(data, model_name):
    """
    Convert extracted data to JSON format matching your app structure
    """
    variants = []
    
    # Example structure - customize based on your brochure layout
    for item in data:
        variant_data = {
            "variant": "VARIANT_NAME",
            "fuel": "MT/AT/CNG",
            "ex_showroom": 0,
            "insurance": 0,
            "road_tax": 0,
            "registration": 1000,
            "fastag": 500,
            "extended_warranty": 0,
            "accessories": 0,
            "nexa_card": 885,
            "onroad": 0
        }
        variants.append(variant_data)
    
    return variants


# Example usage
if __name__ == "__main__":
    # Path to your PDF brochure
    pdf_path = "brochures/your_brochure.pdf"
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        print("\n📝 Instructions:")
        print("1. Create a 'brochures' folder in this directory")
        print("2. Place your PDF brochures there")
        print("3. Update the pdf_path variable")
        exit()
    
    print("🚀 Starting extraction...")
    
    # Method 1: Direct text extraction (faster, works for text-based PDFs)
    print("\n=== Method 1: Direct Text Extraction ===")
    tables = extract_tables_from_pdf(pdf_path)
    
    # Method 2: OCR (slower, works for image-based PDFs)
    # Uncomment if needed:
    # print("\n=== Method 2: OCR Extraction ===")
    # ocr_data = extract_with_ocr(pdf_path)
    
    # Parse specifications
    print("\n=== Parsing Specifications ===")
    for table in tables:
        specs = parse_engine_specs(table['text'])
        if specs:
            print(f"\nPage {table['page']} specs:")
            print(json.dumps(specs, indent=2))
    
    # Save to file
    output_file = "extracted_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Data saved to {output_file}")
    print("\n💡 Next steps:")
    print("1. Review the extracted data")
    print("2. Format it to match your JSON structure")
    print("3. Copy to data/ folder")
