<template>
  <AppNavigation>
    <div class="space-y-6">
      <!-- Header -->
      <div class="bg-indigo-50 p-6 rounded-lg border border-indigo-200">
        <h1 class="text-3xl font-bold text-indigo-800 mb-2">Gestión de Cobranza</h1>
        <p class="text-indigo-600">Administra las cuentas por cobrar y seguimiento de pagos</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Total por Cobrar</h3>
              <p class="text-2xl font-semibold text-gray-900">$127,890</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Facturas Vencidas</h3>
              <p class="text-2xl font-semibold text-gray-900">18</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Cobrado este Mes</h3>
              <p class="text-2xl font-semibold text-gray-900">$84,560</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Por Vencer (7 días)</h3>
              <p class="text-2xl font-semibold text-gray-900">12</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <button class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Registrar Pago
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Enviar Recordatorio
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Reporte de Antigüedad
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Facturas por Cobrar -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Facturas Pendientes de Cobro</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Factura #</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Días Vencida</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#F-2025-045</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Empresa ABC S.A.</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$15,230</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-red-600">15 días</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Vencida</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#F-2025-048</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Constructora XYZ</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$8,950</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-yellow-600">3 días</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Por Vencer</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#F-2025-051</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Oficina Legal 123</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">$4,670</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-green-600">15 días</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Vigente</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Gestión de Cobranza -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Acciones de Cobranza</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 class="text-sm font-medium text-red-800 mb-2">Críticas (>30 días)</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">Empresa ABC</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Llamar</button>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">Hotel Plaza</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Email</button>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 mb-2">Próximas a Vencer</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Constructora XYZ</span>
                    <button class="text-xs bg-yellow-600 text-white px-2 py-1 rounded">Recordar</button>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Oficina 456</span>
                    <button class="text-xs bg-yellow-600 text-white px-2 py-1 rounded">Recordar</button>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Estadísticas del Mes</h4>
                <div class="space-y-1 text-sm text-blue-700">
                  <div class="flex justify-between">
                    <span>Efectividad:</span>
                    <span>78%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Tiempo Promedio:</span>
                    <span>12 días</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Llamadas Realizadas:</span>
                    <span>45</span>
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
  name: 'CobranzaView',
  components: {
    AppNavigation
  }
}
</script>