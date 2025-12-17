<template>
  <div class="fixed bottom-4 right-4 z-50">
    <div 
      class="bg-white rounded-lg shadow-lg border-2 px-4 py-3 flex items-center space-x-3"
      :class="[
        apiStatus === 'connected' ? 'border-green-500' : '',
        apiStatus === 'disconnected' ? 'border-red-500' : '',
        apiStatus === 'checking' ? 'border-yellow-500' : ''
      ]"
    >
      <div class="text-right">
        <p class="text-xs font-semibold text-gray-700">Estado API</p>
        <p class="text-xs text-gray-500">{{ apiStatusText }}</p>
      </div>
      <div class="relative flex items-center justify-center w-8 h-8">
        <div 
          :class="[
            'w-4 h-4 rounded-full',
            apiStatus === 'connected' ? 'bg-green-500' : '',
            apiStatus === 'disconnected' ? 'bg-red-500' : '',
            apiStatus === 'checking' ? 'bg-yellow-500' : ''
          ]"
        >
          <span 
            v-if="apiStatus === 'connected'"
            class="absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75 animate-ping"
          ></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { API_BASE_URL } from '@/config/api'

export default {
  name: 'ApiStatus',
  setup() {
    const apiStatus = ref('checking') // 'checking', 'connected', 'disconnected'
    let intervalId = null
    
    const apiStatusText = computed(() => {
      switch (apiStatus.value) {
        case 'connected':
          return 'Conectado'
        case 'disconnected':
          return 'Desconectado'
        case 'checking':
          return 'Verificando...'
        default:
          return 'Desconocido'
      }
    })
    
    const checkApiStatus = async () => {
      try {
        apiStatus.value = 'checking'
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 segundos timeout
        
        const response = await fetch(API_BASE_URL, {
          signal: controller.signal
        })
        
        clearTimeout(timeoutId)
        
        if (response.ok) {
          apiStatus.value = 'connected'
        } else {
          apiStatus.value = 'disconnected'
        }
      } catch (error) {
        console.error('Error checking API status:', error)
        apiStatus.value = 'disconnected'
      }
    }
    
    onMounted(() => {
      checkApiStatus()
      // Verificar el estado cada 30 segundos
      intervalId = setInterval(checkApiStatus, 30000)
    })
    
    onUnmounted(() => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    })
    
    return {
      apiStatus,
      apiStatusText
    }
  }
}
</script>
