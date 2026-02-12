import { reactive, computed } from 'vue'
import type { MenuItem, CartItem, PlateColor, PlateInfo } from '../types'
import { SUSHIRO_MENU } from '../data/menu'

// ===== Plate Config =====
const PLATE_COLORS: PlateInfo[] = [
  { max: 12, color: 'red', label: '紅碟', labelEn: 'Red Plate' },
  { max: 17, color: 'silver', label: '銀碟', labelEn: 'Silver Plate' },
  { max: 22, color: 'gold', label: '金碟', labelEn: 'Gold Plate' },
  { max: 27, color: 'black', label: '黑碟', labelEn: 'Black Plate' },
]

export function getPlateForPrice(price: number): PlateColor | null {
  if (!price || price <= 0) return null
  if (price <= 12) return 'red'
  if (price <= 17) return 'silver'
  if (price <= 22) return 'gold'
  if (price <= 27) return 'black'
  return 'white'
}

export function getPlateInfo(price: number): PlateInfo | null {
  if (!price || price <= 0) return null
  for (const plate of PLATE_COLORS) {
    if (price <= plate.max) return plate
  }
  return { color: 'white', label: '白碟', labelEn: 'White Plate', max: Infinity }
}

// ===== Category Emojis =====
const categoryEmojis: Record<string, string> = {
  Nigiri: '🍣',
  Sashimi: '🐟',
  Maki: '🍙',
  Roll: '🍙',
  Gunkan: '🍣',
  Udon: '🍜',
  Ramen: '🍜',
  Side: '🥟',
  Dessert: '🍮',
  Drink: '🥤',
  Promotional: '⭐',
  default: '🍽️',
}

export function getEmoji(category: string): string {
  for (const [key, emoji] of Object.entries(categoryEmojis)) {
    if (key !== 'default' && category && category.toLowerCase().includes(key.toLowerCase())) {
      return emoji
    }
  }
  return categoryEmojis.default ?? '🍽️'
}

// ===== State =====
const state = reactive({
  cart: {} as Record<string, number>,
  searchQuery: '',
  activePlate: 'All' as string,
  activeCategory: 'All' as string,
  splitCount: 2,
  customSplit: false,
  personNames: ['Person 1', 'Person 2'] as string[],
  personItems: {} as Record<number, Record<string, number>>,
  showBillModal: false,
  toastMessage: '',
  toastVisible: false,
})

let toastTimer: ReturnType<typeof setTimeout> | null = null

