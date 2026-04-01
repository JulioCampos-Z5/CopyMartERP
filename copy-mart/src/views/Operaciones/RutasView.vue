<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-emerald-50 dark:bg-emerald-900/30 p-6 rounded-lg border border-emerald-200 dark:border-emerald-700">
        <h1 class="text-3xl font-bold text-emerald-800 dark:text-emerald-200 mb-2">Gestión de Rutas</h1>
        <p class="text-emerald-600 dark:text-emerald-400">Control y optimización de rutas de entrega y servicio</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-emerald-100 dark:bg-emerald-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Rutas</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ routes.length }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">En Ruta</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.enRuta }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Programadas</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.programadas }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Completadas</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.completadas }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
        <div class="flex flex-wrap gap-4">
          <button @click="showCreateModal = true" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Ruta
          </button>
          <button @click="loadRoutes" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
          <select v-model="statusFilter" class="input-field w-48">
            <option value="">Todos los estados</option>
            <option value="programada">Programada</option>
            <option value="en_ruta">En Ruta</option>
            <option value="pausada">Pausada</option>
            <option value="completada">Completada</option>
            <option value="cancelada">Cancelada</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white dark:bg-gray-800 p-12 rounded-lg shadow border dark:border-gray-700 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mx-auto"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Cargando rutas...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/30 p-6 rounded-lg border border-red-200 dark:border-red-700">
        <p class="text-red-600 dark:text-red-400">{{ error }}</p>
        <button @click="loadRoutes" class="mt-2 text-red-700 dark:text-red-300 underline">Reintentar</button>
      </div>

      <!-- Main Content -->
      <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow border dark:border-gray-700">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Rutas ({{ filteredRoutes.length }})</h2>
        </div>
        <div class="p-6">
          <div v-if="filteredRoutes.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
            No hay rutas registradas
          </div>
          <div v-else class="space-y-4">
            <!-- Route Cards -->
            <div v-for="route in filteredRoutes" :key="route.route_id" 
              class="border dark:border-gray-700 rounded-lg overflow-hidden"
            >
              <!-- Route Header Row -->
              <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700"
                @click="toggleRouteDetail(route.route_id)"
              >
                <div class="flex items-center gap-4 flex-1 min-w-0">
                  <span class="font-mono font-bold text-emerald-600 dark:text-emerald-400">{{ route.route_code }}</span>
                  <span class="text-sm text-gray-900 dark:text-gray-200">{{ route.driver_name }}</span>
                  <span class="text-sm text-gray-500 dark:text-gray-400">{{ route.vehicle || '-' }}</span>
                  <span class="text-sm text-gray-700 dark:text-gray-300">{{ formatDate(route.scheduled_date) }}</span>
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(route.status)]">
                    {{ getStatusLabel(route.status) }}
                  </span>
                  <div class="flex items-center gap-2">
                    <div class="w-16 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div :class="getProgressBarColor(route.status)" class="h-2 rounded-full" :style="{ width: getProgress(route) + '%' }"></div>
                    </div>
                    <span class="text-xs text-gray-500 dark:text-gray-400">{{ route.completed_stops }}/{{ route.total_stops }}</span>
                  </div>
                </div>
                <div class="flex items-center gap-2 ml-4">
                  <button v-if="route.status === 'programada'" @click.stop="updateRouteStatus(route, 'en_ruta')" class="text-xs px-2 py-1 bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 rounded hover:bg-green-200">Iniciar</button>
                  <button v-if="route.status === 'en_ruta'" @click.stop="updateRouteStatus(route, 'pausada')" class="text-xs px-2 py-1 bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300 rounded hover:bg-yellow-200">Pausar</button>
                  <button v-if="route.status === 'pausada'" @click.stop="updateRouteStatus(route, 'en_ruta')" class="text-xs px-2 py-1 bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 rounded hover:bg-green-200">Reanudar</button>
                  <button v-if="route.status !== 'completada' && route.status !== 'cancelada'" @click.stop="updateRouteStatus(route, 'completada')" class="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 rounded hover:bg-blue-200">Completar</button>
                  <button v-if="route.status !== 'cancelada' && route.status !== 'completada'" @click.stop="deleteRoute(route.route_id)" class="text-xs px-2 py-1 bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 rounded hover:bg-red-200">Cancelar</button>
                  <svg :class="['w-5 h-5 text-gray-400 transition-transform', expandedRoute === route.route_id ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>

              <!-- Route Detail (Stops) -->
              <div v-if="expandedRoute === route.route_id" class="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300">
                    Paradas ({{ (route.stops || []).length }})
                  </h3>
                  <button @click="openAddStopModal(route)" class="text-xs px-3 py-1.5 bg-emerald-600 text-white rounded hover:bg-emerald-700 flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                    Agregar Parada
                  </button>
                </div>

                <div v-if="!route.stops || route.stops.length === 0" class="text-center py-6 text-gray-400 dark:text-gray-500 text-sm">
                  No hay paradas en esta ruta. Agrega una parada para vincular un cliente.
                </div>

                <div v-else class="space-y-3">
                  <div v-for="(stop, idx) in route.stops" :key="stop.stop_id"
                    class="flex items-start gap-3 p-3 rounded-lg border dark:border-gray-600"
                    :class="{
                      'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700': stop.visit_status === 'visitado',
                      'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-700': stop.visit_status === 'no_visitado',
                      'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-700': stop.visit_status === 'reagendado',
                      'bg-gray-50 dark:bg-gray-700/30': !stop.visit_status || stop.visit_status === 'pendiente'
                    }"
                  >
                    <!-- Stop number -->
                    <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                      :class="{
                        'bg-green-200 dark:bg-green-800 text-green-800 dark:text-green-200': stop.visit_status === 'visitado',
                        'bg-red-200 dark:bg-red-800 text-red-800 dark:text-red-200': stop.visit_status === 'no_visitado',
                        'bg-yellow-200 dark:bg-yellow-800 text-yellow-800 dark:text-yellow-200': stop.visit_status === 'reagendado',
                        'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300': !stop.visit_status || stop.visit_status === 'pendiente'
                      }"
                    >
                      {{ idx + 1 }}
                    </div>

                    <!-- Stop info -->
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2 flex-wrap">
                        <span class="font-medium text-sm text-gray-900 dark:text-white">
                          {{ stop.client_name || 'Sin cliente' }}
                        </span>
                        <span v-if="stop.branch_name" class="text-xs px-2 py-0.5 bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 rounded-full">
                          {{ stop.branch_name }}
                        </span>
                        <span v-if="stop.visit_status === 'visitado'" class="text-xs px-2 py-0.5 bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 rounded-full">Visitado</span>
                        <span v-else-if="stop.visit_status === 'no_visitado'" class="text-xs px-2 py-0.5 bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 rounded-full">No visitado</span>
                        <span v-else-if="stop.visit_status === 'reagendado'" class="text-xs px-2 py-0.5 bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300 rounded-full">Reagendado</span>
                      </div>
                      <div v-if="stop.address" class="flex items-center gap-1 mt-1">
                        <svg class="w-3.5 h-3.5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span class="text-xs text-gray-600 dark:text-gray-400">{{ stop.address }}{{ stop.city ? ', ' + stop.city : '' }}</span>
                      </div>
                      <p v-if="stop.notes" class="text-xs text-gray-500 dark:text-gray-400 mt-1 italic">{{ stop.notes }}</p>
                    </div>

                    <!-- Stop actions -->
                    <div class="flex items-center gap-1 flex-shrink-0">
                      <!-- Google Maps button -->
                      <button v-if="stop.address" @click="openGoogleMaps(stop)"
                        class="p-1.5 rounded hover:bg-blue-100 dark:hover:bg-blue-900/50 text-blue-600 dark:text-blue-400"
                        title="Abrir en Google Maps"
                      >
                        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                        </svg>
                      </button>
                      <!-- Visit status actions (only when not yet resolved) -->
                      <template v-if="stop.visit_status === 'pendiente'">
                        <button @click="markStopVisited(route, stop)"
                          class="text-xs px-2 py-1 rounded bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 hover:bg-green-200"
                          title="Marcar visitado"
                        >Visitado</button>
                        <button @click="openNoVisitModal(route, stop)"
                          class="text-xs px-2 py-1 rounded bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 hover:bg-red-200"
                          title="No visitado"
                        >No visitado</button>
                        <button @click="markStopRescheduled(route, stop)"
                          class="text-xs px-2 py-1 rounded bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300 hover:bg-yellow-200"
                          title="Reagendar"
                        >Reagendar</button>
                      </template>
                      <!-- Show reason if no_visitado -->
                      <span v-if="stop.visit_status === 'no_visitado' && stop.no_visit_reason"
                        class="text-xs text-red-600 dark:text-red-400 italic max-w-xs truncate"
                        :title="stop.no_visit_reason"
                      >Motivo: {{ stop.no_visit_reason }}</span>
                      <!-- Delete stop -->
                      <button @click="removeStop(route, stop.stop_id)"
                        class="p-1.5 rounded hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400"
                        title="Eliminar parada"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Google Maps: Open all stops as directions -->
                <div v-if="route.stops && route.stops.length > 1" class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <button @click="openGoogleMapsDirections(route)" class="text-sm px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center gap-2">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                    Ver ruta completa en Google Maps
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- Create Route Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Nueva Ruta</h3>
          <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="createRoute" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Código *</label>
              <input v-model="form.route_code" type="text" required class="input-field" placeholder="R001">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Conductor *</label>
              <input v-model="form.driver_name" type="text" required class="input-field" placeholder="Nombre del conductor">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Vehículo</label>
              <input v-model="form.vehicle" type="text" class="input-field" placeholder="VEH-001">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Fecha *</label>
              <input v-model="form.scheduled_date" type="date" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Estado</label>
              <select v-model="form.status" class="input-field">
                <option value="programada">Programada</option>
                <option value="en_ruta">En Ruta</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Notas</label>
            <textarea v-model="form.notes" rows="2" class="input-field" placeholder="Notas adicionales..."></textarea>
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showCreateModal = false" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">Cancelar</button>
            <button type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">Crear Ruta</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add Stop Modal -->
    <div v-if="showStopModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Agregar Parada</h3>
          <button @click="showStopModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="addStop" class="p-6 space-y-4">
          <!-- Client -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Cliente</label>
            <select v-model="stopForm.client_id" class="input-field" @change="onClientChange">
              <option :value="null">-- Seleccionar cliente --</option>
              <option v-for="c in clients" :key="c.client_id" :value="c.client_id">{{ c.name }}</option>
            </select>
          </div>
          <!-- Branch -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sucursal</label>
            <select v-model="stopForm.branch_id" class="input-field" @change="onBranchChange" :disabled="!stopForm.client_id">
              <option :value="null">-- Seleccionar sucursal --</option>
              <option v-for="b in clientBranches" :key="b.branch_id" :value="b.branch_id">
                {{ b.name }} {{ b.is_main ? '(Principal)' : '' }}
              </option>
            </select>
          </div>
          <!-- Address (auto-filled from branch, editable) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Dirección</label>
            <input v-model="stopForm.address" type="text" class="input-field" placeholder="Calle, número, colonia...">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Ciudad</label>
            <input v-model="stopForm.city" type="text" class="input-field" placeholder="Ciudad">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Notas</label>
            <input v-model="stopForm.notes" type="text" class="input-field" placeholder="Instrucciones especiales...">
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showStopModal = false" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">Cancelar</button>
            <button type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">Agregar Parada</button>
          </div>
        </form>
      </div>
    </div>
    <!-- No Visit Reason Modal -->
    <div v-if="showNoVisitModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Motivo de no visita</h3>
          <button @click="showNoVisitModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <div class="p-6 space-y-4">
          <p class="text-sm text-gray-600 dark:text-gray-400">Indica el motivo por el cual no se pudo visitar esta parada.</p>
          <textarea v-model="noVisitReason" rows="3" class="input-field" placeholder="Ej: Cliente no se encontraba, acceso restringido..."></textarea>
          <div class="flex justify-end gap-3">
            <button @click="showNoVisitModal = false" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">Cancelar</button>
            <button @click="confirmNoVisit" class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700">Confirmar</button>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { routeService } from '@/services/routeService.ts'
