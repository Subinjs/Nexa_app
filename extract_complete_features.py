"""
Comprehensive Feature Extraction from NEXA Brochures
Extracts complete feature set including variant-specific details
"""

import fitz
import re
import json
from pathlib import Path

def extract_comprehensive_features(text, model_name):
    """Extract all possible features from brochure text"""
    features = {
        "safety_features": {},
        "comfort_features": {},
        "technology": {},
        "dimensions": {},
        "wheels": {},
        "exterior": {},
        "interior": {}
    }
    
    # ============ SAFETY FEATURES ============
    # Airbags
    if re.search(r'7\s*airbags?', text, re.IGNORECASE):
        features["safety_features"]["airbags"] = "7 Airbags"
    elif re.search(r'6\s*airbags?', text, re.IGNORECASE):
        features["safety_features"]["airbags"] = "6 Airbags"
    elif re.search(r'4\s*airbags?', text, re.IGNORECASE):
        features["safety_features"]["airbags"] = "4 Airbags"
    elif re.search(r'2\s*airbags?', text, re.IGNORECASE):
        features["safety_features"]["airbags"] = "2 Airbags"
    
    # Safety systems
    features["safety_features"]["abs"] = bool(re.search(r'\bABS\b', text, re.IGNORECASE))
    features["safety_features"]["ebd"] = bool(re.search(r'\bEBD\b', text, re.IGNORECASE))
    features["safety_features"]["esp"] = bool(re.search(r'\b(?:ESP|Electronic Stability(?:\s+Program)?)\b', text, re.IGNORECASE))
    features["safety_features"]["hill_hold"] = bool(re.search(r'Hill(?:\s+Hold|\s+Assist)', text, re.IGNORECASE))
    features["safety_features"]["hill_descent_control"] = bool(re.search(r'Hill\s+Descent(?:\s+Control)?', text, re.IGNORECASE))
    features["safety_features"]["traction_control"] = bool(re.search(r'Traction\s+Control', text, re.IGNORECASE))
    features["safety_features"]["isofix"] = bool(re.search(r'ISOFIX', text, re.IGNORECASE))
    features["safety_features"]["adas"] = bool(re.search(r'ADAS|Advanced\s+Driver\s+Assistance', text, re.IGNORECASE))
    
    # ADAS details
    if re.search(r'Level\s*2\s+ADAS', text, re.IGNORECASE):
        features["safety_features"]["adas"] = "Level 2 ADAS"
    
    # Cameras & Sensors
    if re.search(r'360[°\s]*(?:View|Camera|Degree)', text, re.IGNORECASE):
        features["safety_features"]["camera"] = "360 Degree"
    elif re.search(r'Panoramic\s+(?:View|Camera)', text, re.IGNORECASE):
        features["safety_features"]["camera"] = "Panoramic View"
    elif re.search(r'Rear[- ]?View\s+Camera', text, re.IGNORECASE):
        features["safety_features"]["camera"] = "Rear View"
    
    if re.search(r'(?:Front\s+(?:and|&)\s+Rear|4)\s+Parking\s+Sensors?', text, re.IGNORECASE):
        features["safety_features"]["parking_sensors"] = "Front & Rear"
    elif re.search(r'Rear\s+Parking\s+Sensors?', text, re.IGNORECASE):
        features["safety_features"]["parking_sensors"] = "Rear"
    
    features["safety_features"]["reverse_parking_sensors"] = bool(re.search(r'Reverse\s+Parking\s+Sensors?', text, re.IGNORECASE))
    features["safety_features"]["seat_belt_reminder"] = bool(re.search(r'Seat\s*Belt\s+(?:Reminder|Warning)', text, re.IGNORECASE))
    features["safety_features"]["impact_sensing"] = bool(re.search(r'Impact\s+Sensing', text, re.IGNORECASE))
    
    # ============ COMFORT FEATURES ============
    # Climate Control
    if re.search(r'(?:3|Three)[- ]?Zone\s+(?:Automatic\s+)?(?:Climate|AC)', text, re.IGNORECASE):
        features["comfort_features"]["climate_control"] = "3-Zone Automatic"
    elif re.search(r'(?:Dual|2)[- ]?Zone\s+(?:Automatic\s+)?(?:Climate|AC)', text, re.IGNORECASE):
        features["comfort_features"]["climate_control"] = "Dual Zone Automatic"
    elif re.search(r'Automatic\s+(?:Climate|AC|Air\s+Conditioning)', text, re.IGNORECASE):
        features["comfort_features"]["climate_control"] = "Automatic"
    else:
        features["comfort_features"]["climate_control"] = "Manual"
    
    # AC Vents
    if re.search(r'Rear\s+AC\s+Vents?', text, re.IGNORECASE):
        features["comfort_features"]["ac_vents"] = "Front & Rear"
    
    # Cruise Control
    if re.search(r'Adaptive\s+Cruise\s+Control', text, re.IGNORECASE):
        features["comfort_features"]["cruise_control"] = "Adaptive"
    elif re.search(r'Cruise\s+Control', text, re.IGNORECASE):
        features["comfort_features"]["cruise_control"] = True
    else:
        features["comfort_features"]["cruise_control"] = False
    
    # Convenience Features
    features["comfort_features"]["keyless_entry"] = bool(re.search(r'Keyless\s+Entry', text, re.IGNORECASE))
    features["comfort_features"]["push_button_start"] = bool(re.search(r'Push\s+Button\s+(?:Start|Engine)', text, re.IGNORECASE))
    features["comfort_features"]["head_up_display"] = bool(re.search(r'Head[- ]?Up\s+Display|HUD', text, re.IGNORECASE))
    features["comfort_features"]["auto_headlamps"] = bool(re.search(r'Auto(?:matic)?\s+Headlamps?', text, re.IGNORECASE))
    
    # Sunroof
    if re.search(r'(?:Electric\s+)?Panoramic\s+Sunroof', text, re.IGNORECASE):
        features["comfort_features"]["sunroof"] = "Electric Panoramic"
    elif re.search(r'Electric\s+Sunroof', text, re.IGNORECASE):
        features["comfort_features"]["sunroof"] = "Electric"
    elif re.search(r'Sunroof', text, re.IGNORECASE):
        features["comfort_features"]["sunroof"] = True
    
    # Seats
    features["comfort_features"]["ventilated_seats"] = bool(re.search(r'Ventilated\s+Seats?', text, re.IGNORECASE))
    features["comfort_features"]["leather_seats"] = bool(re.search(r'(?:Leather|Premium)\s+(?:Seats?|Upholstery)', text, re.IGNORECASE))
    features["comfort_features"]["powered_seats"] = bool(re.search(r'(?:Power|Electric(?:ally)?)\s+Adjustable\s+Seats?', text, re.IGNORECASE))
    
    # Seating config
    if re.search(r'[678][- ]?Seater|[678]\s+Seats?', text, re.IGNORECASE):
        seating_match = re.search(r'([678])[- ]?Seater|([678])\s+Seats?', text, re.IGNORECASE)
        if seating_match:
            num = seating_match.group(1) or seating_match.group(2)
            if re.search(r'Captain\s+Seats?', text, re.IGNORECASE):
                features["comfort_features"]["seating"] = f"{num}-Seater with Captain Seats"
            elif re.search(r'Ottoman', text, re.IGNORECASE):
                features["comfort_features"]["seating"] = f"{num}-Seater with Ottoman Seats"
            else:
                features["comfort_features"]["seating"] = f"{num}-Seater"
    
    # Windows & Steering
    if re.search(r'All\s+(?:4|Four)\s+Power\s+Windows?', text, re.IGNORECASE):
        features["comfort_features"]["power_windows"] = "All 4"
    elif re.search(r'Power\s+Windows?', text, re.IGNORECASE):
        features["comfort_features"]["power_windows"] = True
    
    if re.search(r'Tilt\s+(?:and|&)\s+Telescopic\s+Steering', text, re.IGNORECASE):
        features["comfort_features"]["steering_adjustment"] = "Tilt & Telescopic"
    elif re.search(r'Tilt\s+Steering', text, re.IGNORECASE):
        features["comfort_features"]["steering_adjustment"] = "Tilt"
    
    features["comfort_features"]["powered_tailgate"] = bool(re.search(r'(?:Power|Electric)\s+Tailgate', text, re.IGNORECASE))
    features["comfort_features"]["ambient_lighting"] = bool(re.search(r'Ambient\s+Lighting', text, re.IGNORECASE))
    
    # ============ TECHNOLOGY ============
    # Touchscreen
    touchscreen_match = re.search(r'([\d.]+)[- ]?inch\s+(?:HD\s+)?(?:Touchscreen|Display|Infotainment)', text, re.IGNORECASE)
    if touchscreen_match:
        size = touchscreen_match.group(1)
        if re.search(r'HD', text, re.IGNORECASE):
            features["technology"]["touchscreen"] = f"{size}-inch HD Display"
        else:
            features["technology"]["touchscreen"] = f"{size}-inch"
    
    # SmartPlay variants
    if re.search(r'SmartPlay\s+Pro\+', text, re.IGNORECASE):
        if not features["technology"].get("touchscreen"):
            features["technology"]["touchscreen"] = "9-inch SmartPlay Pro+"
    elif re.search(r'SmartPlay\s+Studio', text, re.IGNORECASE):
        if not features["technology"].get("touchscreen"):
            features["technology"]["touchscreen"] = "7-inch SmartPlay Studio"
    
    # Connectivity
    features["technology"]["android_auto"] = bool(re.search(r'Android\s+Auto', text, re.IGNORECASE))
    features["technology"]["apple_carplay"] = bool(re.search(r'Apple\s+CarPlay', text, re.IGNORECASE))
    features["technology"]["bluetooth"] = bool(re.search(r'Bluetooth', text, re.IGNORECASE))
    features["technology"]["wireless_charger"] = bool(re.search(r'Wireless\s+(?:Charger|Charging)', text, re.IGNORECASE))
    
    # Connected features
    if re.search(r'Suzuki\s+Connect', text, re.IGNORECASE):
        features["technology"]["connected_features"] = "Suzuki Connect"
    elif re.search(r'Connected\s+Car', text, re.IGNORECASE):
        features["technology"]["connected_features"] = True
    
    # Sound System
    if re.search(r'JBL\s+Premium|JBL.*9\s+Speakers?', text, re.IGNORECASE):
        features["technology"]["speakers"] = "JBL Premium (9 Speakers)"
    elif re.search(r'JBL', text, re.IGNORECASE):
        features["technology"]["speakers"] = "JBL"
    elif re.search(r'ARKAMYS\s+Premium', text, re.IGNORECASE):
        features["technology"]["speakers"] = "ARKAMYS Premium"
    elif re.search(r'ARKAMYS', text, re.IGNORECASE):
        features["technology"]["speakers"] = "ARKAMYS"
    
    # Speaker count
    speaker_match = re.search(r'(\d+)\s+Speakers?', text, re.IGNORECASE)
    if speaker_match and not features["technology"].get("speakers"):
        features["technology"]["speakers"] = f"{speaker_match.group(1)} Speakers"
    
    # USB Ports
    usb_match = re.search(r'(\d+)\s+USB\s+Ports?', text, re.IGNORECASE)
    if usb_match:
        features["technology"]["usb_ports"] = usb_match.group(1)
    
    features["technology"]["navigation"] = bool(re.search(r'Navigation\s+System', text, re.IGNORECASE))
    features["technology"]["rear_entertainment"] = bool(re.search(r'Rear\s+Entertainment', text, re.IGNORECASE))
    
    # ============ WHEELS & TYRES ============
    # Tyre size
    tyre_match = re.search(r'(\d{3}/\d{2}\s+R\d{2})', text)
    if tyre_match:
        features["wheels"]["tyre_size"] = tyre_match.group(1)
    
    # Alloy wheels
    alloy_match = re.search(r'(\d+)[- ]?inch\s+(?:Diamond[- ]?Cut\s+)?Alloy\s+Wheels?', text, re.IGNORECASE)
    if alloy_match:
        if re.search(r'Diamond[- ]?Cut', text, re.IGNORECASE):
            features["wheels"]["alloy_wheels"] = f"{alloy_match.group(1)}-inch Diamond-Cut"
        else:
            features["wheels"]["alloy_wheels"] = f"{alloy_match.group(1)}-inch"
    elif re.search(r'Alloy\s+Wheels?', text, re.IGNORECASE):
        features["wheels"]["alloy_wheels"] = True
    
    # ============ EXTERIOR ============
    features["exterior"]["led_headlamps"] = bool(re.search(r'LED\s+(?:Headlamps?|Projector)', text, re.IGNORECASE))
    features["exterior"]["led_drls"] = bool(re.search(r'LED\s+(?:DRL|Daytime\s+Running)', text, re.IGNORECASE))
    features["exterior"]["fog_lamps"] = bool(re.search(r'Fog\s+Lamps?', text, re.IGNORECASE))
    features["exterior"]["roof_rails"] = bool(re.search(r'Roof\s+Rails?', text, re.IGNORECASE))
    
    # ============ DRIVETRAIN ============
    if re.search(r'AllGrip\s+Pro|4WD|4x4|Four\s+Wheel\s+Drive', text, re.IGNORECASE):
        if re.search(r'AllGrip\s+Pro', text, re.IGNORECASE):
            features["drivetrain"] = "AllGrip Pro 4WD"
        else:
            features["drivetrain"] = "4WD"
    
    # ============ HYBRID ============
    if re.search(r'Strong\s+Hybrid|Self[- ]?Charging\s+Hybrid', text, re.IGNORECASE):
        features["hybrid"] = "Strong Hybrid (Self-Charging)"
    elif re.search(r'(?:Mild|Smart)\s+Hybrid', text, re.IGNORECASE):
        features["hybrid"] = "Mild Hybrid"
    
    if re.search(r'EV\s+Mode', text, re.IGNORECASE):
        features["ev_mode"] = True
    
    # ============ DIMENSIONS ============
    length_match = re.search(r'Length[:\s]+(\d+)\s*mm', text, re.IGNORECASE)
    if length_match:
        features["dimensions"]["length"] = f"{length_match.group(1)}mm"
    
    width_match = re.search(r'Width[:\s]+(\d+)\s*mm', text, re.IGNORECASE)
    if width_match:
        features["dimensions"]["width"] = f"{width_match.group(1)}mm"
    
    height_match = re.search(r'Height[:\s]+(\d+)\s*mm', text, re.IGNORECASE)
    if height_match:
        features["dimensions"]["height"] = f"{height_match.group(1)}mm"
    
    wheelbase_match = re.search(r'Wheelbase[:\s]+(\d+)\s*mm', text, re.IGNORECASE)
    if wheelbase_match:
        features["dimensions"]["wheelbase"] = f"{wheelbase_match.group(1)}mm"
    
    # Clean up empty dictionaries
    for key in list(features.keys()):
        if isinstance(features[key], dict) and not features[key]:
            del features[key]
    
    return features


