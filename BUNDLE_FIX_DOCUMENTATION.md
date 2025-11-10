# Shopify Bundle Selector Fix

## Issues Fixed

### 1. **Persistence Across Page Loads** ✅
- **Problem**: When returning to the page, the selected radio button didn't match the displayed image
- **Solution**: Implemented localStorage to save and restore the last selected option per product

### 2. **Variant Changes Reset Selection** ✅
- **Problem**: Changing product variants (colors) always reset to the "purchase" option
- **Solution**: Added logic to maintain the current selection when variants change, only updating the bundle thumbnail image

## Key Changes Made

### A. Added Persistence Layer
```javascript
const STORAGE_KEY = 'nira_selected_option';

function saveSelectedOption(optionValue) {
  localStorage.setItem(STORAGE_KEY + '_' + PRODUCT_HANDLE, optionValue);
}

function getSelectedOption() {
  return localStorage.getItem(STORAGE_KEY + '_' + PRODUCT_HANDLE) || 'bundle';
}
```

### B. Created Unified `applySelection()` Function
This function handles all selection changes in one place:
- Unchecks all radios
- Checks the correct one
- Updates images appropriately
- Shows/hides the correct buttons
- Saves to localStorage

### C. Modified Variant Observer
The variant change observer now:
1. Updates only the bundle thumbnail based on the variant
2. **Does NOT auto-select any radio button**
3. Re-applies the saved selection after a brief delay
4. Only changes the main image if the bundle option is currently selected

### D. Removed Auto-Check on Page Load
Changed from `checked` attribute in HTML to JavaScript-controlled based on localStorage

## How It Works Now

### On Page Load:
1. Reads the saved selection from localStorage
2. Applies that selection (radio + image + buttons)
3. User sees exactly what they last selected

### When User Clicks a Radio:
1. Selection is applied via `applySelection()`
2. State is saved to localStorage
3. Image and buttons update accordingly

### When User Changes Variant (Color):
1. Variant ID updates
2. Bundle thumbnail updates (if applicable)
3. **Current radio selection is maintained**
4. If bundle is selected, main image updates to new variant's bundle image
5. If purchase/subscribe is selected, original product image shows

### When User Returns to Page:
1. Saved selection is loaded from localStorage
2. Page state matches their last choice
3. Works across browser sessions

## Implementation Steps

1. **Replace your current code** with the fixed version in `shopify-bundle-fix.liquid`

2. **Test these scenarios**:
   - Select bundle → refresh page → should still show bundle selected
   - Select purchase → change color → should stay on purchase
   - Select subscribe → change color → should stay on subscribe
   - Switch between products → each remembers its own selection

3. **Browser Compatibility**: Uses try/catch around localStorage for older browsers

## Code Structure

```
┌─────────────────────────────────────────┐
│  Persistence Layer (localStorage)       │
│  - saveSelectedOption()                 │
│  - getSelectedOption()                  │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  Selection Application                  │
│  - applySelection()                     │
│  - Updates radios, images, buttons      │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  Event Handlers                         │
│  - Radio clicks → applySelection()      │
│  - Variant changes → maintain selection │
│  - Page load → restore selection        │
└─────────────────────────────────────────┘
```

## Important Notes

- Each product handle gets its own localStorage key
- The `checked` attribute was removed from the bundle radio HTML
- Added safety checks for all DOM elements
- Variant changes wait 100ms before re-applying selection (prevents race conditions)
- Bundle radio is the default if no saved selection exists

## Troubleshooting

**If selections still reset:**
- Check browser console for errors
- Verify radio button IDs match: `bundle-radio`, `flex-pricing-option-1`, `flex-pricing-option-2`
- Ensure no other JavaScript is programmatically changing radios

**If images don't update:**
- Verify bundle_img_src variable is populated
- Check that `.bundle-thumb` and `.img-thumb` classes exist
- Confirm image URLs are accessible

**If localStorage doesn't work:**
- Private browsing mode blocks localStorage
- Check browser settings allow storage
- The code has fallbacks to default to 'bundle'
