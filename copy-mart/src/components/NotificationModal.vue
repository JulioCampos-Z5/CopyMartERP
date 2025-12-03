<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 z-50 overflow-y-auto" @click.self="closeOnBackdrop && close()">
        <div class="flex min-h-screen items-center justify-center p-4">
          <!-- Overlay -->
          <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>
          
          <!-- Modal -->
          <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-auto z-10 transform transition-all">
            <!-- Icon and Header -->
            <div class="p-6">
              <div class="flex items-center justify-center mb-4">
                <!-- Success Icon -->
                <div v-if="type === 'success'" class="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
                  <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <!-- Error Icon -->
                <div v-else-if="type === 'error'" class="h-12 w-12 rounded-full bg-red-100 flex items-center justify-center">
                  <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <!-- Warning Icon -->
                <div v-else-if="type === 'warning'" class="h-12 w-12 rounded-full bg-yellow-100 flex items-center justify-center">
                  <svg class="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <!-- Info Icon -->
                <div v-else class="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              
              <!-- Title -->
              <h3 class="text-lg font-medium text-gray-900 text-center mb-2">
                {{ title }}
              </h3>
              
              <!-- Message -->
              <p class="text-sm text-gray-500 text-center">
                {{ message }}
              </p>
            </div>
            
            <!-- Actions -->
            <div class="bg-gray-50 px-6 py-3 flex justify-center rounded-b-lg">
              <button
                @click="close"
                :class="buttonClass"
                class="px-4 py-2 text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors"
              >
                {{ buttonText }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  name: 'NotificationModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    title: {
      type: String,
      default: 'Notificación'
    },
    message: {
      type: String,
      default: ''
    },
    buttonText: {
      type: String,
      default: 'Aceptar'
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  computed: {
    buttonClass() {
      const classes = {
        success: 'bg-green-600 hover:bg-green-700 text-white focus:ring-green-500',
        error: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
        warning: 'bg-yellow-600 hover:bg-yellow-700 text-white focus:ring-yellow-500',
        info: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500'
      }
      return classes[this.type] || classes.info
    }
  },
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}
</style>