import { clientService } from '@/services/clientService.ts'

export default {
  name: 'RutasView',
  components: { BaseLayout },
  data() {
    return {
      routes: [],
      clients: [],
      clientBranches: [],
      loading: false,
      error: null,
      statusFilter: '',
      showCreateModal: false,
      showStopModal: false,
      showNoVisitModal: false,
      noVisitReason: '',
      noVisitTarget: null,  // { route, stop }
      expandedRoute: null,
      currentRouteId: null,
      form: {
        route_code: '',
        driver_name: '',
        vehicle: '',
        scheduled_date: new Date().toISOString().split('T')[0],
        status: 'programada',
        notes: ''
      },
      stopForm: {
        client_id: null,
        branch_id: null,
        address: '',
        city: '',
        notes: ''
      }
    }
  },
  computed: {
    filteredRoutes() {
      if (!this.statusFilter) return this.routes
      return this.routes.filter(r => r.status === this.statusFilter)
    },
    stats() {
      return {
        enRuta: this.routes.filter(r => r.status === 'en_ruta').length,
        programadas: this.routes.filter(r => r.status === 'programada').length,
        completadas: this.routes.filter(r => r.status === 'completada').length
      }
    }
  },
  async mounted() {
    await this.loadRoutes()
    await this.loadClients()
  },
  methods: {
    async loadRoutes() {
      this.loading = true
      this.error = null
      try {
        this.routes = await routeService.getRoutes()
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    async loadClients() {
      try {
        const res = await clientService.getClients({ pageSize: 500 })
        this.clients = res.items || []
      } catch (err) {
        console.error('Error loading clients:', err)
      }
    },
    async createRoute() {
      try {
        await routeService.createRoute(this.form)
        this.showCreateModal = false
        this.form = { route_code: '', driver_name: '', vehicle: '', scheduled_date: new Date().toISOString().split('T')[0], status: 'programada', notes: '' }
        await this.loadRoutes()
      } catch (err) {
        alert('Error al crear ruta: ' + (err.response?.data?.detail || err.message))
      }
    },
    async updateRouteStatus(route, newStatus) {
      try {
        const data = { status: newStatus }
        if (newStatus === 'completada') data.completed_stops = route.total_stops
        await routeService.updateRoute(route.route_id, data)
        await this.loadRoutes()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },
    async deleteRoute(routeId) {
      if (!confirm('¿Cancelar esta ruta?')) return
      try {
        await routeService.deleteRoute(routeId)
        await this.loadRoutes()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },
    toggleRouteDetail(routeId) {
      this.expandedRoute = this.expandedRoute === routeId ? null : routeId
    },
    openAddStopModal(route) {
      this.currentRouteId = route.route_id
      this.stopForm = { client_id: null, branch_id: null, address: '', city: '', notes: '' }
      this.clientBranches = []
      this.showStopModal = true
    },
    async onClientChange() {
      this.stopForm.branch_id = null
      this.clientBranches = []
      this.stopForm.address = ''
      this.stopForm.city = ''
      if (this.stopForm.client_id) {
        try {
          this.clientBranches = await clientService.getClientBranches(this.stopForm.client_id)
          // Auto-fill address from client
          const client = this.clients.find(c => c.client_id === this.stopForm.client_id)
          if (client) {
            this.stopForm.address = client.address || ''
            this.stopForm.city = client.city || ''
          }
        } catch (err) {
          console.error('Error loading branches:', err)
        }
      }
    },
    onBranchChange() {
      if (this.stopForm.branch_id) {
        const branch = this.clientBranches.find(b => b.branch_id === this.stopForm.branch_id)
        if (branch) {
          this.stopForm.address = branch.address || this.stopForm.address
          this.stopForm.city = branch.city || this.stopForm.city
        }
      }
    },
    async addStop() {
      try {
        const route = this.routes.find(r => r.route_id === this.currentRouteId)
        const stopOrder = route ? (route.stops || []).length : 0
        await routeService.addStop(this.currentRouteId, {
          ...this.stopForm,
          stop_order: stopOrder
        })
        this.showStopModal = false
        await this.loadRoutes()
      } catch (err) {
        alert('Error al agregar parada: ' + (err.message || err))
      }
    },
    async markStopVisited(route, stop) {
      try {
        await routeService.updateStop(stop.stop_id, { is_completed: true, visit_status: 'visitado' })
        await this.loadRoutes()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },
    openNoVisitModal(route, stop) {
      this.noVisitTarget = { route, stop }
      this.noVisitReason = ''
      this.showNoVisitModal = true
    },
    async confirmNoVisit() {
      if (!this.noVisitTarget) return
      try {
        await routeService.updateStop(this.noVisitTarget.stop.stop_id, {
          visit_status: 'no_visitado',
          no_visit_reason: this.noVisitReason || 'Sin motivo especificado'
        })
        this.showNoVisitModal = false
        this.noVisitTarget = null
        await this.loadRoutes()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },
    async markStopRescheduled(route, stop) {
      try {
        await routeService.updateStop(stop.stop_id, { visit_status: 'reagendado' })
        await this.loadRoutes()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },
    async removeStop(route, stopId) {
      if (!confirm('¿Eliminar esta parada?')) return
      try {
        await routeService.deleteStop(stopId)
        await this.loadRoutes()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },
    openGoogleMaps(stop) {
      const address = [stop.address, stop.city].filter(Boolean).join(', ')
      if (address) {
        const encoded = encodeURIComponent(address)
        window.open(`https://www.google.com/maps/search/?api=1&query=${encoded}`, '_blank')
      }
    },
    openGoogleMapsDirections(route) {
      const stops = (route.stops || []).filter(s => s.address)
      if (stops.length === 0) return
      if (stops.length === 1) {
        this.openGoogleMaps(stops[0])
        return
      }
      const origin = encodeURIComponent([stops[0].address, stops[0].city].filter(Boolean).join(', '))
      const destination = encodeURIComponent([stops[stops.length - 1].address, stops[stops.length - 1].city].filter(Boolean).join(', '))
      const waypoints = stops.slice(1, -1).map(s => encodeURIComponent([s.address, s.city].filter(Boolean).join(', '))).join('|')
      let url = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}`
      if (waypoints) url += `&waypoints=${waypoints}`
      window.open(url, '_blank')
    },
    getStatusClass(status) {
      const classes = {
        'programada': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
        'en_ruta': 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
        'pausada': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300',
        'completada': 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
        'cancelada': 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    getStatusLabel(status) {
      const labels = {
        'programada': 'Programada',
        'en_ruta': 'En Ruta',
        'pausada': 'Pausada',
        'completada': 'Completada',
        'cancelada': 'Cancelada'
      }
      return labels[status] || status
    },
    getProgressBarColor(status) {
      const colors = { 'en_ruta': 'bg-green-600', 'pausada': 'bg-yellow-600', 'completada': 'bg-blue-600' }
      return colors[status] || 'bg-gray-400'
    },
    getProgress(route) {
      if (!route.total_stops) return 0
      return Math.round((route.completed_stops / route.total_stops) * 100)
    },
    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('es-MX')
    }
  }
}
</script>