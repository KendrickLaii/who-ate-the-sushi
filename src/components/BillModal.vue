<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { X, Share2 } from 'lucide-vue-next'
import { useCart, getPlateInfo } from '../composables/useCart'

const {
  state,
  cartItems,
  totalItems,
  totalPrice,
  perPersonPrice,
  formatPrice,
  addItem,
  removeItem,
  closeBillModal,
  setSplitCount,
  setCustomSplit,
  setPersonName,
  setPersonItemQty,
  getPersonItemQty,
  getPersonTotal,
  copySummary,
} = useCart()

const plateDotClass: Record<string, string> = {
  red: 'bg-plate-red',
  silver: 'bg-plate-silver',
  gold: 'bg-plate-gold',
  black: 'bg-plate-black',
  white: 'bg-plate-white-bg border border-text-muted',
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') closeBillModal()
}

onMounted(() => document.addEventListener('keydown', handleKeydown))
onUnmounted(() => document.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <Teleport to="body">
    <div
      v-if="state.showBillModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[200] flex items-end sm:items-center justify-center animate-fade-in"
      @click.self="closeBillModal"
    >
      <div class="bg-white rounded-t-2xl sm:rounded-2xl w-full max-w-[560px] max-h-[90vh] sm:max-h-[80vh] sm:mb-10 flex flex-col animate-slide-up-modal">
        <!-- Header -->
        <div class="flex items-center justify-between px-6 pt-5 pb-3 border-b border-border">
          <h2 class="text-xl font-bold">🧾 Your Bill</h2>
          <button
            @click="closeBillModal"
            class="bg-transparent border-none cursor-pointer text-text-secondary p-1 rounded-lg transition-all hover:bg-border-light hover:text-text flex items-center"
          >
            <X :size="24" />
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto px-6 py-4">
          <!-- Bill Items -->
          <div class="flex flex-col gap-2.5 mb-4">
            <p v-if="cartItems.length === 0" class="text-center text-text-muted py-5">
              No items added yet
            </p>
            <div
              v-for="item in cartItems"
              :key="item.id"
              class="flex items-center gap-3 py-2.5 border-b border-border-light"
            >
              <div class="flex-1 min-w-0">
                <div class="text-sm font-semibold whitespace-nowrap overflow-hidden text-ellipsis flex items-center">
                  <span
                    v-if="getPlateInfo(item.price)"
                    :class="['inline-block w-2.5 h-2.5 rounded-full mr-1.5 shrink-0', plateDotClass[getPlateInfo(item.price)!.color]]"
                  />
                  {{ item.title }}
                </div>
                <div class="text-xs text-text-secondary">
                  {{ item.priceLabel || formatPrice(item.price) }} × {{ item.qty }}
                </div>
              </div>
              <div class="flex items-center rounded-lg overflow-hidden border border-border shrink-0">
                <button
                  @click="removeItem(item.id)"
                  class="w-8 h-8 flex items-center justify-center border-none bg-border-light text-text text-lg font-semibold cursor-pointer transition-all hover:bg-primary-light hover:text-primary"
                >−</button>
                <span class="min-w-8 text-center text-sm font-semibold text-primary px-1">{{ item.qty }}</span>
                <button
                  @click="addItem(item.id)"
                  class="w-8 h-8 flex items-center justify-center border-none bg-border-light text-text text-lg font-semibold cursor-pointer transition-all hover:bg-primary-light hover:text-primary"
                >+</button>
              </div>
              <div class="font-bold text-primary text-[0.95rem] whitespace-nowrap">
                {{ formatPrice(item.price * item.qty) }}
              </div>
            </div>
          </div>

          <!-- Total -->
          <div class="bg-border-light rounded-lg px-4 py-3.5 mb-5">
            <div class="flex justify-between items-center py-1 text-sm text-text-secondary">
              <span>Total Items</span>
              <span>{{ totalItems }}</span>
            </div>
            <div class="flex justify-between items-center pt-2.5 mt-1.5 border-t-2 border-border text-xl font-bold text-text">
              <span>Total</span>
              <span>{{ formatPrice(totalPrice) }}</span>
            </div>
          </div>

          <!-- Split Section -->
          <div class="border-t border-border pt-4">
            <h3 class="text-base font-bold mb-3">Split the Bill</h3>

            <div class="flex items-center justify-between mb-3.5">
              <label class="text-sm text-text-secondary">Number of people:</label>
              <div class="flex items-center rounded-lg overflow-hidden border border-border">
                <button
                  @click="setSplitCount(state.splitCount - 1)"
                  class="w-9 h-9 flex items-center justify-center border-none bg-border-light text-text text-xl font-semibold cursor-pointer transition-all hover:bg-primary-light hover:text-primary"
                >−</button>
                <span class="min-w-11 text-center text-base font-bold">{{ state.splitCount }}</span>
                <button
                  @click="setSplitCount(state.splitCount + 1)"
                  class="w-9 h-9 flex items-center justify-center border-none bg-border-light text-text text-xl font-semibold cursor-pointer transition-all hover:bg-primary-light hover:text-primary"
                >+</button>
              </div>
            </div>

            <div class="bg-primary-light rounded-lg px-4 py-3.5 mb-4">
              <div class="flex justify-between items-center">
                <span class="text-sm text-primary-dark">Per person</span>
                <span class="text-xl font-bold text-primary">{{ formatPrice(perPersonPrice) }}</span>
              </div>
            </div>

            <!-- Custom Split -->
            <div>
              <h4 class="text-sm font-semibold mb-2.5 text-text-secondary">Or assign items to each person</h4>
              <label class="flex items-center gap-2 cursor-pointer text-sm mb-3">
                <input
                  type="checkbox"
                  :checked="state.customSplit"
                  @change="setCustomSplit(($event.target as HTMLInputElement).checked)"
                  class="w-4.5 h-4.5 accent-primary"
                />
                <span>Custom split by person</span>
              </label>

              <div v-if="state.customSplit" class="flex flex-col gap-3">
                <div
                  v-for="(_, personIdx) in state.splitCount"
                  :key="personIdx"
                  class="bg-border-light rounded-lg px-3.5 py-3"
                >
                  <div class="flex justify-between items-center mb-2">
                    <input
                      type="text"
                      :value="state.personNames[personIdx]"
                      @input="setPersonName(personIdx, ($event.target as HTMLInputElement).value)"
                      placeholder="Name"
                      class="border border-border rounded-md px-2 py-1 text-sm font-semibold w-30 outline-none transition-all focus:border-primary focus:shadow-[0_0_0_2px_var(--color-primary-light)]"
                    />
                    <span class="font-bold text-primary text-[0.95rem]">
                      {{ formatPrice(getPersonTotal(personIdx)) }}
                    </span>
                  </div>
                  <div class="flex flex-col gap-1">
                    <div
                      v-for="item in cartItems"
                      :key="item.id"
                      class="flex items-center justify-between text-xs py-1"
                    >
                      <span class="whitespace-nowrap overflow-hidden text-ellipsis flex-1 min-w-0">
                        {{ item.title }}
                      </span>
                      <input
                        type="number"
                        :min="0"
                        :max="item.qty"
                        :value="getPersonItemQty(personIdx, item.id)"
                        @change="setPersonItemQty(personIdx, item.id, Math.max(0, parseInt(($event.target as HTMLInputElement).value) || 0))"
                        class="w-12 px-1 py-0.5 border border-border rounded text-center text-xs outline-none focus:border-primary"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-border flex gap-2.5 justify-end">
          <button
            @click="copySummary"
            class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold border border-border bg-transparent text-text-secondary hover:bg-border-light hover:text-text transition-all cursor-pointer"
          >
            <Share2 :size="18" />
            Copy Summary
          </button>
          <button
            @click="closeBillModal"
            class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold bg-primary text-white border-none hover:bg-primary-dark transition-all cursor-pointer"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
