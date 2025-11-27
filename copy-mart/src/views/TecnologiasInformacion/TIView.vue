<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-slate-50 p-6 rounded-lg border border-slate-200">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">Tecnologías de la Información</h1>
        <p class="text-slate-600">Centro de control y administración de sistemas tecnológicos</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Equipos Activos</h3>
              <p class="text-2xl font-semibold text-gray-900">84</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Incidencias Abiertas</h3>
              <p class="text-2xl font-semibold text-gray-900">7</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.25-4.5l2.25 2.25L13.5 15" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Uptime del Sistema</h3>
              <p class="text-2xl font-semibold text-gray-900">99.8%</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Respaldos Hoy</h3>
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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Incidencia
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Monitor de Sistemas
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
            Respaldos
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Configuración
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Incidencias Activas -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Incidencias de TI</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ticket #</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Prioridad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#TI-2025-001</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Impresora no responde</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">María López</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Media</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">En Progreso</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#TI-2025-002</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Error conexión red</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Carlos Ruiz</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Alta</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Crítica</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#TI-2025-003</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Actualizar software</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Ana García</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Baja</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Completada</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Monitoreo -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Estado del Sistema</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Servicios Activos</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700">Servidor Web</span>
                    <span class="text-xs bg-green-600 text-white px-2 py-1 rounded">Online</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700">Base de Datos</span>
                    <span class="text-xs bg-green-600 text-white px-2 py-1 rounded">Online</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700">Correo Electrónico</span>
                    <span class="text-xs bg-green-600 text-white px-2 py-1 rounded">Online</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Uso de Recursos</h4>
                <div class="space-y-3">
                  <div>
                    <div class="flex justify-between text-sm text-blue-700">
                      <span>CPU</span>
                      <span>45%</span>
                    </div>
                    <div class="w-full bg-blue-200 rounded-full h-2 mt-1">
                      <div class="bg-blue-600 h-2 rounded-full" style="width: 45%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm text-blue-700">
                      <span>RAM</span>
                      <span>67%</span>
                    </div>
                    <div class="w-full bg-blue-200 rounded-full h-2 mt-1">
                      <div class="bg-blue-600 h-2 rounded-full" style="width: 67%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm text-blue-700">
                      <span>Disco</span>
                      <span>23%</span>
                    </div>
                    <div class="w-full bg-blue-200 rounded-full h-2 mt-1">
                      <div class="bg-blue-600 h-2 rounded-full" style="width: 23%"></div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <h4 class="text-sm font-medium text-gray-800 mb-2">Últimos Respaldos</h4>
                <div class="space-y-2 text-sm text-gray-700">
                  <div class="flex justify-between">
                    <span>Base de Datos</span>
                    <span class="text-green-600">Hoy 02:00</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Archivos Sistema</span>
                    <span class="text-green-600">Hoy 03:00</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Configuraciones</span>
                    <span class="text-green-600">Ayer 23:00</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 mb-2">Mantenimiento Programado</h4>
                <div class="space-y-2 text-sm text-yellow-700">
                  <div>Actualización del servidor</div>
                  <div>📅 15/11/2025 - 02:00 AM</div>
                  <div>⏱️ Duración estimada: 30 min</div>
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
  name: 'TIView',
  components: {
    BaseLayout
  }
}
</script>