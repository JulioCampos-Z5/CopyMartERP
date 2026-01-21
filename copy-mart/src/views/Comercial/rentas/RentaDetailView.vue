<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Volver a Rentas
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Detalle de Renta</h1>
        <p class="text-gray-600 mt-2">Información completa del contrato de renta</p>
      </div>

      <!-- En construcción -->
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
        <svg class="w-16 h-16 text-yellow-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Vista en Desarrollo</h2>
        <p class="text-gray-600 mb-4">Esta vista está siendo desarrollada. ID: {{ rentId }}</p>
        <button @click="goBack" class="btn-primary">
          Volver a Rentas
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'

export default {
  name: 'RentaDetailView',
  components: {
    AppNavigation
  },
  data() {
    return {
      rentId: null
    }
  },
  mounted() {
    this.rentId = this.$route.params.id
  },
  methods: {
    goBack() {
      this.$router.push('/rentas')
    }
  }
}
</script>

<style scoped>
.btn-primary {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: #2563eb;
}
</style>