export function useCart() {
  // ===== Computed =====
  const menu = computed(() => SUSHIRO_MENU)

  const categories = computed(() => {
    const cats = new Set(SUSHIRO_MENU.map((item) => item.category))
    return ['All', ...Array.from(cats).sort()]
  })

  const filteredItems = computed(() => {
    let items = SUSHIRO_MENU as MenuItem[]
    if (state.activePlate !== 'All') {
      items = items.filter((i) => getPlateForPrice(i.price) === state.activePlate)
    }
    if (state.activeCategory !== 'All') {
      items = items.filter((i) => i.category === state.activeCategory)
    }
    if (state.searchQuery.trim()) {
      const q = state.searchQuery.toLowerCase()
      items = items.filter(
        (i) =>
          (i.title && i.title.toLowerCase().includes(q)) ||
          (i.description && i.description.toLowerCase().includes(q)) ||
          (i.category && i.category.toLowerCase().includes(q)),
      )
    }
    return items
  })

  const cartItems = computed<CartItem[]>(() => {
    const items: CartItem[] = []
    for (const [id, qty] of Object.entries(state.cart)) {
      if (qty > 0) {
        const item = SUSHIRO_MENU.find((m) => String(m.id) === String(id))
        if (item) items.push({ ...item, qty })
      }
    }
    return items
  })

  const totalItems = computed(() =>
    Object.values(state.cart).reduce((sum, q) => sum + q, 0),
  )

  const totalPrice = computed(() =>
    cartItems.value.reduce((sum, item) => sum + item.price * item.qty, 0),
  )

  const perPersonPrice = computed(() => {
    if (state.splitCount <= 0) return totalPrice.value
    return Math.ceil(totalPrice.value / state.splitCount)
  })

  // ===== Actions =====
  function formatPrice(amount: number): string {
    return `HK$${amount.toFixed(0)}`
  }

  function getItemQty(id: number): number {
    return state.cart[id] || 0
  }

  function setItemQty(id: number, qty: number) {
    if (qty <= 0) {
      delete state.cart[id]
    } else {
      state.cart[id] = qty
    }
  }

  function addItem(id: number) {
    setItemQty(id, getItemQty(id) + 1)
  }

  function removeItem(id: number) {
    setItemQty(id, getItemQty(id) - 1)
  }

  function clearAll() {
    state.cart = {}
    state.personItems = {}
  }

  function setSearchQuery(query: string) {
    state.searchQuery = query
  }

  function setActivePlate(plate: string) {
    state.activePlate = plate
  }

  function setActiveCategory(category: string) {
    state.activeCategory = category
  }

  function setSplitCount(count: number) {
    state.splitCount = Math.max(1, Math.min(20, count))
    // Sync person names
    while (state.personNames.length < state.splitCount) {
      state.personNames.push(`Person ${state.personNames.length + 1}`)
    }
    state.personNames = state.personNames.slice(0, state.splitCount)
  }

  function setCustomSplit(enabled: boolean) {
    state.customSplit = enabled
  }

  function setPersonName(index: number, name: string) {
    state.personNames[index] = name
  }

  function setPersonItemQty(personIndex: number, itemId: number, qty: number) {
    if (!state.personItems[personIndex]) {
      state.personItems[personIndex] = {}
    }
    state.personItems[personIndex][itemId] = Math.max(0, qty)
  }

  function getPersonItemQty(personIndex: number, itemId: number): number {
    return state.personItems[personIndex]?.[itemId] || 0
  }

  function getPersonTotal(personIndex: number): number {
    return cartItems.value.reduce((sum, item) => {
      const pQty = state.personItems[personIndex]?.[item.id] || 0
      return sum + item.price * pQty
    }, 0)
  }

  function openBillModal() {
    state.showBillModal = true
  }

  function closeBillModal() {
    state.showBillModal = false
  }

  function showToast(message: string) {
    state.toastMessage = message
    state.toastVisible = true
    if (toastTimer) clearTimeout(toastTimer)
    toastTimer = setTimeout(() => {
      state.toastVisible = false
    }, 2500)
  }

  function copySummary() {
    const items = cartItems.value
    const total = totalPrice.value
    const totalCount = totalItems.value

    let text = '🍣 Who Ate The Sushi\n'
    text += '═══════════════════\n'
    items.forEach((item) => {
      const plate = getPlateInfo(item.price)
      const plateLabel = plate ? `[${plate.label}]` : ''
      text += `${item.title} ${plateLabel} ×${item.qty}  ${formatPrice(item.price * item.qty)}\n`
    })
    text += '═══════════════════\n'
    text += `Total: ${totalCount} items — ${formatPrice(total)}\n`

    if (state.splitCount > 1) {
      const pp = Math.ceil(total / state.splitCount)
      text += `\nSplit ${state.splitCount} ways: ${formatPrice(pp)} each\n`
    }

    if (state.customSplit) {
      text += '\n--- Per Person ---\n'
      for (let i = 0; i < state.splitCount; i++) {
        const personTotal = getPersonTotal(i)
        if (personTotal > 0) {
          text += `${state.personNames[i]}: ${formatPrice(personTotal)}\n`
          items.forEach((item) => {
            const pQty = state.personItems[i]?.[item.id] || 0
            if (pQty > 0) {
              text += `  ${item.title} ×${pQty}\n`
            }
          })
        }
      }
    }

    navigator.clipboard
      .writeText(text)
      .then(() => showToast('Bill summary copied!'))
      .catch(() => {
        // Fallback
        const textarea = document.createElement('textarea')
        textarea.value = text
        document.body.appendChild(textarea)
        textarea.select()
        document.execCommand('copy')
        document.body.removeChild(textarea)
        showToast('Bill summary copied!')
      })
  }

  return {
    state,
    menu,
    categories,
    filteredItems,
    cartItems,
    totalItems,
    totalPrice,
    perPersonPrice,
    formatPrice,
    getItemQty,
    setItemQty,
    addItem,
    removeItem,
    clearAll,
    setSearchQuery,
    setActivePlate,
    setActiveCategory,
    setSplitCount,
    setCustomSplit,
    setPersonName,
    setPersonItemQty,
    getPersonItemQty,
    getPersonTotal,
    openBillModal,
    closeBillModal,
    showToast,
    copySummary,
  }
}
