# Before & After Comparison

## Change 1: HTML - Bundle Radio Button

### ❌ BEFORE
```html
<input
  type="radio"
  id="bundle-radio"
  name="bundle-option"
  class="bundle-radio"
  value="bundle"
  aria-label="Bundle: {{ product.title }} + {{ extra_product.title }}"
  checked    <!-- PROBLEM: Always checked on page load -->
>
```

### ✅ AFTER
```html
<input
  type="radio"
  id="bundle-radio"
  name="bundle-option"
  class="bundle-radio"
  value="bundle"
  aria-label="Bundle: {{ product.title }} + {{ extra_product.title }}"
  <!-- FIXED: Removed 'checked' - now controlled by JavaScript/localStorage -->
>
```

---

## Change 2: NEW Persistence Functions

### ❌ BEFORE
```javascript
// NOTHING - No persistence existed
```

### ✅ AFTER
```javascript
// ============================================
// PERSISTENCE LAYER
// ============================================
const STORAGE_KEY = 'nira_selected_option';
const PRODUCT_HANDLE = {{ product.handle | json }};

function saveSelectedOption(optionValue) {
  try {
    localStorage.setItem(STORAGE_KEY + '_' + PRODUCT_HANDLE, optionValue);
    console.log('💾 Saved selection:', optionValue);
  } catch (e) {
    console.warn('localStorage not available:', e);
  }
}

function getSelectedOption() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY + '_' + PRODUCT_HANDLE);
    console.log('📖 Retrieved selection:', saved);
    return saved || 'bundle'; // default to bundle
  } catch (e) {
    console.warn('localStorage not available:', e);
    return 'bundle';
  }
}
```

---

## Change 3: NEW Unified Selection Function

### ❌ BEFORE
```javascript
// NOTHING - Selection logic was scattered across multiple event handlers
```

### ✅ AFTER
```javascript
function applySelection(optionValue, skipSave = false) {
  console.log('🎯 Applying selection:', optionValue);
  
  // Uncheck all first
  bundleRadio.checked = false;
  purchaseRadio.checked = false;
  subscribeRadio.checked = false;
  
  // Apply the saved selection
  switch(optionValue) {
    case 'bundle':
      bundleRadio.checked = true;
      closeBenefits();
      if (selectedOption) selectedOption.classList.remove('selected');
      swapMainMedia({{ bundle_img_src|json }});
      hideStickyATC();
      break;
      
    case 'purchase':
      purchaseRadio.checked = true;
      swapMainMedia(originalMedia);
      showstickyATC();
      break;
      
    case 'subscribe':
      subscribeRadio.checked = true;
      swapMainMedia(originalMedia);
      showstickyATC();
      break;
  }
  
  updateButtons();
  
  if (!skipSave) {
    saveSelectedOption(optionValue);
  }
}
```

---

## Change 4: Page Load Initialization

### ❌ BEFORE
```javascript
// Run on load
updateButtons();

if (bundleRadio?.checked) {
  console.log('✅ Bundle is selected on load. Swapping image to bundle.');
  swapMainMedia({{bundle_img_src|json}});
  hideStickyATC()
}
// PROBLEM: Only checks if bundle is selected (which it always was due to 'checked' attribute)
// PROBLEM: Doesn't restore user's previous selection
```

### ✅ AFTER
```javascript
// Load and apply saved selection on page load
const savedOption = getSelectedOption();
applySelection(savedOption, true); // true = don't save again, just apply

// FIXED: Reads from localStorage and restores exact user selection
// FIXED: Works for bundle, purchase, AND subscribe options
```

---

## Change 5: Bundle Radio Click Handler

### ❌ BEFORE
```javascript
bundleRadio.addEventListener('click', function () {
 if (this.checked) {
   console.log('[BUNDLE] clicked and selected',this.checked);
   purchaseRadio.checked = false;
   subscribeRadio.checked = false;
   closeBenefits()
   if (selectedOption) selectedOption.classList.remove('selected');
   console.log('subscribeRadio?.checked',subscribeRadio?.checked)
   swapMainMedia({{ bundle_img_src|json }})
   updateButtons()
   hideStickyATC()
   // PROBLEM: No persistence - selection lost on page refresh
 }
});
```

### ✅ AFTER
```javascript
bundleRadio.addEventListener('click', function () {
 if (this.checked) {
   console.log('[BUNDLE] clicked and selected', this.checked);
   applySelection('bundle'); // ✅ FIXED: Single call handles everything + saves to localStorage
 }
});
```

---

## Change 6: Purchase Option Click Handler

### ❌ BEFORE
```javascript
purchaseOptionDiv?.addEventListener('click', function () {
  console.log('purchase clicked')
  if (purchaseRadio) {
    console.log('purchase condition')
    purchaseRadio.checked = true;
    // uncheck the others
    bundleRadio.checked = false;
    subscribeRadio.checked = false;
    swapMainMedia(originalMedia);
    updateButtons()
    showstickyATC()
    // PROBLEM: No persistence - selection lost on page refresh
  }
});
```

