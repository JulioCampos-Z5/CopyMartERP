<template>
  <AppNavigation>
    <div class="space-y-6">
      <!-- Header -->
      <div class="bg-green-50 p-6 rounded-lg border border-green-200">
        <h1 class="text-3xl font-bold text-green-800 mb-2">Gestión de Compras</h1>
        <p class="text-green-600">Administra las adquisiciones y proveedores</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4l1-12z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Órdenes Pendientes</h3>
              <p class="text-2xl font-semibold text-gray-900">18</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Gasto del Mes</h3>
              <p class="text-2xl font-semibold text-gray-900">$67,890</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Proveedores Activos</h3>
              <p class="text-2xl font-semibold text-gray-900">42</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Órdenes Completadas</h3>
              <p class="text-2xl font-semibold text-gray-900">156</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <button class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Orden de Compra
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Gestionar Proveedores
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Reporte de Compras
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Órdenes Recientes -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Órdenes de Compra Recientes</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Orden #</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Proveedor</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#OC-2025-001</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Proveedor ABC</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$15,230</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Pendiente</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">12/11/2025</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#OC-2025-002</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Suministros XYZ</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$8,950</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Entregado</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">10/11/2025</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Proveedores -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Proveedores Principales</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Proveedor ABC S.A.</h4>
                  <p class="text-xs text-gray-500">Papel y suministros</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900">$34,500</p>
                  <p class="text-xs text-gray-500">Este mes</p>
                </div>
              </div>
              
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Tecnología XYZ</h4>
                  <p class="text-xs text-gray-500">Equipos y tecnología</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900">$28,900</p>
                  <p class="text-xs text-gray-500">Este mes</p>
                </div>
              </div>
              
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Servicios 123</h4>
                  <p class="text-xs text-gray-500">Servicios generales</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900">$12,400</p>
                  <p class="text-xs text-gray-500">Este mes</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppNavigation>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'

export default {
  name: 'ComprasView',
  components: {
    AppNavigation
  }
}
</script>