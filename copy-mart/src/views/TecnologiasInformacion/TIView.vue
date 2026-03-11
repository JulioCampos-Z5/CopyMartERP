<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-slate-50 dark:bg-slate-900/30 p-6 rounded-lg border border-slate-200 dark:border-slate-700">
        <h1 class="text-3xl font-bold text-slate-800 dark:text-slate-200 mb-2">Tecnologías de la Información</h1>
        <p class="text-slate-600 dark:text-slate-400">Centro de control y administración de sistemas</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-slate-100 dark:bg-slate-800 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">CPU</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ systemInfo?.cpu?.percent ?? '...' }}%</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">RAM</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ systemInfo?.ram?.used_gb ?? '...' }} / {{ systemInfo?.ram?.total_gb ?? '...' }} GB</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Disco</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ systemInfo?.disk?.percent ?? '...' }}%</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Uptime</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ uptimeText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
        <div class="flex flex-wrap gap-4">
          <button @click="showIncidentModal = true" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Levantar Reporte
          </button>
          <button @click="loadSystemInfo" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Reportes / Incidencias -->
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow border dark:border-gray-700">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Reportes de Incidencias</h2>
          </div>
          <div class="p-6">
            <div v-if="incidents.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
              No hay reportes registrados
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50 dark:bg-gray-700">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">#</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Descripción</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Reportado por</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Prioridad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha</th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="(inc, idx) in incidents" :key="idx">
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ idx + 1 }}</td>
                    <td class="px-4 py-4 text-sm text-gray-900 dark:text-gray-200">{{ inc.description }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ inc.reported_by }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getPriorityClass(inc.priority)]">
                        {{ inc.priority }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStateClass(inc.state)]">
                        {{ inc.state }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ inc.date }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Monitoreo -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow border dark:border-gray-700">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Estado del Sistema</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <!-- Servicios -->
              <div class="p-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-700 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 dark:text-green-200 mb-2">Servicios</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700 dark:text-green-300">Backend API</span>
                    <span :class="['text-xs px-2 py-1 rounded text-white', systemInfo?.services?.backend ? 'bg-green-600' : 'bg-red-600']">
                      {{ systemInfo?.services?.backend ? 'Online' : 'Offline' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-green-700 dark:text-green-300">Base de Datos</span>
                    <span :class="['text-xs px-2 py-1 rounded text-white', systemInfo?.services?.database ? 'bg-green-600' : 'bg-red-600']">
                      {{ systemInfo?.services?.database ? 'Online' : 'Offline' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Uso de Recursos -->
              <div class="p-4 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">Uso de Recursos</h4>
                <div class="space-y-3">
                  <div>
                    <div class="flex justify-between text-sm text-blue-700 dark:text-blue-300">
                      <span>CPU</span>
                      <span>{{ systemInfo?.cpu?.percent ?? 0 }}%</span>
                    </div>
                    <div class="w-full bg-blue-200 dark:bg-blue-900 rounded-full h-2 mt-1">
                      <div class="bg-blue-600 h-2 rounded-full transition-all" :style="{ width: (systemInfo?.cpu?.percent ?? 0) + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm text-blue-700 dark:text-blue-300">
                      <span>RAM</span>
                      <span>{{ systemInfo?.ram?.percent ?? 0 }}%</span>
                    </div>
                    <div class="w-full bg-blue-200 dark:bg-blue-900 rounded-full h-2 mt-1">
                      <div class="bg-blue-600 h-2 rounded-full transition-all" :style="{ width: (systemInfo?.ram?.percent ?? 0) + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-sm text-blue-700 dark:text-blue-300">
                      <span>Disco</span>
                      <span>{{ systemInfo?.disk?.percent ?? 0 }}%</span>
                    </div>
                    <div class="w-full bg-blue-200 dark:bg-blue-900 rounded-full h-2 mt-1">
                      <div class="bg-blue-600 h-2 rounded-full transition-all" :style="{ width: (systemInfo?.disk?.percent ?? 0) + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Información del Sistema -->
              <div class="p-4 bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg">
                <h4 class="text-sm font-medium text-gray-800 dark:text-gray-200 mb-2">Información</h4>
                <div class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                  <div class="flex justify-between">
                    <span>Sistema</span>
                    <span>{{ systemInfo?.system?.os ?? '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Hostname</span>
                    <span>{{ systemInfo?.system?.hostname ?? '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>CPU Cores</span>
                    <span>{{ systemInfo?.cpu?.cores ?? '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Disco Total</span>
                    <span>{{ systemInfo?.disk?.total_gb ?? '-' }} GB</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Disco Usado</span>
                    <span>{{ systemInfo?.disk?.used_gb ?? '-' }} GB</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Red Enviado</span>
                    <span>{{ systemInfo?.network?.sent_mb ?? '-' }} MB</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Red Recibido</span>
                    <span>{{ systemInfo?.network?.recv_mb ?? '-' }} MB</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- Modal: Levantar Reporte -->
    <div v-if="showIncidentModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Levantar Reporte</h3>
            <button @click="showIncidentModal = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <form @submit.prevent="submitIncident" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Descripción del problema *</label>
            <textarea v-model="incidentForm.description" required rows="3" class="input-field w-full" placeholder="Describe el problema..."></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Prioridad</label>
            <select v-model="incidentForm.priority" class="input-field w-full">
              <option value="Baja">Baja</option>
              <option value="Media">Media</option>
              <option value="Alta">Alta</option>
              <option value="Crítica">Crítica</option>
            </select>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showIncidentModal = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Crear Reporte</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Success message -->
    <div v-if="successMsg" class="fixed bottom-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      {{ successMsg }}
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { apiGet } from '@/config/api'

export default {
  name: 'TIView',
  components: { BaseLayout },
  data() {
    return {
      systemInfo: null,
      loading: false,
      showIncidentModal: false,
      successMsg: null,
      incidents: [],
      incidentForm: {
        description: '',
        priority: 'Media'
      }
    }
  },
  computed: {
    uptimeText() {
      if (!this.systemInfo?.uptime) return '...'
      const h = this.systemInfo.uptime.hours
      const m = this.systemInfo.uptime.minutes
      if (h > 24) return Math.floor(h / 24) + 'd ' + (h % 24) + 'h'
      return h + 'h ' + m + 'm'
    }
  },
  async mounted() {
    await this.loadSystemInfo()
    this.loadIncidents()
  },
  methods: {
    async loadSystemInfo() {
      this.loading = true
      try {
        this.systemInfo = await apiGet('/api/system-info')
      } catch (err) {
        console.error('Error loading system info:', err)
      } finally {
        this.loading = false
      }
    },

    loadIncidents() {
      const stored = localStorage.getItem('ti_incidents')
      if (stored) {
        try { this.incidents = JSON.parse(stored) } catch { this.incidents = [] }
      }
    },

    saveIncidents() {
      localStorage.setItem('ti_incidents', JSON.stringify(this.incidents))
    },

    submitIncident() {
      const userData = JSON.parse(localStorage.getItem('user') || '{}')
      const newIncident = {
        description: this.incidentForm.description,
        priority: this.incidentForm.priority,
        reported_by: userData.name || userData.full_name || 'Usuario',
        state: 'Abierto',
        date: new Date().toLocaleDateString('es-MX')
      }
      this.incidents.unshift(newIncident)
      this.saveIncidents()
      this.showIncidentModal = false
      this.incidentForm = { description: '', priority: 'Media' }
      this.successMsg = 'Reporte creado exitosamente'
      setTimeout(() => { this.successMsg = null }, 3000)
    },

    getPriorityClass(priority) {
      const classes = {
        'Baja': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'Media': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'Alta': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
        'Crítica': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      }
      return classes[priority] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    },

    getStateClass(state) {
      const classes = {
        'Abierto': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'En Progreso': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'Resuelto': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'Cerrado': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
      }
      return classes[state] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }
}
</script>