<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-2">Bienvenido al sistema CopyMart ERP</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Clientes</p>
              <p class="text-2xl font-semibold text-gray-900">-</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Rentas Activas</p>
              <p class="text-2xl font-semibold text-gray-900">-</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Ventas del Mes</p>
              <p class="text-2xl font-semibold text-gray-900">-</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Facturas Vencidas</p>
              <p class="text-2xl font-semibold text-gray-900">-</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts & Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Recent Activity -->
        <div class="bg-white rounded-lg shadow-md">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Actividad Reciente</h2>
          </div>
          <div class="p-6">
            <p class="text-center text-gray-500 py-8">No hay actividad reciente</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow-md">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Acciones Rápidas</h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-2 gap-4">
              <router-link to="/clientes" class="flex flex-col items-center justify-center p-6 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
                <svg class="w-8 h-8 text-blue-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                <span class="text-sm font-medium text-gray-900">Nuevo Cliente</span>
              </router-link>

              <router-link to="/comercial/rentas" class="flex flex-col items-center justify-center p-6 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
                <svg class="w-8 h-8 text-green-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="text-sm font-medium text-gray-900">Nueva Renta</span>
              </router-link>

              <router-link to="/comercial/ventas" class="flex flex-col items-center justify-center p-6 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors">
                <svg class="w-8 h-8 text-yellow-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="text-sm font-medium text-gray-900">Nueva Venta</span>
              </router-link>

              <router-link to="/administracion/cobranza" class="flex flex-col items-center justify-center p-6 bg-red-50 rounded-lg hover:bg-red-100 transition-colors">
                <svg class="w-8 h-8 text-red-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <span class="text-sm font-medium text-gray-900">Ver Cobranza</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'

export default {
  name: 'DashboardView',
  components: {
    AppNavigation
  }
}
</script>
