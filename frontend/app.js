// ===== State =====
const state = {
  cart: {},          // { itemId: quantity }
  searchQuery: '',
  activePlate: 'All',
  activeCategory: 'All',
  splitCount: 2,
  customSplit: false,
  personNames: ['Person 1', 'Person 2'],
  personItems: {},   // { personIndex: { itemId: quantity } }
};

// ===== Helpers =====
function getMenu() {
  return typeof SUSHIRO_MENU !== 'undefined' ? SUSHIRO_MENU : [];
}

function getCategories() {
  const cats = new Set(getMenu().map(item => item.category));
  return ['All', ...Array.from(cats).sort()];
}

function getPlateForPrice(price) {
  if (!price || price <= 0) return null;
  if (price <= 12) return 'red';
  if (price <= 17) return 'silver';
  if (price <= 22) return 'gold';
  if (price <= 27) return 'black';
  return 'white';
}

function getFilteredItems() {
  let items = getMenu();
  if (state.activePlate !== 'All') {
    items = items.filter(i => getPlateForPrice(i.price) === state.activePlate);
  }
  if (state.activeCategory !== 'All') {
    items = items.filter(i => i.category === state.activeCategory);
  }
  if (state.searchQuery.trim()) {
    const q = state.searchQuery.toLowerCase();
    items = items.filter(i =>
      (i.title && i.title.toLowerCase().includes(q)) ||
      (i.description && i.description.toLowerCase().includes(q)) ||
      (i.category && i.category.toLowerCase().includes(q))
    );
  }
  return items;
}

function getCartItems() {
  const menu = getMenu();
  const items = [];
  for (const [id, qty] of Object.entries(state.cart)) {
    if (qty > 0) {
      const item = menu.find(m => String(m.id) === String(id));
      if (item) items.push({ ...item, qty });
    }
  }
  return items;
}

function getTotalItems() {
  return Object.values(state.cart).reduce((sum, q) => sum + q, 0);
}

function getTotalPrice() {
  const cartItems = getCartItems();
  return cartItems.reduce((sum, item) => sum + item.price * item.qty, 0);
}

function formatPrice(amount) {
  return `HK$${amount.toFixed(0)}`;
}

function getItemQty(id) {
  return state.cart[id] || 0;
}

function setItemQty(id, qty) {
  if (qty <= 0) {
    delete state.cart[id];
  } else {
    state.cart[id] = qty;
  }
  updateUI();
}

// ===== Plate Colors =====
const PLATE_COLORS = [
  { max: 12, color: 'red',    label: '紅碟', labelEn: 'Red Plate' },
  { max: 17, color: 'silver', label: '銀碟', labelEn: 'Silver Plate' },
  { max: 22, color: 'gold',   label: '金碟', labelEn: 'Gold Plate' },
  { max: 27, color: 'black',  label: '黑碟', labelEn: 'Black Plate' },
];

function getPlateInfo(price) {
  if (!price || price <= 0) return null;
  for (const plate of PLATE_COLORS) {
    if (price <= plate.max) return plate;
  }
  return { color: 'white', label: '白碟', labelEn: 'White Plate' };
}

// ===== Emoji for placeholder =====
const categoryEmojis = {
  'Nigiri': '🍣',
  'Sashimi': '🐟',
  'Maki': '🍙',
  'Roll': '🍙',
  'Udon': '🍜',
  'Ramen': '🍜',
  'Side': '🥟',
  'Dessert': '🍮',
  'Drink': '🥤',
  'Promotional': '⭐',
  'default': '🍽️',
};

function getEmoji(category) {
  for (const [key, emoji] of Object.entries(categoryEmojis)) {
    if (category && category.toLowerCase().includes(key.toLowerCase())) {
      return emoji;
    }
  }
  return categoryEmojis.default;
}

