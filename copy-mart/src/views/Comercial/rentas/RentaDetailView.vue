<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6 flex justify-between items-start">
        <div>
          <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Volver a Rentas
          </button>
          <h1 class="text-3xl font-bold text-gray-900">Detalle de Renta</h1>
          <p class="text-gray-600 mt-1">Contrato: <span class="font-semibold text-blue-600">{{ rent?.contract_number || 'Cargando...' }}</span></p>
        </div>
        <div class="flex gap-2">
          <button @click="editRent" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Editar
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando información...</p>
      </div>

      <!-- Content -->
      <div v-else-if="rent" class="space-y-6">
        <!-- Estado Badge -->
        <div class="flex items-center gap-4">
          <span :class="getContractStatusClass(rent.contract_status)" class="px-4 py-2 rounded-full text-sm font-semibold">
            {{ getContractStatusLabel(rent.contract_status) }}
          </span>
          <span v-if="rent.is_foreign" class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
            Foráneo
          </span>
          <span v-if="rent.has_print_service" class="px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full text-sm">
            Con Servicio de Impresión
          </span>
        </div>

        <!-- Tabs -->
        <div class="bg-white rounded-lg shadow border">
          <div class="border-b border-gray-200">
            <nav class="flex -mb-px overflow-x-auto">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id 
                    ? 'border-blue-500 text-blue-600 bg-blue-50' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm flex items-center gap-2'
                ]"
              >
                {{ tab.label }}
                <span v-if="tab.count !== undefined" class="ml-1 px-2 py-0.5 text-xs rounded-full" 
                  :class="activeTab === tab.id ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'">
                  {{ tab.count }}
                </span>
              </button>
            </nav>
          </div>
        </div>

        <!-- Tab: Información General -->
        <div v-if="activeTab === 'info'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Datos del Contrato -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Datos del Contrato
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Número de Contrato</span>
                <span class="font-medium">{{ rent.contract_number || '-' }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Fecha de Inicio</span>
                <span class="font-medium">{{ formatDate(rent.start_date) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Fecha de Fin</span>
                <span class="font-medium">{{ rent.end_date ? formatDate(rent.end_date) : 'Indefinido' }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Renta Mensual</span>
                <span class="font-bold text-green-600 text-lg">${{ formatNumber(rent.rent) }}</span>
              </div>
              <div class="flex justify-between py-2">
                <span class="text-gray-500">Creado</span>
                <span class="font-medium text-sm">{{ formatDateTime(rent.created_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Datos del Cliente -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Cliente
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Nombre</span>
                <span class="font-medium">{{ rent.client?.name || `Cliente #${rent.client_id}` }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Sucursal</span>
                <span class="font-medium">{{ rent.branch?.name || 'Sin asignar' }}</span>
              </div>
              <div class="flex justify-between py-2">
                <span class="text-gray-500">Área</span>
                <span class="font-medium">{{ rent.area?.name || 'Sin asignar' }}</span>
              </div>
            </div>
          </div>

          <!-- Datos del Equipo -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Equipo Asignado
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">SKU</span>
                <span class="font-medium font-mono">{{ rent.equipment?.sku || '-' }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Modelo</span>
                <span class="font-medium">{{ rent.equipment?.model || '-' }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Serie</span>
                <span class="font-medium font-mono">{{ rent.equipment?.serie || '-' }}</span>
              </div>
              <div class="flex justify-between py-2">
                <span class="text-gray-500">Tipo</span>
                <span class="font-medium capitalize">{{ rent.equipment?.type || '-' }}</span>
              </div>
            </div>
          </div>

          <!-- Configuración de Impresión -->
          <div v-if="rent.has_print_service" class="bg-white rounded-lg shadow border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Servicio de Impresión
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-gray-50 p-3 rounded-lg">
                <p class="text-xs text-gray-500 mb-1">B/N Incluidas</p>
                <p class="text-xl font-bold text-gray-900">{{ formatNumber(rent.bn_included) }}</p>
              </div>
              <div class="bg-gray-50 p-3 rounded-lg">
                <p class="text-xs text-gray-500 mb-1">Costo Exceso B/N</p>
                <p class="text-xl font-bold text-gray-900">${{ rent.bn_cost_per_excess }}</p>
              </div>
              <div class="bg-blue-50 p-3 rounded-lg">
                <p class="text-xs text-blue-600 mb-1">Color Incluidas</p>
                <p class="text-xl font-bold text-blue-900">{{ formatNumber(rent.color_included) }}</p>
              </div>
              <div class="bg-blue-50 p-3 rounded-lg">
                <p class="text-xs text-blue-600 mb-1">Costo Exceso Color</p>
                <p class="text-xl font-bold text-blue-900">${{ rent.color_cost_per_excess }}</p>
              </div>
            </div>
            <div v-if="rent.print_notes" class="mt-4 p-3 bg-yellow-50 rounded-lg">
              <p class="text-xs text-yellow-700 mb-1">Notas:</p>
              <p class="text-sm text-yellow-900">{{ rent.print_notes }}</p>
            </div>
          </div>
        </div>

        <!-- Tab: Facturas -->
        <div v-if="activeTab === 'billings'" class="space-y-6">
          <div class="bg-white rounded-lg shadow border p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Facturas de esta Renta</h2>
            </div>

            <div v-if="loadingBillings" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>

            <div v-else-if="billings.length > 0" class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Factura</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Objetivo</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vencimiento</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="billing in billings" :key="billing.billing_id" class="hover:bg-gray-50">
                    <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ billing.invoice_number || `#${billing.billing_id}` }}</td>
                    <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(billing.target_date) }}</td>
                    <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(billing.due_date) }}</td>
                    <td class="px-4 py-3 text-sm font-semibold text-green-600">${{ formatNumber(billing.amount) }}</td>
                    <td class="px-4 py-3">
                      <span :class="getBillingStatusClass(billing.status)" class="px-2 py-1 text-xs rounded-full font-medium">
                        {{ getBillingStatusLabel(billing.status) }}
                      </span>
                    </td>
                    <td class="px-4 py-3">
                      <button @click="viewBilling(billing.billing_id)" class="text-blue-600 hover:text-blue-800">
                        Ver detalle
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p>No hay facturas generadas para esta renta</p>
              <p class="text-sm mt-2">Las facturas se generan automáticamente cuando el contrato está vigente</p>
            </div>
          </div>
        </div>

        <!-- Tab: Contadores de Impresión -->
        <div v-if="activeTab === 'counters'" class="space-y-6">
          <div class="bg-white rounded-lg shadow border p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Historial de Contadores</h2>
              <button v-if="rent.has_print_service" @click="openCounterModal()" class="bg-cyan-600 text-white px-4 py-2 rounded-lg hover:bg-cyan-700 flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Registrar Contador
              </button>
            </div>

            <div v-if="!rent.has_print_service" class="text-center py-8 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
              <p>Esta renta no tiene servicio de impresión habilitado</p>
            </div>

            <div v-else-if="loadingCounters" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-600"></div>
            </div>

            <div v-else-if="printCounters.length > 0" class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Período</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">B/N Impresas</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">B/N Exceso</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color Impresas</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color Exceso</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Excesos</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Facturado</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="counter in printCounters" :key="counter.counter_id" class="hover:bg-gray-50">
                    <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ counter.period_month }}/{{ counter.period_year }}</td>
                    <td class="px-4 py-3 text-sm text-gray-600">{{ formatNumber(counter.bn_printed) }}</td>
                    <td class="px-4 py-3 text-sm" :class="counter.bn_excess > 0 ? 'text-red-600 font-semibold' : 'text-gray-500'">
                      {{ formatNumber(counter.bn_excess) }}
                    </td>
                    <td class="px-4 py-3 text-sm text-blue-600">{{ formatNumber(counter.color_printed) }}</td>
                    <td class="px-4 py-3 text-sm" :class="counter.color_excess > 0 ? 'text-red-600 font-semibold' : 'text-gray-500'">
                      {{ formatNumber(counter.color_excess) }}
                    </td>
                    <td class="px-4 py-3 text-sm font-bold text-green-600">${{ formatNumber(counter.total_excess_amount) }}</td>
                    <td class="px-4 py-3">
                      <span :class="counter.is_billed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" class="px-2 py-1 text-xs rounded-full font-medium">
                        {{ counter.is_billed ? 'Sí' : 'Pendiente' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="text-center py-8 text-gray-500">
              <p>No hay registros de contadores para esta renta</p>
            </div>
          </div>
        </div>

        <!-- Tab: Planes Mensuales -->
        <div v-if="activeTab === 'plans'" class="space-y-6">
          <div class="bg-white rounded-lg shadow border p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Planes Mensuales de Servicio</h2>
              <button @click="openPlanModal()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Nuevo Plan
              </button>
            </div>

            <div v-if="loadingPlans" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>

            <div v-else-if="monthlyPlans.length > 0" class="space-y-4">
              <div v-for="plan in monthlyPlans" :key="plan.monthlyplan_id" class="border rounded-lg p-4 hover:bg-gray-50">
                <div class="flex justify-between items-start">
                  <div class="flex-1 grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p class="text-xs text-gray-500">Fecha de Visita</p>
                      <p class="text-sm font-medium">{{ formatDate(plan.visit_date) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Tipo de Servicio</p>
                      <p class="text-sm font-medium">{{ getServiceTypeName(plan.service_type_id) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Estado</p>
                      <span :class="getPlanStatusClass(plan.attendance_status)" class="inline-block px-2 py-1 text-xs font-medium rounded-full">
                        {{ getPlanStatusLabel(plan.attendance_status) }}
                      </span>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Técnicos</p>
                      <p class="text-sm font-medium">{{ plan.assigned_users?.length || 0 }} asignado(s)</p>
                    </div>
                  </div>
                  <div class="flex gap-2 ml-4">
                    <button @click="openPlanModal(plan)" class="text-blue-600 hover:text-blue-800">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="deletePlan(plan.monthlyplan_id)" class="text-red-600 hover:text-red-800">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8 text-gray-500">
              No hay planes mensuales registrados
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Plan Mensual -->
      <div v-if="showPlanModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showPlanModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-semibold mb-4">{{ planForm.monthlyplan_id ? 'Editar' : 'Nuevo' }} Plan Mensual</h3>
          <form @submit.prevent="savePlan" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Servicio *</label>
                <select v-model.number="planForm.service_type_id" required class="w-full px-3 py-2 border rounded-lg">
                  <option value="">Seleccione...</option>
                  <option v-for="type in serviceTypes" :key="type.service_type_id" :value="type.service_type_id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Visita *</label>
                <input v-model="planForm.visit_date" type="date" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div v-if="planForm.monthlyplan_id">
                <label class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
                <select v-model="planForm.attendance_status" required class="w-full px-3 py-2 border rounded-lg">
                  <option value="pendiente">Pendiente</option>
                  <option value="visitado">Visitado</option>
                  <option value="no_quedo">No Quedó</option>
                </select>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
                <textarea v-model="planForm.description" rows="3" class="w-full px-3 py-2 border rounded-lg"></textarea>
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showPlanModal = false" class="px-4 py-2 border rounded-lg">Cancelar</button>
              <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal Contador -->
      <div v-if="showCounterModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showCounterModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg">
          <h3 class="text-xl font-semibold mb-4">Registrar Contador</h3>
          <form @submit.prevent="saveCounter" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Mes *</label>
                <select v-model.number="counterForm.period_month" required class="w-full px-3 py-2 border rounded-lg">
                  <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Año *</label>
                <input v-model.number="counterForm.period_year" type="number" min="2020" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Contador B/N Actual *</label>
                <input v-model.number="counterForm.bn_current" type="number" min="0" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Contador Color Actual *</label>
                <input v-model.number="counterForm.color_current" type="number" min="0" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Lectura</label>
                <input v-model="counterForm.reading_date" type="date" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
              <textarea v-model="counterForm.notes" rows="2" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showCounterModal = false" class="px-4 py-2 border rounded-lg">Cancelar</button>
              <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded-lg hover:bg-cyan-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppNavigation from '@/components/AppNavigation.vue'
import { rentService } from '@/services/rentService'
import { billingService } from '@/services/billingService'
import printService from '@/services/printService'
import monthlyplanService from '@/services/monthlyplanService'

const route = useRoute()
const router = useRouter()

const rentId = computed(() => Number(route.params.id))
const loading = ref(true)
const rent = ref<any>(null)
const activeTab = ref('info')

// Billings
const billings = ref<any[]>([])
const loadingBillings = ref(false)

// Print Counters
const printCounters = ref<any[]>([])
const loadingCounters = ref(false)
const showCounterModal = ref(false)
const counterForm = ref({
  period_month: new Date().getMonth() + 1,
  period_year: new Date().getFullYear(),
  bn_current: 0,
  color_current: 0,
  reading_date: new Date().toISOString().split('T')[0],
  notes: ''
})

// Monthly Plans
const monthlyPlans = ref<any[]>([])
const loadingPlans = ref(false)
const showPlanModal = ref(false)
const serviceTypes = ref<any[]>([])
const planForm = ref<any>({
  monthlyplan_id: 0,
  client_id: 0,
  branch_id: 0,
  service_type_id: 0,
  description: '',
  visit_date: '',
  attendance_status: 'pendiente'
})

const tabs = computed(() => [
  { id: 'info', label: 'Información' },
  { id: 'billings', label: 'Facturas', count: billings.value.length },
  { id: 'counters', label: 'Contadores', count: printCounters.value.length },
  { id: 'plans', label: 'Planes', count: monthlyPlans.value.length }
])

// Load Data
const loadRent = async () => {
  loading.value = true
  try {
    rent.value = await rentService.getRentById(rentId.value)
  } catch (error) {
    console.error('Error loading rent:', error)
  } finally {
    loading.value = false
  }
}

const loadBillings = async () => {
  loadingBillings.value = true
  try {
    const response = await billingService.getBillings({ rent_id: rentId.value })
    billings.value = response.items || []
  } catch (error) {
    console.error('Error loading billings:', error)
    billings.value = []
  } finally {
    loadingBillings.value = false
  }
}

const loadPrintCounters = async () => {
  if (!rent.value?.has_print_service) return
  loadingCounters.value = true
  try {
    const response = await printService.getAll({ rent_id: rentId.value })
    printCounters.value = response || []
  } catch (error) {
    console.error('Error loading counters:', error)
    printCounters.value = []
  } finally {
    loadingCounters.value = false
  }
}

const loadMonthlyPlans = async () => {
  loadingPlans.value = true
  try {
    const response = await monthlyplanService.getAll({ client_id: rent.value?.client_id })
    monthlyPlans.value = response || []
  } catch (error) {
    console.error('Error loading plans:', error)
    monthlyPlans.value = []
  } finally {
    loadingPlans.value = false
  }
}

const loadServiceTypes = async () => {
  try {
    serviceTypes.value = await monthlyplanService.getServiceTypes()
  } catch (error) {
    console.error('Error loading service types:', error)
  }
}

// Actions
const editRent = () => {
  router.push(`/rentas/${rentId.value}/editar`)
}

const viewBilling = (billingId: number) => {
  router.push(`/facturacion/${billingId}`)
}

const openCounterModal = () => {
  counterForm.value = {
    period_month: new Date().getMonth() + 1,
    period_year: new Date().getFullYear(),
    bn_current: 0,
    color_current: 0,
    reading_date: new Date().toISOString().split('T')[0],
    notes: ''
  }
  showCounterModal.value = true
}

const saveCounter = async () => {
  try {
    await printService.create({
      rent_id: rentId.value,
      ...counterForm.value
    })
    showCounterModal.value = false
    await loadPrintCounters()
  } catch (error: any) {
    alert(`Error: ${error.message || error}`)
  }
}

const openPlanModal = (plan?: any) => {
  if (plan) {
    planForm.value = { ...plan }
  } else {
    planForm.value = {
      monthlyplan_id: 0,
      client_id: rent.value?.client_id,
      branch_id: rent.value?.branch_id || 1,
      service_type_id: 0,
      description: '',
      visit_date: '',
      attendance_status: 'pendiente'
    }
  }
  showPlanModal.value = true
}

const savePlan = async () => {
  try {
    if (planForm.value.monthlyplan_id) {
      await monthlyplanService.update(planForm.value.monthlyplan_id, planForm.value)
    } else {
      await monthlyplanService.create(planForm.value)
    }
    showPlanModal.value = false
    await loadMonthlyPlans()
  } catch (error: any) {
    alert(`Error: ${error.message || error}`)
  }
}

const deletePlan = async (planId: number) => {
  if (!confirm('¿Eliminar este plan?')) return
  try {
    await monthlyplanService.delete(planId)
    await loadMonthlyPlans()
  } catch (error: any) {
    alert(`Error: ${error.message || error}`)
  }
}

// Helpers
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' })
}

const formatDateTime = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('es-MX')
}

const formatNumber = (num: any) => {
  if (num === null || num === undefined) return '0'
  return Number(num).toLocaleString('es-MX')
}

const getContractStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'vigente': 'bg-green-100 text-green-800',
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'sin_firmar': 'bg-orange-100 text-orange-800',
    'finalizado': 'bg-gray-100 text-gray-800',
    'cancelado': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getContractStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    'vigente': 'Vigente',
    'pendiente': 'Pendiente',
    'sin_firmar': 'Sin Firmar',
    'finalizado': 'Finalizado',
    'cancelado': 'Cancelado'
  }
  return labels[status] || status
}

const getBillingStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'pagado': 'bg-green-100 text-green-800',
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'vencido': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getBillingStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    'pagado': 'Pagado',
    'pendiente': 'Pendiente',
    'vencido': 'Vencido'
  }
  return labels[status] || status
}

const getPlanStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'visitado': 'bg-green-100 text-green-800',
    'no_quedo': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPlanStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    'pendiente': 'Pendiente',
    'visitado': 'Visitado',
    'no_quedo': 'No Quedó'
  }
  return labels[status] || status
}

const getServiceTypeName = (id: number) => {
  const type = serviceTypes.value.find(t => t.service_type_id === id)
  return type?.name || `Tipo #${id}`
}

const goBack = () => {
  router.push('/rentas')
}

onMounted(async () => {
  await loadRent()
  await Promise.all([
    loadBillings(),
    loadPrintCounters(),
    loadMonthlyPlans(),
    loadServiceTypes()
  ])
})
</script>