### ✅ AFTER
```javascript
purchaseOptionDiv?.addEventListener('click', function () {
  console.log('purchase clicked')
  if (purchaseRadio) {
    console.log('purchase condition')
    applySelection('purchase'); // ✅ FIXED: Single call handles everything + saves to localStorage
  }
});
```

---

## Change 7: Subscribe Option Click Handler

### ❌ BEFORE
```javascript
subscribeOptionDiv?.addEventListener('click', function () {
  console.log('subscribe clicked')
  if (subscribeRadio) {
    subscribeRadio.checked = true;
    bundleRadio.checked = false;
    purchaseRadio.checked = false;
    swapMainMedia(originalMedia); // or your desired restore logic
    updateButtons()
    showstickyATC()
    // PROBLEM: No persistence - selection lost on page refresh
  }
});
```

### ✅ AFTER
```javascript
subscribeOptionDiv?.addEventListener('click', function () {
  console.log('subscribe clicked')
  if (subscribeRadio) {
    applySelection('subscribe'); // ✅ FIXED: Single call handles everything + saves to localStorage
  }
});
```

---

## Change 8: NEW - Direct Radio Change Listeners

### ❌ BEFORE
```javascript
// NOTHING - If radios changed programmatically, no persistence would happen
```

### ✅ AFTER
```javascript
// Also listen to direct radio changes (in case they're triggered programmatically)
purchaseRadio.addEventListener('change', function() {
  if (this.checked) {
    applySelection('purchase');
  }
});

subscribeRadio.addEventListener('change', function() {
  if (this.checked) {
    applySelection('subscribe');
  }
});
```

---

## Change 9: Variant Observer (CRITICAL FIX)

### ❌ BEFORE
```javascript
const observer = new MutationObserver(() => {
  const newId = Number(variantIdInput.value);
  if (!newId || newId === currentVariantId) return;
  currentVariantId = newId;
  window.currentVariantId = newId;
  console.log('Variant updated →', newId);
  
  (function initBundleThumb() {
    console.log('change img')
    if (currentVariantId === 52955689320814) {
      console.log('chm change')
      let imgSrc="https://cdn.shopify.com/s/files/1/0073/0231/6068/files/NIRA_Champagne_1500x1500_cf8319fd-520a-4386-9fd3-be29c976576d.png?v=1762526772"
      changeMainThumb(imgSrc);
      swapMainMedia(imgSrc)  // PROBLEM: Always swaps main media
      changeAllThumbs(imgSrc)
    } else {
      changeMainThumb({{ bundle_img_src | json }});
      changeAllThumbs(originalMedia)
      // PROBLEM: Doesn't swap back to bundle image if bundle is selected
    }
  })();
  // PROBLEM: No logic to maintain radio selection - external code resets it
});
```

### ✅ AFTER
```javascript
const observer = new MutationObserver(() => {
  const newId = Number(variantIdInput.value);
  if (!newId || newId === currentVariantId) return;
  
  isChangingVariant = true; // ✅ NEW: Set flag
  currentVariantId = newId;
  window.currentVariantId = newId;
  console.log('Variant updated →', newId);
  
  // Update bundle thumb based on variant WITHOUT changing the selected radio
  (function initBundleThumb() {
    console.log('change img for variant');
    if (currentVariantId === 52955689320814) {
      console.log('champagne variant');
      let imgSrc = "https://cdn.shopify.com/s/files/1/0073/0231/6068/files/NIRA_Champagne_1500x1500_cf8319fd-520a-4386-9fd3-be29c976576d.png?v=1762526772";
      changeMainThumb(imgSrc);
      
      // ✅ FIXED: Only swap main media if bundle is selected
      if (bundleRadio.checked) {
        swapMainMedia(imgSrc);
      }
      changeAllThumbs(imgSrc);
    } else {
      changeMainThumb({{ bundle_img_src | json }});
      changeAllThumbs(originalMedia);
      
      // ✅ FIXED: Only swap main media if bundle is selected
      if (bundleRadio.checked) {
        swapMainMedia({{ bundle_img_src | json }});
      }
    }
  })();
  
  // ✅ NEW: Re-apply the saved selection to maintain state
  const currentSelection = getSelectedOption();
  console.log('🔄 Maintaining selection after variant change:', currentSelection);
  
  // ✅ NEW: Small delay to ensure Shopify's code doesn't interfere
  setTimeout(() => {
    applySelection(currentSelection, true);
    isChangingVariant = false;
  }, 100);
});
```

---

## Summary of All Changes

| Change | Type | Impact |
|--------|------|--------|
| 1. Remove `checked` from bundle radio | HTML | Allows JS control of initial state |
| 2. Add localStorage functions | NEW | Enables persistence across sessions |
| 3. Create `applySelection()` function | NEW | Centralizes all selection logic |
| 4. Update page load logic | MODIFIED | Restores saved selection on load |
| 5-7. Simplify click handlers | MODIFIED | Use `applySelection()` + save |
| 8. Add direct radio listeners | NEW | Catch programmatic changes |
| 9. Fix variant observer | CRITICAL | Maintains selection on variant change |

**Result:** 
- ✅ Selection persists across page refreshes
- ✅ Variant changes don't reset selection
- ✅ Images always match selected radio button
- ✅ Works for all three options (bundle/purchase/subscribe)
