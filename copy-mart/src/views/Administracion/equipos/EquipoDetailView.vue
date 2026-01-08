<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Volver a Inventario
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Detalle del Equipo</h1>
        <p class="text-gray-600 mt-2">Información completa del equipo</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando información...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {{ error }}
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Actions Bar -->
        <div class="bg-white p-4 rounded-lg shadow border flex justify-end gap-3">
          <button @click="editEquipment" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Editar
          </button>
        </div>

        <!-- Main Info Card -->
        <div class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-6">Información General</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <p class="text-sm text-gray-500 mb-1">SKU</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.sku || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Marca</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.brand?.name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Modelo</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.model || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Número de Serie</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.serie || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Modelo de Toner</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.model_toner || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Tipo</p>
              <p class="text-base font-medium text-gray-900">
                <span :class="equipment.type === 'color' ? 'text-purple-600' : 'text-gray-900'">
                  {{ equipment.type === 'color' ? 'Color' : 'Monocromo' }}
                </span>
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Estado</p>
              <p class="text-base font-medium">
                <span :class="getStatusClass(equipment.location_status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ equipment.location_status || '-' }}
                </span>
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Proveedor</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.supplier?.name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Factura</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.invoice || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Costo</p>
              <p class="text-base font-medium text-gray-900">
                {{ equipment.cost ? formatCurrency(equipment.cost) : '-' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Comments Card -->
        <div v-if="equipment.comments" class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Comentarios</h2>
          <p class="text-gray-700">{{ equipment.comments }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { equipmentService } from '@/services/equipmentService'

export default {
  name: 'EquipoDetailView',
  components: {
    AppNavigation
  },
  data() {
    return {
      equipment: {},
      loading: false,
      error: null
    }
  },
  async mounted() {
    await this.loadEquipment()
  },
  methods: {
    async loadEquipment() {
      this.loading = true
      this.error = null
      try {
        this.equipment = await equipmentService.getEquipmentById(this.$route.params.id)
      } catch (err) {
        this.error = 'Error al cargar el equipo: ' + err.message
      } finally {
        this.loading = false
      }
    },

    editEquipment() {
      this.$router.push(`/administracion/equipos/editar/${this.$route.params.id}`)
    },

    goBack() {
      this.$router.push('/inventario')
    },

    formatCurrency(value) {
      return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
      }).format(value)
    },

    getStatusClass(status) {
      const classes = {
        'bodega': 'bg-green-100 text-green-800',
        'asignado': 'bg-blue-100 text-blue-800',
        'vendido': 'bg-gray-100 text-gray-800',
        'taller': 'bg-yellow-100 text-yellow-800',
        'desconocido': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }
  }
}
</script>
