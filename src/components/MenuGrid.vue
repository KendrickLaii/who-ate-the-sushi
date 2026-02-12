<script setup lang="ts">
import { Search } from 'lucide-vue-next'
import { useCart } from '../composables/useCart'
import MenuCard from './MenuCard.vue'

const { filteredItems } = useCart()
</script>

<template>
  <main class="max-w-[1200px] mx-auto p-5 pb-28">
    <div
      v-if="filteredItems.length > 0"
      class="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4 max-sm:grid-cols-[repeat(auto-fill,minmax(160px,1fr))] max-sm:gap-2.5"
    >
      <MenuCard v-for="item in filteredItems" :key="item.id" :item="item" />
    </div>
    <div v-else class="text-center py-16 text-text-muted">
      <Search :size="48" class="mx-auto mb-3 opacity-50" />
      <p class="text-base">No items found</p>
    </div>
  </main>
</template>
