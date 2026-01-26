import json
import os

def merge_features(model_name, model_file_suffix):
    """Merge extracted features into existing feature file"""
    
    # File paths
    extracted_file = f"extracted_{model_file_suffix}_features.json"
    existing_file = f"data/{model_file_suffix}_features.json"
    
    if not os.path.exists(extracted_file):
        print(f"⚠️  Skipping {model_name}: extracted file not found")
        return
    
    if not os.path.exists(existing_file):
        print(f"⚠️  Skipping {model_name}: existing file not found")
        return
    
    # Load files
    with open(extracted_file, 'r', encoding='utf-8') as f:
        extracted = json.load(f)
    
    with open(existing_file, 'r', encoding='utf-8') as f:
        existing = json.load(f)
    
    # Merge top-level features (safety, comfort, technology, wheels, exterior)
    # Preserve existing engine, transmission, mileage, variants, and variant_features
    
    # Update safety_features - merge extracted with existing
    if 'safety_features' in existing:
        existing['safety_features'].update(extracted.get('safety_features', {}))
    else:
        existing['safety_features'] = extracted.get('safety_features', {})
    
    # Update comfort_features
    if 'comfort_features' in existing:
        existing['comfort_features'].update(extracted.get('comfort_features', {}))
    else:
        existing['comfort_features'] = extracted.get('comfort_features', {})
    
    # Update technology
    if 'technology' in existing:
        existing['technology'].update(extracted.get('technology', {}))
    else:
        existing['technology'] = extracted.get('technology', {})
    
    # Update wheels
    if 'wheels' in existing:
        existing['wheels'].update(extracted.get('wheels', {}))
    else:
        existing['wheels'] = extracted.get('wheels', {})
    
    # Add exterior if not exists
    if 'exterior' not in existing and 'exterior' in extracted:
        existing['exterior'] = extracted.get('exterior', {})
    elif 'exterior' in extracted:
        existing['exterior'].update(extracted.get('exterior', {}))
    
    # Add dimensions if exists in extracted
    if 'dimensions' in extracted:
        existing['dimensions'] = extracted.get('dimensions', {})
    
    # Add drivetrain if exists in extracted
    if 'drivetrain' in extracted:
        existing['drivetrain'] = extracted.get('drivetrain', {})
    
    # Add hybrid if exists in extracted
    if 'hybrid' in extracted:
        existing['hybrid'] = extracted.get('hybrid', {})
    
    # Save updated file
    with open(existing_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {model_name}: Features merged successfully")
    print(f"   - Safety: {len(existing.get('safety_features', {}))} items")
    print(f"   - Comfort: {len(existing.get('comfort_features', {}))} items")
    print(f"   - Technology: {len(existing.get('technology', {}))} items")
    print(f"   - Wheels: {len(existing.get('wheels', {}))} items")
    if 'exterior' in existing:
        print(f"   - Exterior: {len(existing.get('exterior', {}))} items")
    if 'dimensions' in existing:
        print(f"   - Dimensions: {len(existing.get('dimensions', {}))} items")
    if 'drivetrain' in existing:
        print(f"   - Drivetrain: {existing.get('drivetrain')}")
    if 'hybrid' in existing:
        print(f"   - Hybrid: {existing.get('hybrid')}")
    print()

def main():
    print("=" * 60)
    print("Merging Extracted Features into Existing Files")
    print("=" * 60)
    print()
    
    models = [
        ("Baleno", "baleno"),
        ("Fronx", "fronx"),
        ("Grand Vitara", "grand_vitara"),
        ("Ignis", "ignis"),
        ("Invicto", "invicto"),
        ("Jimny", "jimny"),
        ("XL6", "xl6"),
        ("Ciaz", "ciaz")
    ]
    
    for model_name, file_suffix in models:
        merge_features(model_name, file_suffix)
    
    print("=" * 60)
    print("✅ Merge Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