// ===== Render Functions =====
function renderPlateFilters() {
  const container = document.getElementById('plate-tabs');
  const plates = [
    { key: 'All',    label: 'All',   chip: '' },
    { key: 'red',    label: '紅碟 $12', chip: 'chip-red' },
    { key: 'silver', label: '銀碟 $17', chip: 'chip-silver' },
    { key: 'gold',   label: '金碟 $22', chip: 'chip-gold' },
    { key: 'black',  label: '黑碟 $27', chip: 'chip-black' },
    { key: 'white',  label: '白碟 海鮮價', chip: 'chip-white' },
  ];

  container.innerHTML = plates.map(p => `
    <button class="plate-tab ${state.activePlate === p.key ? 'active' : ''}" data-plate="${p.key}">
      ${p.chip ? `<span class="plate-chip ${p.chip}"></span>` : ''}
      ${p.label}
    </button>
  `).join('');

  container.querySelectorAll('.plate-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      state.activePlate = btn.dataset.plate;
      renderPlateFilters();
      renderMenuGrid();
    });
  });
}

function renderCategories() {
  const container = document.getElementById('category-tabs');
  const categories = getCategories();
  container.innerHTML = categories.map(cat => `
    <button class="category-tab ${state.activeCategory === cat ? 'active' : ''}" 
            data-category="${cat}">
      ${cat}
    </button>
  `).join('');

  container.querySelectorAll('.category-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      state.activeCategory = btn.dataset.category;
      renderCategories();
      renderMenuGrid();
    });
  });
}

function renderMenuGrid() {
  const grid = document.getElementById('menu-grid');
  const emptyState = document.getElementById('empty-state');
  const items = getFilteredItems();

  if (items.length === 0) {
    grid.style.display = 'none';
    emptyState.style.display = 'block';
    return;
  }

  grid.style.display = 'grid';
  emptyState.style.display = 'none';

  grid.innerHTML = items.map(item => {
    const qty = getItemQty(item.id);
    const hasQty = qty > 0;
    const imageHtml = item.imageUrl
      ? `<div class="card-image-wrapper"><img class="card-image" src="${item.imageUrl}" alt="${item.title}" loading="lazy" onerror="this.parentElement.outerHTML='<div class=\\'card-image-placeholder\\'>${getEmoji(item.category)}</div>'" /></div>`
      : `<div class="card-image-placeholder">${getEmoji(item.category)}</div>`;

    const plate = getPlateInfo(item.price);
    const plateHtml = plate
      ? `<span class="plate-badge plate-${plate.color}" title="${plate.labelEn}">${plate.label}</span>`
      : '';

    return `
      <div class="menu-card ${hasQty ? 'selected' : ''}" data-id="${item.id}">
        ${imageHtml}
        <div class="card-body">
          <div class="card-category-row">
            <span class="card-category">${item.category || ''}</span>
            ${plateHtml}
          </div>
          <div class="card-title">${item.title}</div>
          ${item.description ? `<div class="card-desc">${item.description}</div>` : ''}
          <div class="card-footer">
            <div class="card-price">${item.priceLabel || formatPrice(item.price)}</div>
            ${hasQty ? `
              <div class="qty-control">
                <button class="qty-btn minus" data-id="${item.id}" data-action="minus">−</button>
                <span class="qty-value has-items">${qty}</span>
                <button class="qty-btn plus" data-id="${item.id}" data-action="plus">+</button>
              </div>
            ` : `
              <button class="add-btn" data-id="${item.id}" data-action="add">+ Add</button>
            `}
          </div>
        </div>
      </div>
    `;
  }).join('');

  // Event delegation for buttons
  grid.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.dataset.id;
      const action = btn.dataset.action;
      const currentQty = getItemQty(id);
      if (action === 'add' || action === 'plus') {
        setItemQty(id, currentQty + 1);
      } else if (action === 'minus') {
        setItemQty(id, currentQty - 1);
      }
    });
  });
}

function updateCartUI() {
  const totalItems = getTotalItems();
  const totalPrice = getTotalPrice();

  // Badge
  document.getElementById('badge-count').textContent = totalItems;

  // Floating cart
  const floatingCart = document.getElementById('floating-cart');
  if (totalItems > 0) {
    floatingCart.style.display = 'flex';
    document.getElementById('cart-items-count').textContent = `${totalItems} item${totalItems > 1 ? 's' : ''}`;
    document.getElementById('cart-total').textContent = formatPrice(totalPrice);
  } else {
    floatingCart.style.display = 'none';
  }
}

