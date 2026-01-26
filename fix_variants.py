import json
import os

# Script to check and report variant name mismatches

data_dir = "data"

models = {
    "baleno": ("baleno_6_airbag.json", "baleno_features.json"),
    "fronx": ("new_fronx_6_airbag.json", "fronx_features.json"),
    "grand_vitara": ("grand_vitara_6_airbag.json", "grand_vitara_features.json"),
    "ignis": ("ignis.json", "ignis_features.json"),
    "invicto": ("invicto.json", "invicto_features.json"),
    "jimny": ("jimny.json", "jimny_features.json"),
    "xl6": ("new_xl6_6_airbag.json", "xl6_features.json"),
    "ciaz": ("ciaz.json", "ciaz_features.json")
}

for model_name, (price_file, features_file) in models.items():
    print(f"\n{'='*60}")
    print(f"MODEL: {model_name.upper()}")
    print('='*60)
    
    # Load price data
    with open(os.path.join(data_dir, price_file), 'r') as f:
        price_data = json.load(f)
    
    # Load features data
    with open(os.path.join(data_dir, features_file), 'r') as f:
        features_data = json.load(f)
    
    # Get variant names from price file
    price_variants = [item['variant'] for item in price_data]
    
    # Get variant names from features file
    feature_variants = list(features_data.get('variant_features', {}).keys())
    
    print(f"\nPrice variants ({len(price_variants)}):")
    for v in sorted(price_variants):
        print(f"  - {v}")
    
    print(f"\nFeature variants ({len(feature_variants)}):")
    for v in sorted(feature_variants):
        print(f"  - {v}")
    
    # Find mismatches
    price_set = set(price_variants)
    feature_set = set(feature_variants)
    
    missing_in_features = price_set - feature_set
    extra_in_features = feature_set - price_set
    
    if missing_in_features:
        print(f"\n⚠️  MISSING in variant_features ({len(missing_in_features)}):")
        for v in sorted(missing_in_features):
            print(f"  - {v}")
    
    if extra_in_features:
        print(f"\n⚠️  EXTRA in variant_features (not in prices) ({len(extra_in_features)}):")
        for v in sorted(extra_in_features):
            print(f"  - {v}")
    
    if not missing_in_features and not extra_in_features:
        print("\n✅ Perfect match!")
