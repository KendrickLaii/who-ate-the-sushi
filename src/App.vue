<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import FilterBar from './components/FilterBar.vue'
import MenuGrid from './components/MenuGrid.vue'
import FloatingCart from './components/FloatingCart.vue'
import BillModal from './components/BillModal.vue'
import ToastNotification from './components/ToastNotification.vue'
</script>

<template>
  <div id="app-root" class="min-h-screen">
    <AppHeader />
    <FilterBar />
    <MenuGrid />
    <FloatingCart />
    <BillModal />
    <ToastNotification />
  </div>
</template>
