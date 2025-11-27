<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-rose-50 p-6 rounded-lg border border-rose-200">
        <h1 class="text-3xl font-bold text-rose-800 mb-2">Atención a Clientes</h1>
        <p class="text-rose-600">Centro de soporte y gestión de la experiencia del cliente</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-rose-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Tickets Abiertos</h3>
              <p class="text-2xl font-semibold text-gray-900">23</p>
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
              <h3 class="text-sm font-medium text-gray-500">Tiempo Promedio</h3>
              <p class="text-2xl font-semibold text-gray-900">2.4h</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m-5-14V3a2 2 0 012-2h2a2 2 0 012 2v1h6v20H7V4h2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Satisfacción</h3>
              <p class="text-2xl font-semibold text-gray-900">4.7/5</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Resueltos Hoy</h3>
              <p class="text-2xl font-semibold text-gray-900">18</p>
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
            Nuevo Ticket
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Chat en Vivo
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            Seguimiento Telefónico
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Tickets Recientes -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Tickets de Soporte</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ticket #</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Asunto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Prioridad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Agente</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#T-2025-001</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Empresa ABC</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Problema con impresora</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Alta</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">En Progreso</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Ana García</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#T-2025-002</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Hotel Plaza</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Consulta de precios</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Baja</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">Nuevo</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Luis Martín</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#T-2025-003</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Constructora XYZ</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Facturación incorrecta</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Media</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Resuelto</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Carmen Ruiz</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Soporte -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Centro de Soporte</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 class="text-sm font-medium text-red-800 mb-2">Tickets Críticos</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">#T-001 - Empresa ABC</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Atender</button>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">#T-007 - Hospital San José</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Atender</button>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Chat en Vivo</h4>
                <div class="flex items-center">
                  <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span class="text-sm text-green-700">3 conversaciones activas</span>
                </div>
                <div class="mt-2 space-y-1 text-xs text-green-600">
                  <div>• Cliente: ¿Tienen papel A3?</div>
                  <div>• Cliente: Problema con pedido #123</div>
                  <div>• Cliente: Horarios de entrega</div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Métricas de Rendimiento</h4>
                <div class="space-y-1 text-sm text-blue-700">
                  <div class="flex justify-between">
                    <span>Tiempo de Respuesta:</span>
                    <span>12 min</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Primera Resolución:</span>
                    <span>78%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Tickets Cerrados:</span>
                    <span>18/23</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 mb-2">Agentes Activos</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Ana García</span>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Disponible</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Luis Martín</span>
                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Ocupado</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Carmen Ruiz</span>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Disponible</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'

export default {
  name: 'AtencionClientesView',
  components: {
    BaseLayout
  }
}
</script>