def extract_from_brochure(pdf_path, model_name):
    """Extract text and features from PDF brochure"""
    print(f"\n{'='*60}")
    print(f"Processing: {model_name}")
    print('='*60)
    
    try:
        doc = fitz.open(pdf_path)
        all_text = ""
        
        # Extract text from all pages
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            all_text += text + "\n"
        
        doc.close()
        
        # Save raw text
        output_file = f"extracted_{model_name.lower().replace(' ', '_')}_complete.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(all_text)
        print(f"✓ Extracted text saved to: {output_file}")
        
        # Extract features
        features = extract_comprehensive_features(all_text, model_name)
        
        # Save features JSON
        json_file = f"extracted_{model_name.lower().replace(' ', '_')}_features.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(features, f, indent=2, ensure_ascii=False)
        print(f"✓ Features saved to: {json_file}")
        
        # Print summary
        print(f"\n📊 Feature Summary:")
        for category, items in features.items():
            if isinstance(items, dict):
                print(f"  {category}: {len(items)} items")
                for key, value in items.items():
                    if value and value != False:
                        print(f"    - {key}: {value}")
            else:
                print(f"  {category}: {items}")
        
        return features
        
    except Exception as e:
        print(f"❌ Error processing {model_name}: {str(e)}")
        return None


def main():
    """Process all brochures"""
    brochures = {
        "Baleno": "brochures/NEXA-Baleno-Brochure.pdf",
        "Fronx": "brochures/NEXA-FRONX-Brochure.pdf",
        "Grand Vitara": "brochures/NEXA-Grand-Vitara-Brochure.pdf",
        "Ignis": "brochures/Nexa-Ignis-Brochure.pdf",
        "Invicto": "brochures/NEXA-Invicto-Brochure.pdf",
        "Jimny": "brochures/NEXA-Jimny-Brochure.pdf",
        "XL6": "brochures/NEXA-Xl6-Brochure.pdf",
        "Ciaz": "brochures/Ciaz_Brochure.pdf"
    }
    
    all_features = {}
    
    for model_name, pdf_path in brochures.items():
        if Path(pdf_path).exists():
            features = extract_from_brochure(pdf_path, model_name)
            if features:
                all_features[model_name] = features
        else:
            print(f"⚠️  Brochure not found: {pdf_path}")
    
    # Save combined features
    with open("all_extracted_features_complete.json", 'w', encoding='utf-8') as f:
        json.dump(all_features, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print("✅ Extraction Complete!")
    print(f"Processed {len(all_features)} models")
    print("Combined features saved to: all_extracted_features_complete.json")
    print('='*60)


if __name__ == "__main__":
    main()
