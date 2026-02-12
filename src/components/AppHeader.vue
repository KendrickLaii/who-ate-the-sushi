<script setup lang="ts">
import { Trash2, FileText } from 'lucide-vue-next'
import { useCart } from '../composables/useCart'

const { totalItems, clearAll, openBillModal, showToast } = useCart()

function handleClear() {
  if (totalItems.value === 0) return
  if (confirm('Clear all items from your order?')) {
    clearAll()
    showToast('Order cleared')
  }
}
</script>

<template>
  <header class="bg-white border-b border-border sticky top-0 z-50 backdrop-blur-sm">
    <div class="max-w-[1200px] mx-auto px-5 py-3 flex items-center justify-between">
      <div class="flex items-baseline gap-2.5">
        <h1 class="text-2xl font-bold text-primary">🍣 Who Ate The Sushi</h1>
        <span class="text-sm text-text-secondary font-medium hidden sm:inline">
          I love Sushiro and I only want to pay my part.
        </span>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="handleClear"
          class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold border border-border bg-transparent text-text-secondary hover:bg-border-light hover:text-text transition-all cursor-pointer"
        >
          <Trash2 :size="18" />
          Clear
        </button>
        <button
          @click="openBillModal"
          class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold bg-primary text-white border-none hover:bg-primary-dark hover:-translate-y-px hover:shadow-md transition-all cursor-pointer"
        >
          <FileText :size="18" />
          Bill
          <span class="bg-white text-primary text-xs font-bold px-1.5 py-0.5 rounded-full min-w-5 text-center">
            {{ totalItems }}
          </span>
        </button>
      </div>
    </div>
  </header>
</template>
