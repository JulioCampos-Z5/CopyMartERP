<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
              <h3 class="text-sm font-medium text-gray-500">Total Rutas</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ routes.length }}</p>
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
              <h3 class="text-sm font-medium text-gray-500">En Ruta</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.enRuta }}</p>
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
              <h3 class="text-sm font-medium text-gray-500">Programadas</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.programadas }}</p>
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
              <h3 class="text-sm font-medium text-gray-500">Completadas</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.completadas }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
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
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando rutas...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 p-6 rounded-lg border border-red-200">
        <p class="text-red-600">{{ error }}</p>
        <button @click="loadRoutes" class="mt-2 text-red-700 underline">Reintentar</button>
      </div>

      <!-- Main Content -->
      <div v-else class="bg-white rounded-lg shadow border">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Rutas ({{ filteredRoutes.length }})</h2>
        </div>
        <div class="p-6">
          <div v-if="filteredRoutes.length === 0" class="text-center py-8 text-gray-500">
            No hay rutas registradas
          </div>
          <div v-else class="overflow-x-auto">
            <table class="min-w-full table-auto">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Código</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Conductor</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vehículo</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Paradas</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Progreso</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="route in filteredRoutes" :key="route.route_id">
                  <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-emerald-600">{{ route.route_code }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ route.driver_name }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{{ route.vehicle || '-' }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-700">{{ formatDate(route.scheduled_date) }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ route.total_stops }} paradas</td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(route.status)]">
                      {{ getStatusLabel(route.status) }}
                    </span>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div :class="getProgressBarColor(route.status)" class="h-2 rounded-full" :style="{ width: getProgress(route) + '%' }"></div>
                      </div>
                      <span class="text-xs text-gray-500 ml-2">{{ route.completed_stops }}/{{ route.total_stops }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm space-x-2">
                    <button v-if="route.status === 'programada'" @click="updateRouteStatus(route, 'en_ruta')" class="text-green-600 hover:text-green-900">Iniciar</button>
                    <button v-if="route.status === 'en_ruta'" @click="updateRouteStatus(route, 'pausada')" class="text-yellow-600 hover:text-yellow-900">Pausar</button>
                    <button v-if="route.status === 'pausada'" @click="updateRouteStatus(route, 'en_ruta')" class="text-green-600 hover:text-green-900">Reanudar</button>
                    <button v-if="route.status !== 'completada' && route.status !== 'cancelada'" @click="updateRouteStatus(route, 'completada')" class="text-blue-600 hover:text-blue-900">Completar</button>
                    <button v-if="route.status !== 'cancelada' && route.status !== 'completada'" @click="deleteRoute(route.route_id)" class="text-red-600 hover:text-red-900">Cancelar</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-lg w-full">
        <div class="p-6 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-xl font-semibold text-gray-900">Nueva Ruta</h3>
          <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="createRoute" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código *</label>
              <input v-model="form.route_code" type="text" required class="input-field" placeholder="R001">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Conductor *</label>
              <input v-model="form.driver_name" type="text" required class="input-field" placeholder="Nombre del conductor">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Vehículo</label>
              <input v-model="form.vehicle" type="text" class="input-field" placeholder="VEH-001">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha *</label>
              <input v-model="form.scheduled_date" type="date" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Total Paradas</label>
              <input v-model.number="form.total_stops" type="number" min="0" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="form.status" class="input-field">
                <option value="programada">Programada</option>
                <option value="en_ruta">En Ruta</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
            <textarea v-model="form.notes" rows="2" class="input-field" placeholder="Notas adicionales..."></textarea>
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showCreateModal = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">Crear Ruta</button>
          </div>
        </form>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { routeService } from '@/services/routeService.ts'

export default {
  name: 'RutasView',
  components: { BaseLayout },
  data() {
    return {
      routes: [],
      loading: false,
      error: null,
      statusFilter: '',
      showCreateModal: false,
      form: {
        route_code: '',
        driver_name: '',
        vehicle: '',
        scheduled_date: new Date().toISOString().split('T')[0],
        total_stops: 0,
        status: 'programada',
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
    async createRoute() {
      try {
        await routeService.createRoute(this.form)
        this.showCreateModal = false
        this.form = { route_code: '', driver_name: '', vehicle: '', scheduled_date: new Date().toISOString().split('T')[0], total_stops: 0, status: 'programada', notes: '' }
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
    getStatusClass(status) {
      const classes = {
        'programada': 'bg-gray-100 text-gray-800',
        'en_ruta': 'bg-green-100 text-green-800',
        'pausada': 'bg-yellow-100 text-yellow-800',
        'completada': 'bg-blue-100 text-blue-800',
        'cancelada': 'bg-red-100 text-red-800'
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