function updateUI() {
  renderMenuGrid();
  updateCartUI();
}

// ===== Bill Modal =====
function openBillModal() {
  const modal = document.getElementById('bill-modal');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  renderBill();
}

function closeBillModal() {
  const modal = document.getElementById('bill-modal');
  modal.style.display = 'none';
  document.body.style.overflow = '';
}

function renderBill() {
  const cartItems = getCartItems();
  const totalItems = getTotalItems();
  const totalPrice = getTotalPrice();

  // Bill items
  const billItemsEl = document.getElementById('bill-items');
  if (cartItems.length === 0) {
    billItemsEl.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:20px;">No items added yet</p>';
  } else {
    billItemsEl.innerHTML = cartItems.map(item => {
      const plate = getPlateInfo(item.price);
      const plateTag = plate ? `<span class="plate-dot plate-${plate.color}"></span>` : '';
      return `
      <div class="bill-item">
        <div class="bill-item-info">
          <div class="bill-item-title">${plateTag}${item.title}</div>
          <div class="bill-item-meta">${item.priceLabel || formatPrice(item.price)} \u00d7 ${item.qty}</div>
        </div>
        <div class="qty-control">
          <button class="qty-btn minus" data-id="${item.id}" data-action="bill-minus">−</button>
          <span class="qty-value has-items">${item.qty}</span>
          <button class="qty-btn plus" data-id="${item.id}" data-action="bill-plus">+</button>
        </div>
        <div class="bill-item-total">${formatPrice(item.price * item.qty)}</div>
      </div>
    `}).join('');

    billItemsEl.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.id;
        const action = btn.dataset.action;
        const currentQty = getItemQty(id);
        if (action === 'bill-plus') {
          setItemQty(id, currentQty + 1);
        } else if (action === 'bill-minus') {
          setItemQty(id, currentQty - 1);
        }
        renderBill();
      });
    });
  }

  // Totals
  document.getElementById('bill-total-items').textContent = totalItems;
  document.getElementById('bill-total-amount').textContent = formatPrice(totalPrice);

  // Split
  const perPerson = state.splitCount > 0 ? totalPrice / state.splitCount : totalPrice;
  document.getElementById('split-count').textContent = state.splitCount;
  document.getElementById('split-price').textContent = formatPrice(Math.ceil(perPerson));

  // Custom split
  renderPersonList();
}

function renderPersonList() {
  const container = document.getElementById('person-list');
  if (!state.customSplit) {
    container.style.display = 'none';
    return;
  }
  container.style.display = 'flex';

  const cartItems = getCartItems();

  // Ensure personNames and personItems match splitCount
  while (state.personNames.length < state.splitCount) {
    state.personNames.push(`Person ${state.personNames.length + 1}`);
  }
  state.personNames = state.personNames.slice(0, state.splitCount);

  for (let i = 0; i < state.splitCount; i++) {
    if (!state.personItems[i]) state.personItems[i] = {};
  }

  container.innerHTML = Array.from({ length: state.splitCount }, (_, i) => {
    const personTotal = cartItems.reduce((sum, item) => {
      const pQty = state.personItems[i]?.[item.id] || 0;
      return sum + item.price * pQty;
    }, 0);

    return `
      <div class="person-card">
        <div class="person-header">
          <input class="person-name-input" type="text" value="${state.personNames[i]}" 
                 data-person="${i}" placeholder="Name" />
          <span class="person-total">${formatPrice(personTotal)}</span>
        </div>
        <div class="person-items">
          ${cartItems.map(item => {
            const pQty = state.personItems[i]?.[item.id] || 0;
            return `
              <div class="person-item-row">
                <label>
                  <span>${item.title}</span>
                </label>
                <input type="number" min="0" max="${item.qty}" value="${pQty}"
                       data-person="${i}" data-item="${item.id}" />
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }).join('');

  // Events
  container.querySelectorAll('.person-name-input').forEach(input => {
    input.addEventListener('input', (e) => {
      state.personNames[parseInt(e.target.dataset.person)] = e.target.value;
    });
  });

  container.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('change', (e) => {
      const personIdx = parseInt(e.target.dataset.person);
      const itemId = e.target.dataset.item;
      const val = Math.max(0, parseInt(e.target.value) || 0);
      if (!state.personItems[personIdx]) state.personItems[personIdx] = {};
      state.personItems[personIdx][itemId] = val;
      renderPersonList();
    });
  });
}

