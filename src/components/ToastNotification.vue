<script setup lang="ts">
import { useCart } from '../composables/useCart'

const { state } = useCart()
</script>

<template>
  <Teleport to="body">
    <div
      v-if="state.toastVisible"
      class="fixed bottom-20 left-1/2 -translate-x-1/2 bg-text text-white px-5 py-2.5 rounded-lg text-sm font-medium z-[300] shadow-lg toast-enter"
    >
      {{ state.toastMessage }}
    </div>
  </Teleport>
</template>
