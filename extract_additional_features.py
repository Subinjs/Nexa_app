"""
Extract Additional Features from Brochures
This extracts safety, comfort, and technology features to enhance your feature JSONs
"""

import fitz
import re
import json
from pathlib import Path

def extract_features_from_text(text):
    """Extract safety, comfort and technology features"""
    features = {
        "safety_features": {},
        "comfort_features": {},
        "technology": {},
        "dimensions": {},
        "wheels": {}
    }
    
    # Safety Features
    if re.search(r'6\s*airbags?', text, re.IGNORECASE):
        features["safety_features"]["airbags"] = "6 Airbags"
    elif re.search(r'2\s*airbags?', text, re.IGNORECASE):
        features["safety_features"]["airbags"] = "2 Airbags"
    
    features["safety_features"]["abs"] = bool(re.search(r'\bABS\b', text, re.IGNORECASE))
    features["safety_features"]["esp"] = bool(re.search(r'\b(?:ESP|Electronic Stability)', text, re.IGNORECASE))
    features["safety_features"]["hill_hold"] = bool(re.search(r'Hill(?:\s+Hold|\s+Assist)', text, re.IGNORECASE))
    features["safety_features"]["isofix"] = bool(re.search(r'ISOFIX', text, re.IGNORECASE))
    features["safety_features"]["adas"] = bool(re.search(r'ADAS', text, re.IGNORECASE))
    
    if re.search(r'(?:Rear|Parking)\s+Sensors?', text, re.IGNORECASE):
        features["safety_features"]["parking_sensors"] = "Rear"
    if re.search(r'(?:Front|4)\s+Parking\s+Sensors?', text, re.IGNORECASE):
        features["safety_features"]["parking_sensors"] = "Front & Rear"
    
    if re.search(r'360[°\s]*(?:View|Camera)', text, re.IGNORECASE):
        features["safety_features"]["camera"] = "360 Degree"
    elif re.search(r'Rear[- ]?View\s+Camera', text, re.IGNORECASE):
        features["safety_features"]["camera"] = "Rear View"
    
    # Comfort Features
    features["comfort_features"]["climate_control"] = "Automatic" if re.search(r'Automatic\s+(?:Climate|AC|Air)', text, re.IGNORECASE) else "Manual"
    features["comfort_features"]["push_button_start"] = bool(re.search(r'Push\s+Button\s+Start', text, re.IGNORECASE))
    features["comfort_features"]["cruise_control"] = bool(re.search(r'Cruise\s+Control', text, re.IGNORECASE))
    features["comfort_features"]["head_up_display"] = bool(re.search(r'Head[- ]?Up\s+Display|HUD', text, re.IGNORECASE))
    features["comfort_features"]["auto_headlamps"] = bool(re.search(r'Auto(?:matic)?\s+Headlamps?', text, re.IGNORECASE))
    features["comfort_features"]["sunroof"] = bool(re.search(r'Sunroof', text, re.IGNORECASE))
    features["comfort_features"]["leather_seats"] = bool(re.search(r'Leather\s+(?:Seats?|Upholstery)', text, re.IGNORECASE))
    features["comfort_features"]["ventilated_seats"] = bool(re.search(r'Ventilated\s+Seats?', text, re.IGNORECASE))
    
    # Technology
    screen_match = re.search(r'(\d+(?:\.\d+)?)[- ]?inch.*?(?:Display|Screen|Infotainment)', text, re.IGNORECASE)
    if screen_match:
        features["technology"]["infotainment_screen"] = f"{screen_match.group(1)}-inch Touchscreen"
    
    features["technology"]["android_auto"] = bool(re.search(r'Android\s+Auto', text, re.IGNORECASE))
    features["technology"]["apple_carplay"] = bool(re.search(r'Apple\s+CarPlay', text, re.IGNORECASE))
    
    speaker_match = re.search(r'ARKAMYS|(?:(\d+)[\s-]?Speaker)', text, re.IGNORECASE)
    if speaker_match:
        features["technology"]["speakers"] = speaker_match.group(0)
    
    if re.search(r'Suzuki\s+Connect', text, re.IGNORECASE):
        features["technology"]["connected_features"] = "Suzuki Connect"
    
    features["technology"]["wireless_charging"] = bool(re.search(r'Wireless\s+Charg(?:ing|er)', text, re.IGNORECASE))
    
    # Dimensions
    length_match = re.search(r'Length.*?(\d{4})\s*mm', text, re.IGNORECASE)
    if length_match:
        features["dimensions"]["length"] = f"{length_match.group(1)} mm"
    
    width_match = re.search(r'Width.*?(\d{4})\s*mm', text, re.IGNORECASE)
    if width_match:
        features["dimensions"]["width"] = f"{width_match.group(1)} mm"
    
    height_match = re.search(r'Height.*?(\d{4})\s*mm', text, re.IGNORECASE)
    if height_match:
        features["dimensions"]["height"] = f"{height_match.group(1)} mm"
    
    wheelbase_match = re.search(r'Wheelbase.*?(\d{4})\s*mm', text, re.IGNORECASE)
    if wheelbase_match:
        features["dimensions"]["wheelbase"] = f"{wheelbase_match.group(1)} mm"
    
    boot_match = re.search(r'Boot.*?(\d+)\s*(?:liters?|L)', text, re.IGNORECASE)
    if boot_match:
        features["dimensions"]["boot_space"] = f"{boot_match.group(1)} liters"
    
    # Wheels & Tyres
    wheel_match = re.search(r'(\d+/\d+\s+R\d+)', text)
    if wheel_match:
        features["wheels"]["tyre_size"] = wheel_match.group(1)
    
    rim_match = re.search(r'(\d+)[- ]?inch.*?(?:Alloy|Wheel)', text, re.IGNORECASE)
    if rim_match:
        features["wheels"]["rim_size"] = f"{rim_match.group(1)}-inch Alloy"
    
    # Clean up empty sections
    features = {k: v for k, v in features.items() if v}
    for key in features:
        if isinstance(features[key], dict):
            features[key] = {k: v for k, v in features[key].items() if v}
    
    return features

