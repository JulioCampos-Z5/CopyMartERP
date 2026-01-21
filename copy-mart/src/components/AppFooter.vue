<template>
  <footer class="fixed bottom-0 left-0 right-0 z-40">
    <!-- Base footer bar -->
    <div class="bg-gray-100 border-t border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex items-center justify-between">
        <p class="text-xs text-gray-500">CopyMart ERP · © {{ new Date().getFullYear() }}</p>
        <slot name="footer-actions"></slot>
      </div>
    </div>

    <!-- Global centered modal overlay -->
    <transition name="fade">
      <div v-if="modalState.visible" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset-0 bg-black bg-opacity-40" @click="modalState.type === 'confirm' ? onCancel() : hideModal()" aria-hidden="true"></div>
        <div :class="containerClass" role="dialog" aria-modal="true" class="relative max-w-lg w-[90%]">
          <div class="flex items-start gap-3">
            <span :class="iconClass" class="inline-flex items-center justify-center w-8 h-8 rounded-full">
              <svg v-if="modalState.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else-if="modalState.type === 'error'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 20a8 8 0 100-16 8 8 0 000 16z" />
              </svg>
            </span>
            <div class="flex-1">
              <p class="text-base font-semibold" :class="titleClass">{{ modalState.title }}</p>
              <p class="text-sm mt-1 whitespace-pre-line" :class="messageClass">{{ modalState.message }}</p>
            </div>
            <button @click="modalState.type === 'confirm' ? onCancel() : hideModal()" class="text-gray-400 hover:text-gray-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div v-if="modalState.type === 'confirm'" class="mt-4 flex justify-end gap-2">
            <button @click="onCancel" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">{{ modalState.cancelText }}</button>
            <button @click="onConfirm" class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">{{ modalState.confirmText }}</button>
          </div>
        </div>
      </div>
    </transition>
  </footer>
</template>

<script>
import { computed } from 'vue'
import { useModalBus } from '@/composables/useModalBus.ts'

export default {
  name: 'AppFooter',
  setup() {
    const { modalState, hideModal, onConfirm, onCancel } = useModalBus()

    const containerClass = computed(() => {
      switch (modalState.type) {
        case 'success': return 'bg-green-50 border border-green-200 rounded-lg p-4 shadow-lg'
        case 'error': return 'bg-red-50 border border-red-200 rounded-lg p-4 shadow-lg'
        case 'warning': return 'bg-yellow-50 border border-yellow-200 rounded-lg p-4 shadow-lg'
        default: return 'bg-gray-50 border border-gray-200 rounded-lg p-4 shadow-lg'
      }
    })
    const iconClass = computed(() => {
      switch (modalState.type) {
        case 'success': return 'bg-green-100 text-green-700'
        case 'error': return 'bg-red-100 text-red-700'
        case 'warning': return 'bg-yellow-100 text-yellow-700'
        default: return 'bg-gray-100 text-gray-700'
      }
    })
    const titleClass = computed(() => {
      switch (modalState.type) {
        case 'success': return 'text-green-800'
        case 'error': return 'text-red-800'
        case 'warning': return 'text-yellow-800'
        default: return 'text-gray-800'
      }
    })
    const messageClass = computed(() => {
      switch (modalState.type) {
        case 'success': return 'text-green-700'
        case 'error': return 'text-red-700'
        case 'warning': return 'text-yellow-700'
        default: return 'text-gray-700'
      }
    })

    return { modalState, hideModal, onConfirm, onCancel, containerClass, iconClass, titleClass, messageClass }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
