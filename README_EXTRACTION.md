# 📄 Brochure Data Extraction Guide

Extract tables and specifications from PDF brochures using Python.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# In VS Code terminal
pip install -r requirements.txt
```

**Note:** This will install:
- **PyMuPDF** - Fast PDF text extraction
- **PaddleOCR** - Advanced OCR for image-based PDFs
- **pandas** - Data manipulation
- **OpenCV** - Image processing

### 2. Prepare Your Brochures

```bash
# Create brochures folder
mkdir brochures

# Place your PDF brochures there
# Example: brochures/baleno_brochure.pdf
```

### 3. Run Extraction

```bash
python extract_brochure_data.py
```

## 📋 Features

### Method 1: Direct Text Extraction (Recommended)
- ✅ **Fast** - Instant extraction from text-based PDFs
- ✅ **Accurate** - No OCR errors
- ✅ **Layout aware** - Preserves table structure

**Use when:** Your PDF has selectable text

### Method 2: OCR Extraction
- ✅ **Works with scanned PDFs** - Extract from images
- ✅ **Handles complex layouts** - Multiple columns, rotated text
- ⚠️ **Slower** - Takes time for OCR processing

**Use when:** Your PDF is scanned or has text as images

## 🔧 Customization

### Extract Specific Data

Edit `extract_brochure_data.py` and customize these functions:

```python
def parse_engine_specs(text):
    # Add regex patterns for your specific data
    # Example: Extract variant names, prices, etc.
```

### Convert to Your Format

```python
def convert_to_json_format(data, model_name):
    # Map extracted data to your JSON structure
    # Matches: baleno_6_airbag.json format
```

## 📊 Output Format

The script generates `extracted_data.json` with:

```json
[
  {
    "page": 1,
    "text": "Full page text...",
    "specs": {
      "displacement": "1197cc",
      "power_text": "90PS @ 6000 rpm",
      "torque_text": "113Nm @ 4400 rpm",
      "mileage": "22.35"
    }
  }
]
```

## 💡 Tips

### For Better OCR Results:
1. Use **high-quality scans** (300 DPI minimum)
2. **Straighten pages** before scanning
3. Use **good lighting** for photos

### For Table Extraction:
1. Check if PDF has **selectable text** first (try copying text)
2. If scanned, use **OCR method**
3. For complex tables, consider **Tabula-py** or **Camelot**

## 🎯 Common Use Cases

### Extract Price Table
```python
# Look for price patterns
price_pattern = r'₹\s*(\d{1,3}(?:,\d{3})*)'
prices = re.findall(price_pattern, text)
```

### Extract Specifications Table
```python
# Look for spec keywords
specs = {
    'engine': re.search(r'Engine.*?(\d+cc)', text),
    'power': re.search(r'Power.*?(\d+\s*PS)', text),
    'torque': re.search(r'Torque.*?(\d+\s*Nm)', text)
}
```

### Extract Variant Names
```python
# Common variant patterns
variants = re.findall(r'(SIGMA|DELTA|ZETA|ALPHA)', text, re.IGNORECASE)
```

## 🔍 Debugging

### View extracted text:
```python
print(text[:1000])  # First 1000 characters
```

### Check OCR confidence:
```python
for line in ocr_data:
    if line['confidence'] < 0.8:
        print(f"Low confidence: {line['text']}")
```

### Save images for inspection:
```python
# Don't delete temp images
# Path(img_path).unlink(missing_ok=True)  # Comment this
```

## 📦 Alternative Tools

- **Tabula-py** - Excel-like table extraction
- **Camelot** - Advanced PDF table extraction
- **pdfplumber** - Detailed PDF parsing
- **Tesseract OCR** - Open-source OCR alternative

## 🆘 Troubleshooting

**OCR not working?**
- Ensure PaddlePaddle is installed correctly
- Try CPU-only version if GPU issues occur

**Table extraction messy?**
- Use OCR method for scanned PDFs
- Try pdfplumber for better table detection

**Slow extraction?**
- Process specific pages only
- Use direct text extraction instead of OCR
- Reduce image DPI if using OCR

## ✅ Next Steps

1. Extract data from brochures
2. Review `extracted_data.json`
3. Format to match your app's JSON structure
4. Copy to `data/` folder
5. Test in the app!