# Process all brochures
MODELS = {
    "NEXA-Baleno-Brochure.pdf": "Baleno",
    "NEXA-FRONX-Brochure.pdf": "Fronx",
    "NEXA-Grand-Vitara-Brochure.pdf": "Grand Vitara",
    "Nexa-Ignis-Brochure.pdf": "Ignis",
    "NEXA-Invicto-Brochure.pdf": "Invicto",
    "NEXA-Jimny-Brochure.pdf": "Jimny",
    "NEXA-Xl6-Brochure.pdf": "XL6",
    "Ciaz_Brochure.pdf": "Ciaz",
}

if __name__ == "__main__":
    print("Extracting additional features from brochures...\\n")
    
    all_features = {}
    
    for pdf_file, model_name in MODELS.items():
        pdf_path = Path("brochures") / pdf_file
        
        if not pdf_path.exists():
            continue
        
        print(f"Processing {model_name}...")
        
        # Extract text
        doc = fitz.open(str(pdf_path))
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # Extract features
        features = extract_features_from_text(text)
        all_features[model_name] = features
        
        # Display summary
        if features.get("safety_features"):
            print(f"  Safety: {len(features['safety_features'])} features found")
        if features.get("comfort_features"):
            print(f"  Comfort: {len(features['comfort_features'])} features found")
        if features.get("technology"):
            print(f"  Technology: {len(features['technology'])} features found")
        if features.get("dimensions"):
            print(f"  Dimensions: {len(features['dimensions'])} specs found")
    
    # Save combined report
    with open("additional_features.json", 'w', encoding='utf-8') as f:
        json.dump(all_features, f, indent=2, ensure_ascii=False)
    
    print(f"\\n✅ All features saved to additional_features.json")
    print("\\n📋 Review the file and manually add features to your data/*_features.json files")
