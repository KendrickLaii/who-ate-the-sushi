<script setup lang="ts">
import { Search } from 'lucide-vue-next'
import { useCart } from '../composables/useCart'

const { state, categories, setSearchQuery, setActivePlate, setActiveCategory } = useCart()

const plates = [
  { key: 'All', label: 'All', chipClass: '' },
  { key: 'red', label: '紅碟 $12', chipClass: 'bg-plate-red' },
  { key: 'silver', label: '銀碟 $17', chipClass: 'bg-plate-silver' },
  { key: 'gold', label: '金碟 $22', chipClass: 'bg-plate-gold' },
  { key: 'black', label: '黑碟 $27', chipClass: 'bg-plate-black' },
  { key: 'white', label: '白碟 海鮮價', chipClass: 'bg-plate-white-bg border border-text-muted' },
]
</script>

<template>
  <div class="bg-white border-b border-border sticky top-[53px] z-40">
    <div class="max-w-[1200px] mx-auto px-5 py-3 flex flex-col gap-2.5">
      <!-- Search -->
      <div
        class="flex items-center gap-2 bg-border-light rounded-lg px-3.5 py-2 border-2 border-transparent transition-all focus-within:border-primary focus-within:bg-white focus-within:shadow-[0_0_0_3px_var(--color-primary-light)]"
      >
        <Search :size="18" class="text-text-muted shrink-0" />
        <input
          type="text"
          :value="state.searchQuery"
          @input="setSearchQuery(($event.target as HTMLInputElement).value)"
          placeholder="Search menu items..."
          class="border-none bg-transparent outline-none text-sm w-full font-[inherit] text-text placeholder:text-text-muted"
        />
      </div>

      <!-- Plate Filter -->
      <div class="flex items-center gap-2">
        <span class="text-xs font-semibold text-text-muted whitespace-nowrap min-w-14">Plate:</span>
        <div class="flex gap-1.5 overflow-x-auto pb-1 hide-scrollbar">
          <button
            v-for="plate in plates"
            :key="plate.key"
            @click="setActivePlate(plate.key)"
            :class="[
              'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border cursor-pointer transition-all whitespace-nowrap',
              state.activePlate === plate.key
                ? 'border-primary bg-primary-light text-primary'
                : 'border-border bg-white text-text-secondary hover:border-text-secondary',
            ]"
          >
            <span
              v-if="plate.chipClass"
              :class="['inline-block w-2.5 h-2.5 rounded-full shrink-0', plate.chipClass]"
            />
            {{ plate.label }}
          </button>
        </div>
      </div>

      <!-- Category Filter -->
      <div class="flex items-center gap-2">
        <span class="text-xs font-semibold text-text-muted whitespace-nowrap min-w-14">Category:</span>
        <div class="flex gap-1.5 overflow-x-auto pb-1 hide-scrollbar">
          <button
            v-for="cat in categories"
            :key="cat"
            @click="setActiveCategory(cat)"
            :class="[
              'px-3.5 py-1.5 rounded-full text-xs font-medium border cursor-pointer transition-all whitespace-nowrap',
              state.activeCategory === cat
                ? 'bg-primary text-white border-primary'
                : 'bg-white text-text-secondary border-border hover:border-primary hover:text-primary',
            ]"
          >
            {{ cat }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
