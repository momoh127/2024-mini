// ============================================
// COMPLETE SCRIPT WITH CHANGES HIGHLIGHTED
// ============================================

document.addEventListener('DOMContentLoaded', function () {
console.log('current product',{{ product|json }})
console.log('skincare',{{ extra_product|json }})
console.log('pro_bund',{{ pro_bundle_id|json }})

// ============================================
// 🆕 NEW: PERSISTENCE LAYER
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
// ============================================
// END NEW SECTION
// ============================================

// Grab radios
const bundleRadio = document.getElementById('bundle-radio');
const purchaseRadio = document.getElementById('flex-pricing-option-1');
const purchaseOptionDiv = document.getElementById('fragile-non-subscription-option');
const subscribeRadio = document.getElementById('flex-pricing-option-2');
const subscribeOptionDiv = document.getElementById('fragile-subscription-option');
const subscribeBtn = document.getElementById('fragile-subscribe');
const addToCartBtns = document.querySelectorAll('.product__block--buy_buttons');
const addToCartButtons = document.querySelectorAll('.product-form__buttons');
const mainImgEl = document.querySelector('.product__media.media-wrapper img');
const bundleImgSrc =
document.getElementById('bundle-option')?.getAttribute('data-bundle-img');
const sticky_atc = document.querySelector('.sticky-atc-bar')
const selectedOption=document.querySelector('.fragile-pricing-option')
const fragileBenefits =
document.querySelectorAll('.fragile-pricing-option-benefits');

// Safety check
if (!bundleRadio || !purchaseRadio || !subscribeRadio) {
 console.log('One or more radio buttons are missing');
 return;
}

let originalMedia = {{original_media|json}};

function getActiveMediaImg() {
 const active = document.querySelector('.product__media-gallery-viewer .swiper-slide-active img');
 if (active) return active;
 return document.querySelector('.product__media-gallery-viewer img');
}

function swapMainMedia(toSrc) {
 if (!toSrc) return;
 const imgEl = getActiveMediaImg();
 if (!imgEl) return;
 if (!originalMedia) {
 originalMedia = {
 el: imgEl,
 src: imgEl.getAttribute('src'),
 srcset: imgEl.getAttribute('srcset')
 };
 }
 imgEl.setAttribute('src', toSrc);
 imgEl.setAttribute('srcset', toSrc);
}

// ✏️ MODIFIED: Added safety check for sticky_atc
function hideStickyATC(){
 if (sticky_atc) sticky_atc.style.display = "none"; // ⬅️ ADDED: null check
}

// ✏️ MODIFIED: Added safety check for sticky_atc
function showstickyATC(){
 if (sticky_atc) sticky_atc.style.display = ""; // ⬅️ ADDED: null check
}

function changeMainThumb(bundleSrc) {
  const thumb = document.querySelector('.bundle-thumb');
  console.log('change bundle func')
  if (!thumb) return;
  thumb.src = bundleSrc;
}

function changeAllThumbs(src) {
 document.querySelectorAll('.img-thumb').forEach(img => {
 img.src = src;
 });
}

function closeBenefits(){
 fragileBenefits.forEach(el => {
   el.style.display = 'none';
 });
}

// ✏️ MODIFIED: Added safety checks
function showAddToCart() {
  hideSubscribe();
  const firstDiv = document.querySelector('.product-form__buttons');
  if (firstDiv) firstDiv.style.display = ""; // ⬅️ ADDED: null check
  
  const secondDiv = document.querySelector('.product__block--buy_buttons');
  if (secondDiv) { // ⬅️ ADDED: null check
    secondDiv.style.display = "";
    secondDiv.classList.remove("hidden")
  }
  console.log(firstDiv)
  console.log(secondDiv)
}

function showSubscribe() {
 if (subscribeBtn) subscribeBtn.style.display = "";
}

function hideSubscribe() {
 if (subscribeBtn) subscribeBtn.style.display = "none";
}

function updateButtons() {
 if (subscribeRadio?.checked) {
   showSubscribe();
 } else {
   // bundle or purchase
   hideSubscribe();
   showAddToCart();
 }
}

// ============================================
// 🆕 NEW: UNIFIED SELECTION APPLICATION FUNCTION
// ============================================
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

// 🆕 NEW: Load and apply saved selection on page load
const savedOption = getSelectedOption();
applySelection(savedOption, true); // true = don't save again, just apply
// ============================================
// END NEW SECTION
// ============================================


// ❌ REMOVED: Old initialization logic
// --------------------------------------------------
// Run on load
// updateButtons();
//
// if (bundleRadio?.checked) {
//   console.log('✅ Bundle is selected on load. Swapping image to bundle.');
//   swapMainMedia({{bundle_img_src|json}});
//   hideStickyATC()
// }
// --------------------------------------------------


// ============================================
// ✏️ MODIFIED: EVENT LISTENERS WITH PERSISTENCE
// ============================================

// STEP 1: Bundle radio click
// ✏️ MODIFIED: Now uses applySelection() instead of manual updates
bundleRadio.addEventListener('click', function () {
 if (this.checked) {
   console.log('[BUNDLE] clicked and selected', this.checked);
   applySelection('bundle'); // ⬅️ CHANGED: Single function call with persistence
   
   // ❌ REMOVED: Manual state management
   // --------------------------------------------------
   // purchaseRadio.checked = false;
   // subscribeRadio.checked = false;
   // closeBenefits()
   // if (selectedOption) selectedOption.classList.remove('selected');
   // swapMainMedia({{ bundle_img_src|json }})
   // updateButtons()
   // hideStickyATC()
   // --------------------------------------------------
 }
});

// STEP 2: Purchase option click
// ✏️ MODIFIED: Now uses applySelection() instead of manual updates
purchaseOptionDiv?.addEventListener('click', function () {
  console.log('purchase clicked')
  if (purchaseRadio) {
    console.log('purchase condition')
    applySelection('purchase'); // ⬅️ CHANGED: Single function call with persistence
    
    // ❌ REMOVED: Manual state management
    // --------------------------------------------------
    // purchaseRadio.checked = true;
    // bundleRadio.checked = false;
    // subscribeRadio.checked = false;
    // swapMainMedia(originalMedia);
    // updateButtons()
    // showstickyATC()
    // --------------------------------------------------
  }
});

// STEP 3: Subscribe option click
// ✏️ MODIFIED: Now uses applySelection() instead of manual updates
subscribeOptionDiv?.addEventListener('click', function () {
  console.log('subscribe clicked')
  if (subscribeRadio) {
    applySelection('subscribe'); // ⬅️ CHANGED: Single function call with persistence
    
    // ❌ REMOVED: Manual state management
    // --------------------------------------------------
    // subscribeRadio.checked = true;
    // bundleRadio.checked = false;
    // purchaseRadio.checked = false;
    // swapMainMedia(originalMedia);
    // updateButtons()
    // showstickyATC()
    // --------------------------------------------------
  }
});

// 🆕 NEW: Also listen to direct radio changes (in case they're triggered programmatically)
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

// ============================================
// ✏️ HEAVILY MODIFIED: VARIANT CHANGE HANDLING
// ============================================
const productForm = document.querySelector('form[action*="/cart/add"]');
if (!productForm) return;
const variantIdInput = productForm.querySelector('[name="id"]');
if (!variantIdInput) return;

let currentVariantId = Number(variantIdInput.value) || null;
window.currentVariantId = currentVariantId;
console.log('Initial variant ID:', currentVariantId);

// 🆕 NEW: Flag to prevent interference during variant changes
let isChangingVariant = false;

// Observer for Shopify's script changing the variant ID
const observer = new MutationObserver(() => {
  const newId = Number(variantIdInput.value);
  if (!newId || newId === currentVariantId) return;
  
  isChangingVariant = true; // 🆕 NEW: Set flag
  currentVariantId = newId;
  window.currentVariantId = newId;
  console.log('Variant updated →', newId);
  
  // ✏️ MODIFIED: Update bundle thumb based on variant WITHOUT changing the selected radio
  (function initBundleThumb() {
    console.log('change img for variant'); // ⬅️ CHANGED: Updated log message
    if (currentVariantId === 52955689320814) {
      console.log('champagne variant'); // ⬅️ CHANGED: Updated log message
      let imgSrc = "https://cdn.shopify.com/s/files/1/0073/0231/6068/files/NIRA_Champagne_1500x1500_cf8319fd-520a-4386-9fd3-be29c976576d.png?v=1762526772";
      changeMainThumb(imgSrc);
      
      // 🆕 NEW: Only swap main media if bundle is selected
      if (bundleRadio.checked) {
        swapMainMedia(imgSrc);
      }
      changeAllThumbs(imgSrc);
    } else {
      changeMainThumb({{ bundle_img_src | json }});
      changeAllThumbs(originalMedia);
      
      // 🆕 NEW: Only swap main media if bundle is selected
      if (bundleRadio.checked) {
        swapMainMedia({{ bundle_img_src | json }});
      }
    }
  })();
  
  // 🆕 NEW: Re-apply the saved selection to maintain state after variant change
  const currentSelection = getSelectedOption();
  console.log('🔄 Maintaining selection after variant change:', currentSelection);
  
  // 🆕 NEW: Small delay to ensure Shopify's code doesn't interfere
  setTimeout(() => {
    applySelection(currentSelection, true); // ⬅️ Restore saved selection
    isChangingVariant = false; // ⬅️ Clear flag
  }, 100);
});

observer.observe(variantIdInput, {
 attributes: true,
 attributeFilter: ['value']
});

// ============================================
// CART ADD LOGIC (UNCHANGED)
// ============================================
const EXTRA_VARIANT_ID = 41296162684964;
const selling_plan_id = 691889275246;

document.addEventListener('click', function (e) {
  const product_id = currentVariantId;
  const btn = e.target.closest('.product-form__submit');
  if (!btn) return;
  
  // 🆕 NEW: Only intercept if bundle is selected
  if (!bundleRadio.checked) return;
  
  e.preventDefault();
  const form = btn.closest('form');
  const qty = 1;
  const payload = {
    items: [
      {
        id: EXTRA_VARIANT_ID,
        quantity: 1,
        ...(selling_plan_id ? { selling_plan: selling_plan_id } : {})
      },
      {
        id: product_id,
        quantity: qty
      }
    ]
  };
  
  fetch('/cart/add.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(() => { 
    console.log('✅ Bundle added to cart'); // ⬅️ ADDED: Success log
    // Optional: trigger cart drawer open
    if (window.theme && window.theme.openCart) {
      window.theme.openCart();
    }
  })
  .catch(err => {
    console.error('❌ Error adding to cart:', err); // ⬅️ ADDED: Error log
  });
});

});

// ============================================
// LEGEND:
// ============================================
// 🆕 NEW: Completely new code added
// ✏️ MODIFIED: Existing code that was changed
// ❌ REMOVED: Code that was deleted (shown in comments)
// ⬅️ Inline markers for specific changes
// ============================================
