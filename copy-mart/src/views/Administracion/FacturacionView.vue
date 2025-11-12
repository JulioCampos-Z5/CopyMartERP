<template>
  <AppNavigation>
    <div class="space-y-6">
      <!-- Header -->
      <div class="bg-orange-50 p-6 rounded-lg border border-orange-200">
        <h1 class="text-3xl font-bold text-orange-800 mb-2">Sistema de Facturación</h1>
        <p class="text-orange-600">Genera y administra facturas fiscales y no fiscales</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Facturas Hoy</h3>
              <p class="text-2xl font-semibold text-gray-900">24</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Total Facturado</h3>
              <p class="text-2xl font-semibold text-gray-900">$89,450</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">IVA del Mes</h3>
              <p class="text-2xl font-semibold text-gray-900">$14,312</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Timbradas</h3>
              <p class="text-2xl font-semibold text-gray-900">342</p>
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
            Nueva Factura
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2v0M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
            </svg>
            Nota de Crédito
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Consultar RFC
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Reporte SAT
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Facturas Recientes -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Facturas Recientes</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Folio</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">F001-123</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Empresa ABC S.A.</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$15,230.00</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Timbrada</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">12/11/2025</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">F001-124</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Hotel Plaza</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$8,950.00</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Pendiente</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">12/11/2025</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">F001-125</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Constructora XYZ</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$4,670.00</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Cancelada</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">11/11/2025</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Control SAT -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Control Fiscal</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Estado del PAC</h4>
                <div class="flex items-center">
                  <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span class="text-sm text-green-700">Conectado y Operativo</span>
                </div>
                <p class="text-xs text-green-600 mt-1">Último: 12/11/2025 14:32</p>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Folios Disponibles</h4>
                <div class="space-y-1 text-sm text-blue-700">
                  <div class="flex justify-between">
                    <span>Serie A:</span>
                    <span>850 folios</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Serie B:</span>
                    <span>1,200 folios</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                <h4 class="text-sm font-medium text-orange-800 mb-2">Próximo Vencimiento</h4>
                <p class="text-sm text-orange-700">Certificado: 15/12/2025</p>
                <p class="text-xs text-orange-600">Renovar en 33 días</p>
              </div>

              <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <h4 class="text-sm font-medium text-gray-800 mb-2">Resumen del Día</h4>
                <div class="space-y-1 text-sm text-gray-700">
                  <div class="flex justify-between">
                    <span>Timbradas:</span>
                    <span>24</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Canceladas:</span>
                    <span>2</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Pendientes:</span>
                    <span>3</span>
                  </div>
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
  name: 'FacturacionView',
  components: {
    AppNavigation
  }
}
</script>