<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Ventas</h1>
        <p class="text-gray-600 mt-2">Gestiona las ventas y transacciones</p>
      </div>
      
      <div class="card">
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Módulo de Ventas</h3>
          <p class="mt-1 text-sm text-gray-500">Este módulo se encuentra en desarrollo</p>
          <div class="mt-6">
            <button type="button" class="btn-primary">
              Próximamente
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '../components/AppNavigation.vue'

export default {
  name: 'VentasView',
  components: {
    AppNavigation
  }
}
</script>