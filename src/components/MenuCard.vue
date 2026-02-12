<script setup lang="ts">
import { computed } from 'vue'
import type { MenuItem } from '../types'
import { useCart, getPlateInfo, getEmoji } from '../composables/useCart'

const props = defineProps<{ item: MenuItem }>()

const { getItemQty, addItem, removeItem, formatPrice } = useCart()

const qty = computed(() => getItemQty(props.item.id))
const hasQty = computed(() => qty.value > 0)
const plate = computed(() => getPlateInfo(props.item.price))
const emoji = computed(() => getEmoji(props.item.category))

const plateBadgeClass = computed(() => {
  if (!plate.value) return ''
  const map: Record<string, string> = {
    red: 'bg-plate-red-bg text-plate-red border border-plate-red-border',
    silver: 'bg-plate-silver-bg text-plate-silver border border-plate-silver-border',
    gold: 'bg-plate-gold-bg text-[#b45309] border border-plate-gold-border',
    black: 'bg-plate-black-bg text-gray-50 border border-plate-black-border',
    white: 'bg-plate-white-bg text-plate-white border border-plate-white-border',
  }
  return map[plate.value.color] || ''
})
</script>

<template>
  <div
    :class="[
      'bg-white rounded-xl border overflow-hidden transition-all flex flex-col',
      hasQty
        ? 'border-primary shadow-[0_0_0_2px_var(--color-primary-light)]'
        : 'border-border hover:shadow-md hover:-translate-y-0.5',
    ]"
  >
    <!-- Image -->
    <div v-if="item.imageUrl" class="card-image-wrapper relative w-full h-40 overflow-hidden bg-border-light">
      <img
        :src="item.imageUrl"
        :alt="item.title"
        loading="lazy"
        class="card-image w-full h-full object-cover transition-all duration-300"
        @error="($event.target as HTMLImageElement).parentElement!.outerHTML = `<div class='w-full h-40 shrink-0 bg-gradient-to-br from-primary-light to-amber-100 flex items-center justify-center text-5xl'>${emoji}</div>`"
      />
    </div>
    <div v-else class="w-full h-40 shrink-0 bg-gradient-to-br from-primary-light to-amber-100 flex items-center justify-center text-5xl">
      {{ emoji }}
    </div>

    <!-- Body -->
    <div class="p-3.5 flex-1 flex flex-col">
      <div class="flex items-center justify-between mb-1 gap-1.5">
        <span class="text-[0.7rem] font-semibold uppercase tracking-wider text-primary">
          {{ item.category }}
        </span>
        <span
          v-if="plate"
          :class="['inline-flex items-center gap-1 text-[0.65rem] font-bold px-2 py-0.5 rounded-full whitespace-nowrap tracking-wide', plateBadgeClass]"
        >
          {{ plate.label }}
        </span>
      </div>

      <div class="text-[0.95rem] font-semibold text-text mb-1 leading-tight">{{ item.title }}</div>
      <div v-if="item.description" class="text-xs text-text-secondary mb-2.5 flex-1 line-clamp-2">
        {{ item.description }}
      </div>

      <div class="flex items-center justify-between mt-auto">
        <div class="text-lg font-bold text-primary">{{ item.priceLabel || formatPrice(item.price) }}</div>

        <!-- Qty control -->
        <div v-if="hasQty" class="flex items-center rounded-lg overflow-hidden border border-border">
          <button
            @click="removeItem(item.id)"
            class="w-8 h-8 flex items-center justify-center border-none bg-border-light text-text text-lg font-semibold cursor-pointer transition-all hover:bg-primary-light hover:text-primary active:scale-95 border-r border-border"
          >−</button>
          <span class="min-w-8 text-center text-sm font-semibold text-primary px-1">{{ qty }}</span>
          <button
            @click="addItem(item.id)"
            class="w-8 h-8 flex items-center justify-center border-none bg-border-light text-text text-lg font-semibold cursor-pointer transition-all hover:bg-primary-light hover:text-primary active:scale-95 border-l border-border"
          >+</button>
        </div>

        <!-- Add button -->
        <button
          v-else
          @click="addItem(item.id)"
          class="px-4 py-1.5 rounded-lg border border-primary bg-white text-primary text-sm font-semibold cursor-pointer transition-all hover:bg-primary hover:text-white"
        >
          + Add
        </button>
      </div>
    </div>
  </div>
</template>
