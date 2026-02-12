# NEXA Price Explorer with January 2026 Offers

## 🎉 What's New

This update integrates January 2026 promotional offers directly into the price calculation system. All prices now automatically show discounted amounts based on current offers!

## ✨ Features

### Automatic Offer Application
- **Consumer Offers** and **Retail Support** are automatically deducted from ex-showroom prices
- Discounted on-road prices calculated automatically
- No manual calculation needed!

### Complete Offer Information
Every price breakdown now shows:
1. Original Ex-Showroom Price
2. Consumer Offer (deducted) 🔻
3. Retail Support (deducted) 🔻
4. **Discounted Ex-Showroom Price** ✅
5. Insurance, Road Tax, Registration, etc.
6. **Discounted On-Road Price** ✅
7. Exchange Bonus (informational) 💰
8. Corporate/Rural Offer (informational) 💰

### All Models Supported
✅ Ignis  
✅ Baleno  
✅ Fronx  
✅ Grand Vitara  
✅ XL6  
✅ Jimny  
✅ Invicto  
✅ Ciaz  

## 🚀 How to Use

1. **Start the server** (if not already running):
   ```bash
   python -m http.server 8080
   ```

2. **Open in browser**:
   - Main app: http://localhost:8080/index.html
   - Test page: http://localhost:8080/test_offers.html

3. **Select and Compare**:
   - Choose a model from dropdown
   - Select a variant
   - Click "Show Price" to see discounted pricing
   - Add multiple variants to compare with all offer details

## 📊 Offer Highlights

### Biggest Discounts
- **Grand Vitara Strong Hybrid**: Up to ₹50,000 automatic discount + ₹1,50,000 exchange bonus
- **Invicto**: Up to ₹50,000 automatic discount + ₹1,65,000 exchange bonus
- **Baleno/Ignis MT**: ₹25,000 automatic discount

### Additional Benefits
- **Exchange Bonus**: Available for all models (₹15,000 to ₹1,65,000)
- **Corporate Offer**: For corporate customers (up to ₹4,100)
- **Rural Offer**: For IFFCO/Shagun customers (up to ₹4,100)
- **Scrappage Bonus**: When scrapping old vehicle (₹3,500 to ₹15,000)

## 📁 Key Files

### Data Files
- `data/january_offers.json` - All offer data in structured format
- `data/*_6_airbag.json` - Price data for each model
- `data/*_features.json` - Feature data for each model

### Application Files
- `index.html` - Main application with offer integration
- `features.html` - Feature comparison tool
- `test_offers.html` - Offer matching test page

### Documentation
- `OFFERS_IMPLEMENTATION.md` - Technical implementation details
- `JANUARY_2026_OFFERS.md` - Quick reference for all offers
- `README.md` - This file

## 🔧 Technical Details

### Offer Matching System
The app uses intelligent pattern matching to apply correct offers:
- Matches by variant name (SIGMA, DELTA, ZETA, ALPHA)
- Handles transmission types (MT, AT, AGS, AMT)
- Recognizes fuel types (Petrol, CNG, Hybrid)
- Special handling for Strong Hybrid and 4WD variants

### Price Calculation
```javascript
Discounted Ex-Showroom = Original Ex-Showroom - Consumer Offer - Retail Support
Discounted On-Road = Original On-Road - Consumer Offer - Retail Support
```

### Visual Indicators
- 🟡 Yellow background: Discount rows
- 🟢 Green background: Discounted final price
- 🔵 Blue background: Additional bonus offers

## 📱 Progressive Web App

The app can be installed on your device:
1. Click the install button in your browser
2. Add to home screen on mobile
3. Works offline after first load

## 🧪 Testing

Run the test page to verify offer matching:
```
http://localhost:8080/test_offers.html
```

This shows:
- All models and variants
- Which offers are applied
- Match success rate
- Offer amounts for each variant

## 📝 Updating Offers

To update for future months:
1. Edit `data/january_offers.json`
2. Update the "month" field
3. Modify offer amounts as needed
4. Update header text in `index.html` if desired

No code changes required for regular offer updates!

## 💡 Tips

- **Compare Feature**: Add multiple variants to see side-by-side offer comparison
- **Best Value**: Green highlighting shows the best price when comparing
- **All Inclusive**: On-road price includes all taxes and charges with discounts applied
- **Transparency**: Full breakdown shows exactly what's included

## 🎯 Offer Types Explained

### Automatically Deducted (Shown in Yellow)
- **Consumer Offer**: Direct discount from manufacturer
- **Retail Support**: Additional dealer support

### Additional Benefits (Shown in Blue)
These are available but not automatically deducted:
- **Exchange Bonus**: When exchanging old vehicle
- **Corporate Offer**: For corporate purchases (requires corporate ID)
- **Rural Offer**: For rural customers (IFFCO/Shagun scheme)
- **Scrappage Bonus**: When scrapping old vehicle

## 🌟 Example

**Grand Vitara Strong Hybrid ZETA+**
- Ex-Showroom: ₹19,00,000
- Consumer Offer: -₹25,000
- Retail Support: -₹25,000
- **Discounted Ex-Showroom: ₹18,50,000**
- (+ taxes, insurance, etc.)
- **Discounted On-Road: ~₹21,50,000**
- Exchange Bonus: ₹1,50,000 (can be availed)
- Corporate/Rural: ₹4,100 (if eligible)

Total savings potential: ₹2,04,100!

## 📞 Support

For actual purchase and final prices, please contact your nearest NEXA dealership. Prices and offers are indicative and may vary by location.

---

*Last Updated: January 2026*  
*Offers valid for January 2026. Terms and conditions apply.*
