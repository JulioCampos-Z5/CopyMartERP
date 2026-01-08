<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h1 class="text-3xl font-bold text-blue-800 mb-2">Gestión de Rentas</h1>
        <p class="text-blue-600">Administra los servicios de renta y alquiler de equipos</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Rentas Activas</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.active }}</p>
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
              <h3 class="text-sm font-medium text-gray-500">Ingresos del Mes</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ formatCurrency(stats.monthlyIncome) }}</p>
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
              <h3 class="text-sm font-medium text-gray-500">Próximos Vencimientos</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.expiringSoon }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Total Contratos</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ rents.length }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <button @click="goToNewRent" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Renta
          </button>
          <button @click="loadRents" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
          <select v-model="filters.contract_status" class="input-field w-48">
            <option value="">Todos los estados</option>
            <option value="vigente">Vigente</option>
            <option value="pendiente">Pendiente</option>
            <option value="sin_firmar">Sin Firmar</option>
            <option value="vencido">Vencido</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando rentas...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 p-6 rounded-lg border border-red-200">
        <p class="text-red-600">{{ error }}</p>
        <button @click="loadRents" class="mt-2 text-red-700 underline">Reintentar</button>
      </div>

      <!-- Main Content -->
      <div v-else class="bg-white rounded-lg shadow border">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Contratos de Renta ({{ filteredRents.length }})</h2>
        </div>
        <div class="p-6">
          <div v-if="filteredRents.length === 0" class="text-center py-8 text-gray-500">
            No hay rentas registradas
          </div>
          <div v-else class="overflow-x-auto">
            <table class="min-w-full table-auto">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contrato</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Equipo</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ubicación</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="rent in filteredRents" :key="rent.rent_id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{{ rent.contract_number || '-' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ rent.client?.name || '-' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ rent.equipment?.model || '-' }}
                    <span class="text-gray-500 text-xs block">{{ rent.equipment?.sku || '' }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ rent.branch?.name || '-' }}
                    <span v-if="rent.area" class="text-xs block">{{ rent.area.name }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(rent.contract_status)]">
                      {{ getStatusLabel(rent.contract_status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ formatCurrency(rent.rent) }}/mes</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button @click="viewRent(rent)" class="text-blue-600 hover:text-blue-900 mr-3">Ver</button>
                    <button v-if="rent.contract_status !== 'vigente'" @click="updateStatus(rent.rent_id, 'vigente')" class="text-green-600 hover:text-green-900 mr-3">Activar</button>
                    <button @click="cancelRent(rent.rent_id)" class="text-red-600 hover:text-red-900">Cancelar</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ selectedRent ? 'Ver Renta' : 'Nueva Renta' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Formulario de creación -->
        <form v-if="!selectedRent" @submit.prevent="createRent" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
              <select v-model="rentForm.client_id" required class="input-field">
                <option value="">Selecciona un cliente</option>
                <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                  {{ client.name }} - {{ client.rfc }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Equipo *</label>
              <select v-model="rentForm.equipment_id" required class="input-field">
                <option value="">Selecciona un equipo</option>
                <option v-for="equipment in availableEquipment" :key="equipment.item_id" :value="equipment.item_id">
                  {{ equipment.model }} - {{ equipment.sku }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Contrato</label>
              <input v-model="rentForm.contract_number" type="text" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Renta Mensual *</label>
              <input v-model="rentForm.rent" type="number" step="0.01" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado del Contrato</label>
              <select v-model="rentForm.contract_status" class="input-field">
                <option value="vigente">Vigente</option>
                <option value="pendiente">Pendiente</option>
                <option value="sin_firmar">Sin Firmar</option>
                <option value="vencido">Vencido</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="flex items-center">
                <input v-model="rentForm.is_foreign" type="checkbox" class="mr-2">
                <span class="text-sm text-gray-700">Servicio Foráneo</span>
              </label>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              Crear Renta
            </button>
          </div>
        </form>

        <!-- Vista de detalle -->
        <div v-else class="p-6">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Cliente</p>
              <p class="text-base font-medium">{{ selectedRent.client?.name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Equipo</p>
              <p class="text-base font-medium">{{ selectedRent.equipment?.model }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Contrato</p>
              <p class="text-base font-medium">{{ selectedRent.contract_number }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Renta Mensual</p>
              <p class="text-base font-medium">{{ formatCurrency(selectedRent.rent) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Estado</p>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(selectedRent.contract_status)]">
                {{ getStatusLabel(selectedRent.contract_status) }}
              </span>
            </div>
            <div>
              <p class="text-sm text-gray-500">Servicio Foráneo</p>
              <p class="text-base font-medium">{{ selectedRent.is_foreign ? 'Sí' : 'No' }}</p>
            </div>
          </div>
          <div class="mt-6 flex justify-end">
            <button @click="closeModal" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { rentService } from '@/services/rentService'
import { clientService } from '@/services/clientService'
import { equipmentService } from '@/services/equipmentService'

export default {
  name: 'RentasView',
  components: {
    BaseLayout
  },
  data() {
    return {
      rents: [],
      clients: [],
      availableEquipment: [],
      loading: false,
      error: null,
      stats: {
        active: 0,
        monthlyIncome: 0,
        expiringSoon: 0,
        availableEquipment: 0
      },
      filters: {
        contract_status: '',
        is_active: true
      },
      showModal: false,
      selectedRent: null,
      rentForm: {
        client_id: '',
        equipment_id: '',
        contract_number: '',
        rent: '',
        contract_status: 'pendiente',
        is_foreign: false
      }
    }
  },
  computed: {
    filteredRents() {
      return this.rents.filter(rent => {
        if (this.filters.contract_status && rent.contract_status !== this.filters.contract_status) {
          return false
        }
        return true
      })
    }
  },
  async mounted() {
    await this.loadRents()
    await this.loadClients()
    await this.loadEquipment()
  },
  methods: {
    async loadRents() {
      this.loading = true
      this.error = null
      try {
        this.rents = await rentService.getRents({ is_active: true })
        this.calculateStats()
      } catch (err) {
        this.error = err.message
        console.error('Error loading rents:', err)
      } finally {
        this.loading = false
      }
    },

    async loadClients() {
      try {
        this.clients = await clientService.getClients()
      } catch (err) {
        console.error('Error loading clients:', err)
      }
    },

    async loadEquipment() {
      try {
        // Cargar solo equipos disponibles (no en renta activa)
        const allEquipment = await equipmentService.getEquipment()
        this.availableEquipment = allEquipment.filter(eq => eq.status === 'disponible' || !eq.status)
      } catch (err) {
        console.error('Error loading equipment:', err)
      }
    },

    calculateStats() {
      this.stats.active = this.rents.filter(r => r.contract_status === 'vigente').length
      this.stats.monthlyIncome = this.rents.reduce((sum, r) => sum + parseFloat(r.rent || 0), 0)
      this.stats.expiringSoon = this.rents.filter(r => r.contract_status === 'vencido' || r.contract_status === 'sin_firmar').length
    },

    getStatusClass(status) {
      const classes = {
        'vigente': 'bg-green-100 text-green-800',
        'pendiente': 'bg-yellow-100 text-yellow-800',
        'sin_firmar': 'bg-orange-100 text-orange-800',
        'vencido': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },

    getStatusLabel(status) {
      const labels = {
        'vigente': 'Vigente',
        'pendiente': 'Pendiente',
        'sin_firmar': 'Sin Firmar',
        'vencido': 'Vencido'
      }
      return labels[status] || status
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
      }).format(amount)
    },

    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('es-MX')
    },

    viewRent(rent) {
      this.selectedRent = rent
      this.showModal = true
    },

    async updateStatus(rentId, newStatus) {
      try {
        await rentService.updateContractStatus(rentId, newStatus)
        await this.loadRents()
      } catch (err) {
        alert('Error al actualizar estado: ' + err.message)
      }
    },

    async cancelRent(rentId) {
      if (!confirm('¿Está seguro de cancelar esta renta?')) return
      try {
        await rentService.deleteRent(rentId)
        await this.loadRents()
      } catch (err) {
        alert('Error al cancelar renta: ' + err.message)
      }
    },

    openNewRentModal() {
      this.selectedRent = null
      this.showModal = true
      // Recargar listas al abrir el modal (sin esperar)
      this.loadClients()
      this.loadEquipment()
    },

    closeModal() {
      this.showModal = false
      this.selectedRent = null
      this.rentForm = {
        client_id: '',
        equipment_id: '',
        contract_number: '',
        rent: '',
        contract_status: 'pendiente',
        is_foreign: false
      }
    },

    async createRent() {
      try {
        // Validar campos requeridos
        if (!this.rentForm.client_id) {
          alert('Por favor selecciona un cliente')
          return
        }
        
        if (!this.rentForm.equipment_id) {
          alert('Por favor selecciona un equipo')
          return
        }
        
        if (!this.rentForm.rent || parseFloat(this.rentForm.rent) <= 0) {
          alert('Por favor ingresa una renta mensual válida')
          return
        }
        
        const data = {
          client_id: parseInt(this.rentForm.client_id),
          item_id: parseInt(this.rentForm.equipment_id), // Backend espera 'item_id' no 'equipment_id'
          rent: parseFloat(this.rentForm.rent),
          contract_status: this.rentForm.contract_status,
          is_foreign: this.rentForm.is_foreign
        }
        
        await rentService.createRent(data)
        await this.loadRents()
        this.closeModal()
        alert('Renta creada exitosamente')
      } catch (err) {
        console.error('Error creating rent:', err)
        console.error('Error response:', err.response)
        
        // Manejar errores de validación de FastAPI (422)
        let errorMessage = 'Error desconocido al crear renta'
        
        if (err.response?.data) {
          const errorData = err.response.data
          
          // Si es un error de validación con detalles
          if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail.map(e => `${e.loc?.join('.') || 'campo'}: ${e.msg}`).join('\n')
          } 
          // Si es un string simple
          else if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail
          }
          // Si tiene un mensaje general
          else if (errorData.message) {
            errorMessage = errorData.message
          }
          // Último recurso
          else {
            errorMessage = JSON.stringify(errorData)
          }
        } else if (err.message) {
          errorMessage = err.message
        }
        
        alert('Error al crear renta:\n' + errorMessage)
      }
    },

    goToNewRent() {
      this.$router.push('/comercial/rentas/nueva')
    },

    goToDetail(rentId) {
      this.$router.push(`/comercial/rentas/${rentId}`)
    },

    goToEditRent(rentId) {
      this.$router.push(`/comercial/rentas/editar/${rentId}`)
    }
  }
}
</script>