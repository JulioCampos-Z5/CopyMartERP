<template>
  <AppNavigation>
    <div class="space-y-6">
      <!-- Header -->
      <div class="bg-emerald-50 p-6 rounded-lg border border-emerald-200">
        <h1 class="text-3xl font-bold text-emerald-800 mb-2">Gestión de Rutas</h1>
        <p class="text-emerald-600">Control y optimización de rutas de entrega y servicio</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Rutas Activas</h3>
              <p class="text-2xl font-semibold text-gray-900">12</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Entregas Hoy</h3>
              <p class="text-2xl font-semibold text-gray-900">28</p>
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
              <h3 class="text-sm font-medium text-gray-500">Entregas Pendientes</h3>
              <p class="text-2xl font-semibold text-gray-900">7</p>
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
              <h3 class="text-sm font-medium text-gray-500">Eficiencia</h3>
              <p class="text-2xl font-semibold text-gray-900">94%</p>
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
            Nueva Ruta
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Optimizar Rutas
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            </svg>
            Rastreo en Vivo
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Rutas del Día -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Rutas del Día</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ruta</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Conductor</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Paradas</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Progreso</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">R001 - Centro</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Luis González</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">8 paradas</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">En Ruta</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-16 bg-gray-200 rounded-full h-2">
                          <div class="bg-green-600 h-2 rounded-full" style="width: 75%"></div>
                        </div>
                        <span class="text-xs text-gray-500 ml-2">6/8</span>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">R002 - Norte</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">María Rodríguez</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">5 paradas</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Pausada</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-16 bg-gray-200 rounded-full h-2">
                          <div class="bg-yellow-600 h-2 rounded-full" style="width: 40%"></div>
                        </div>
                        <span class="text-xs text-gray-500 ml-2">2/5</span>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">R003 - Sur</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Carlos Mendoza</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">10 paradas</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">Completada</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-16 bg-gray-200 rounded-full h-2">
                          <div class="bg-blue-600 h-2 rounded-full" style="width: 100%"></div>
                        </div>
                        <span class="text-xs text-gray-500 ml-2">10/10</span>
                      </div>
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
            <h3 class="text-lg font-medium text-gray-900">Control de Flota</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Vehículos en Servicio</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700">VEH-001</span>
                    <span class="text-xs bg-green-600 text-white px-2 py-1 rounded">Activo</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700">VEH-002</span>
                    <span class="text-xs bg-green-600 text-white px-2 py-1 rounded">Activo</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700">VEH-003</span>
                    <span class="text-xs bg-green-600 text-white px-2 py-1 rounded">Activo</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 mb-2">Mantenimiento Pendiente</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">VEH-004</span>
                    <span class="text-xs text-yellow-600">5 días</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">VEH-006</span>
                    <span class="text-xs text-yellow-600">12 días</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Estadísticas del Día</h4>
                <div class="space-y-1 text-sm text-blue-700">
                  <div class="flex justify-between">
                    <span>Distancia Total:</span>
                    <span>245 km</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Combustible:</span>
                    <span>32.5 L</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Tiempo Promedio:</span>
                    <span>35 min</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <h4 class="text-sm font-medium text-gray-800 mb-2">Próximas Entregas</h4>
                <div class="space-y-2 text-sm text-gray-700">
                  <div class="flex justify-between">
                    <span>14:30 - Empresa ABC</span>
                    <span class="text-green-600">R001</span>
                  </div>
                  <div class="flex justify-between">
                    <span>15:15 - Hotel Plaza</span>
                    <span class="text-green-600">R001</span>
                  </div>
                  <div class="flex justify-between">
                    <span>16:00 - Oficina 123</span>
                    <span class="text-yellow-600">R002</span>
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
  name: 'RutasView',
  components: {
    AppNavigation
  }
}
</script>