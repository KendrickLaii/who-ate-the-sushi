<script setup lang="ts">
import { useCart } from '../composables/useCart'

const { totalItems, totalPrice, formatPrice, openBillModal } = useCart()
</script>

<template>
  <Transition name="cart">
    <div
      v-if="totalItems > 0"
      class="fixed bottom-5 left-1/2 -translate-x-1/2 bg-text text-white px-6 py-3 rounded-2xl flex items-center gap-5 shadow-xl z-40 min-w-80 animate-slide-up max-sm:left-3.5 max-sm:right-3.5 max-sm:translate-x-0 max-sm:min-w-0"
    >
      <div class="flex flex-col flex-1">
        <span class="text-xs text-text-muted">
          {{ totalItems }} item{{ totalItems > 1 ? 's' : '' }}
        </span>
        <span class="text-xl font-bold">{{ formatPrice(totalPrice) }}</span>
      </div>
      <button
        @click="openBillModal"
        class="bg-primary text-white px-6 py-3 rounded-lg text-base font-semibold border-none cursor-pointer transition-all hover:bg-primary-dark shrink-0"
      >
        View Bill →
      </button>
    </div>
  </Transition>
</template>
