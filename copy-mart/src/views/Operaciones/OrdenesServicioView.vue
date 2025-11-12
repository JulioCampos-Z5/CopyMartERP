<template>
  <AppNavigation>
    <div class="space-y-6">
      <!-- Header -->
      <div class="bg-cyan-50 p-6 rounded-lg border border-cyan-200">
        <h1 class="text-3xl font-bold text-cyan-800 mb-2">Órdenes de Servicio</h1>
        <p class="text-cyan-600">Gestión y seguimiento de órdenes de trabajo y mantenimiento</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-cyan-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Órdenes Abiertas</h3>
              <p class="text-2xl font-semibold text-gray-900">15</p>
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
              <h3 class="text-sm font-medium text-gray-500">Urgentes</h3>
              <p class="text-2xl font-semibold text-gray-900">4</p>
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
              <h3 class="text-sm font-medium text-gray-500">Completadas Hoy</h3>
              <p class="text-2xl font-semibold text-gray-900">8</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Eficiencia</h3>
              <p class="text-2xl font-semibold text-gray-900">87%</p>
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
            Nueva Orden
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Asignar Técnico
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Dashboard Técnicos
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Órdenes Activas -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Órdenes Activas</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Orden #</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Técnico</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Prioridad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#OS-2025-001</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Empresa ABC</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Mantenimiento</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Juan Pérez</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Alta</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">En Progreso</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#OS-2025-002</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Hotel Plaza</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Reparación</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">María López</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Media</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">Asignada</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#OS-2025-003</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Oficina Legal</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Instalación</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Carlos Ruiz</td>
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

        <!-- Panel de Control -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Control de Operaciones</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 class="text-sm font-medium text-red-800 mb-2">Órdenes Urgentes</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">#OS-001 - Empresa ABC</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Ver</button>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">#OS-005 - Hospital XYZ</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Ver</button>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Técnicos Disponibles</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-blue-700">Juan Pérez</span>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Disponible</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-blue-700">Ana García</span>
                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Ocupada</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-blue-700">Luis Martín</span>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Disponible</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Rendimiento del Día</h4>
                <div class="space-y-1 text-sm text-green-700">
                  <div class="flex justify-between">
                    <span>Completadas:</span>
                    <span>8</span>
                  </div>
                  <div class="flex justify-between">
                    <span>En Progreso:</span>
                    <span>6</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Tiempo Promedio:</span>
                    <span>2.5h</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <h4 class="text-sm font-medium text-gray-800 mb-2">Próximas Citas</h4>
                <div class="space-y-2 text-sm text-gray-700">
                  <div class="flex justify-between">
                    <span>14:00 - Mantenimiento</span>
                    <span class="text-blue-600">Juan P.</span>
                  </div>
                  <div class="flex justify-between">
                    <span>15:30 - Reparación</span>
                    <span class="text-green-600">Ana G.</span>
                  </div>
                  <div class="flex justify-between">
                    <span>16:15 - Instalación</span>
                    <span class="text-purple-600">Luis M.</span>
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
  name: 'OrdenesServicioView',
  components: {
    AppNavigation
  }
}
</script>