// ===== Copy Summary =====
function copySummary() {
  const cartItems = getCartItems();
  const totalPrice = getTotalPrice();
  const totalItems = getTotalItems();

  let text = '\ud83c\udf63 Who Ate The Sushi\n';
  text += '\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n';
  cartItems.forEach(item => {
    const plate = getPlateInfo(item.price);
    const plateLabel = plate ? `[${plate.label}]` : '';
    text += `${item.title} ${plateLabel} \u00d7${item.qty}  ${formatPrice(item.price * item.qty)}\n`;
  });
  text += '\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n';
  text += `Total: ${totalItems} items \u2014 ${formatPrice(totalPrice)}\n`;

  if (state.splitCount > 1) {
    const perPerson = Math.ceil(totalPrice / state.splitCount);
    text += `\nSplit ${state.splitCount} ways: ${formatPrice(perPerson)} each\n`;
  }

  if (state.customSplit) {
    text += '\n--- Per Person ---\n';
    for (let i = 0; i < state.splitCount; i++) {
      const personTotal = cartItems.reduce((sum, item) => {
        const pQty = state.personItems[i]?.[item.id] || 0;
        return sum + item.price * pQty;
      }, 0);
      if (personTotal > 0) {
        text += `${state.personNames[i]}: ${formatPrice(personTotal)}\n`;
        cartItems.forEach(item => {
          const pQty = state.personItems[i]?.[item.id] || 0;
          if (pQty > 0) {
            text += `  ${item.title} ×${pQty}\n`;
          }
        });
      }
    }
  }

  navigator.clipboard.writeText(text).then(() => {
    showToast('Bill summary copied!');
  }).catch(() => {
    // Fallback
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('Bill summary copied!');
  });
}

function showToast(message) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2500);
}

// ===== Clear All =====
function clearAll() {
  if (getTotalItems() === 0) return;
  if (confirm('Clear all items from your order?')) {
    state.cart = {};
    state.personItems = {};
    updateUI();
    showToast('Order cleared');
  }
}

// ===== Init =====
function init() {
  // Render
  renderPlateFilters();
  renderCategories();
  renderMenuGrid();
  updateCartUI();

  // Search
  document.getElementById('search-input').addEventListener('input', (e) => {
    state.searchQuery = e.target.value;
    renderMenuGrid();
  });

  // Header buttons
  document.getElementById('btn-clear').addEventListener('click', clearAll);
  document.getElementById('btn-bill').addEventListener('click', openBillModal);
  document.getElementById('btn-view-bill').addEventListener('click', openBillModal);

  // Modal
  document.getElementById('btn-close-modal').addEventListener('click', closeBillModal);
  document.getElementById('btn-done-modal').addEventListener('click', closeBillModal);
  document.getElementById('bill-modal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) closeBillModal();
  });

  // Split controls
  document.getElementById('split-minus').addEventListener('click', () => {
    if (state.splitCount > 1) {
      state.splitCount--;
      renderBill();
    }
  });
  document.getElementById('split-plus').addEventListener('click', () => {
    if (state.splitCount < 20) {
      state.splitCount++;
      renderBill();
    }
  });

  // Custom split toggle
  document.getElementById('toggle-custom-split').addEventListener('change', (e) => {
    state.customSplit = e.target.checked;
    renderPersonList();
  });

  // Copy summary
  document.getElementById('btn-share').addEventListener('click', copySummary);

  // Keyboard shortcut: Escape to close modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeBillModal();
  });
}

document.addEventListener('DOMContentLoaded', init);
