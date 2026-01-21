<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-teal-50 p-6 rounded-lg border border-teal-200">
        <h1 class="text-3xl font-bold text-teal-800 mb-2">Recursos Humanos</h1>
        <p class="text-teal-600">Gestión integral del personal y nóminas</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-teal-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Empleados Activos</h3>
              <p class="text-2xl font-semibold text-gray-900">47</p>
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
              <h3 class="text-sm font-medium text-gray-500">Solicitudes Pendientes</h3>
              <p class="text-2xl font-semibold text-gray-900">8</p>
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
              <h3 class="text-sm font-medium text-gray-500">Nómina del Mes</h3>
              <p class="text-2xl font-semibold text-gray-900">$298,450</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Evaluaciones Mes</h3>
              <p class="text-2xl font-semibold text-gray-900">12</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <router-link to="/recursos-humanos/empleados" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Gestionar Empleados
          </router-link>
          <router-link to="/recursos-humanos/nominas" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Procesar Nóminas
          </router-link>
          <router-link to="/recursos-humanos/vacaciones" class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3a4 4 0 118 0v4m-4 12v6m0 0l-3-3m3 3l3-3" />
            </svg>
            Gestionar Vacaciones
          </router-link>
          <router-link to="/recursos-humanos/areas" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 flex items-center transition-colors">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Gestionar Áreas
          </router-link>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Lista de Empleados -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Empleados Recientes</h2>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empleado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Puesto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Departamento</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ingreso</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="h-8 w-8 bg-teal-500 rounded-full flex items-center justify-center">
                          <span class="text-xs font-medium text-white">JP</span>
                        </div>
                        <div class="ml-3">
                          <p class="text-sm font-medium text-gray-900">Juan Pérez</p>
                          <p class="text-sm text-gray-500">EMP001</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Operador de Máquina</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Producción</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Activo</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">15/03/2023</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="h-8 w-8 bg-purple-500 rounded-full flex items-center justify-center">
                          <span class="text-xs font-medium text-white">ML</span>
                        </div>
                        <div class="ml-3">
                          <p class="text-sm font-medium text-gray-900">María López</p>
                          <p class="text-sm text-gray-500">EMP002</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Cajera</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Ventas</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full">Vacaciones</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">20/01/2024</td>
                  </tr>
                  <tr>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center">
                          <span class="text-xs font-medium text-white">CR</span>
                        </div>
                        <div class="ml-3">
                          <p class="text-sm font-medium text-gray-900">Carlos Ruiz</p>
                          <p class="text-sm text-gray-500">EMP003</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Supervisor</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">Operaciones</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Activo</span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">10/05/2022</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Gestión -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Gestión del Personal</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 mb-2">Solicitudes Pendientes</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Vacaciones - Juan P.</span>
                    <button class="text-xs bg-yellow-600 text-white px-2 py-1 rounded">Revisar</button>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Permiso - Ana G.</span>
                    <button class="text-xs bg-yellow-600 text-white px-2 py-1 rounded">Revisar</button>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Cumpleaños del Mes</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-blue-700">María L. - 15/11</span>
                    <span class="text-xs text-blue-600">3 días</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-blue-700">Pedro M. - 22/11</span>
                    <span class="text-xs text-blue-600">10 días</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Indicadores del Mes</h4>
                <div class="space-y-1 text-sm text-green-700">
                  <div class="flex justify-between">
                    <span>Asistencia:</span>
                    <span>96%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Puntualidad:</span>
                    <span>92%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Rotación:</span>
                    <span>4.2%</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 class="text-sm font-medium text-red-800 mb-2">Próximos Vencimientos</h4>
                <div class="space-y-2 text-sm text-red-700">
                  <div>Contratos: 3 empleados</div>
                  <div>Evaluaciones: 5 pendientes</div>
                  <div>Capacitaciones: 8 empleados</div>
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
  name: 'RHView',
  components: {
    BaseLayout
  }
}
</script>