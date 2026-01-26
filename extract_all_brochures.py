"""
Extract data from all NEXA brochures and generate feature JSONs
"""

import fitz  # PyMuPDF
import json
import re
from pathlib import Path

def extract_pdf_text(pdf_path):
    """Extract all text from PDF"""
    doc = fitz.open(pdf_path)
    all_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        all_text += page.get_text()
    
    doc.close()
    return all_text

def parse_specifications(text, model_name):
    """Parse specifications from brochure text"""
    
    # Common patterns
    displacement_patterns = [
        r'(\d{4})\s*cc',
        r'(\d\.\d)L',
        r'Displacement.*?(\d{4})',
    ]
    
    power_patterns = [
        r'(\d+)\s*PS.*?@\s*(\d+)\s*rpm',
        r'(\d+)\s*bhp.*?@\s*(\d+)',
        r'Power.*?(\d+).*?(\d+)\s*rpm',
    ]
    
    torque_patterns = [
        r'(\d+)\s*Nm.*?@\s*(\d+)',
        r'Torque.*?(\d+).*?(\d+)',
    ]
    
    mileage_patterns = [
        r'(\d+\.?\d*)\s*km[/\s]*(?:pl|kg)',
        r'Mileage.*?(\d+\.?\d*)',
    ]
    
    # Extract displacement
    displacement = None
    for pattern in displacement_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            displacement = match.group(1)
            break
    
    # Extract power
    power_ps = None
    power_rpm = None
    for pattern in power_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            power_ps = match.group(1)
            power_rpm = match.group(2) if len(match.groups()) > 1 else '6000'
            break
    
    # Extract torque
    torque_nm = None
    torque_rpm = None
    for pattern in torque_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            torque_nm = match.group(1)
            torque_rpm = match.group(2) if len(match.groups()) > 1 else '4400'
            break
    
    # Extract mileage
    mileage = None
    for pattern in mileage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            mileage = match.group(1)
            break
    
    # Build features object
    features = {
        "model_name": model_name,
        "engine": {},
        "transmission": {},
        "mileage": {},
        "fuel_type": "Petrol"
    }
    
    if displacement:
        features["engine"]["displacement"] = f"{displacement}cc"
        features["engine"]["displacement_text"] = f"{float(displacement)/1000:.1f}L Petrol"
    
    if power_ps and power_rpm:
        features["engine"]["power_ps"] = int(power_ps)
        features["engine"]["power_rpm"] = int(power_rpm)
        features["engine"]["power_text"] = f"{power_ps}PS @ {power_rpm} rpm"
    
    if torque_nm and torque_rpm:
        features["engine"]["torque_nm"] = int(torque_nm)
        features["engine"]["torque_rpm"] = int(torque_rpm)
        features["engine"]["torque_text"] = f"{torque_nm}Nm @ {torque_rpm} rpm"
    
    # Detect transmission types
    has_mt = bool(re.search(r'\b(?:5MT|Manual|5-speed manual)\b', text, re.IGNORECASE))
    has_at = bool(re.search(r'\b(?:AT|Automatic|6AT|4AT|AGS|AMT)\b', text, re.IGNORECASE))
    has_cvt = bool(re.search(r'\b(?:CVT|e-CVT)\b', text, re.IGNORECASE))
    
    trans_options = []
    if has_mt:
        trans_options.append("5MT")
    if has_at:
        trans_options.append("AT")
    if has_cvt:
        trans_options.append("CVT")
    
    features["transmission"]["options"] = trans_options
    features["transmission"]["description"] = " / ".join(trans_options) if trans_options else "Manual"
    
    if mileage:
        features["mileage"]["mt"] = f"{mileage} kmpl"
        features["mileage"]["type"] = "ARAI Certified"
    
    # Check for hybrid
    if re.search(r'hybrid', text, re.IGNORECASE):
        features["hybrid"] = {
            "type": "Hybrid System",
            "description": "Extracted from brochure"
        }
    
    # Check for 4WD/AWD
    if re.search(r'(?:4WD|AWD|AllGrip)', text, re.IGNORECASE):
        features["drivetrain"] = {
            "type": "4WD",
            "description": "All Wheel Drive"
        }
    
    return features

# Model mapping
MODELS = {
    "NEXA-Baleno-Brochure.pdf": ("Baleno", "baleno_features.json"),
    "NEXA-FRONX-Brochure.pdf": ("Fronx", "fronx_features.json"),
    "NEXA-Grand-Vitara-Brochure.pdf": ("Grand Vitara", "grand_vitara_features.json"),
    "Nexa-Ignis-Brochure.pdf": ("Ignis", "ignis_features.json"),
    "NEXA-Invicto-Brochure.pdf": ("Invicto", "invicto_features.json"),
    "NEXA-Jimny-Brochure.pdf": ("Jimny", "jimny_features.json"),
    "NEXA-Xl6-Brochure.pdf": ("XL6", "xl6_features.json"),
    "Ciaz_Brochure.pdf": ("Ciaz", "ciaz_features.json"),
}

if __name__ == "__main__":
    brochures_dir = Path("brochures")
    
    print("Starting brochure extraction...\n")
    
    for pdf_file, (model_name, output_file) in MODELS.items():
        pdf_path = brochures_dir / pdf_file
        
        if not pdf_path.exists():
            print(f"SKIP: {pdf_file} not found")
            continue
        
        print(f"Processing {model_name}...")
        
        try:
            # Extract text
            text = extract_pdf_text(str(pdf_path))
            
            # Save raw text for manual review
            text_file = f"extracted_{model_name.lower().replace(' ', '_')}.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Parse specifications
            features = parse_specifications(text, model_name)
            
            # Save to JSON
            output_path = Path("data") / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(features, f, indent=2, ensure_ascii=False)
            
            print(f"  -> Saved to {output_path}")
            print(f"  -> Raw text: {text_file}")
            
            # Show preview
            if features.get("engine"):
                eng = features["engine"]
                print(f"  -> Engine: {eng.get('displacement_text', 'N/A')}")
                print(f"  -> Power: {eng.get('power_text', 'N/A')}")
                print(f"  -> Torque: {eng.get('torque_text', 'N/A')}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
        
        print()
    
    print("Extraction complete!")
    print("\nNext steps:")
    print("1. Review the extracted_*.txt files")
    print("2. Check data/*.json files and update any missing data")
    print("3. Run the app to test!")
