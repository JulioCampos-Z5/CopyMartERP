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
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalActive }}</p>
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
              <p class="text-2xl font-semibold text-gray-900">${{ stats.totalMonthlyRent.toLocaleString() }}</p>
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
              <h3 class="text-sm font-medium text-gray-500">Contratos Vigentes</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.vigentes }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Pendientes</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.pendientes }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <button @click="openCreateModal" class="btn-primary">
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
          <!-- Filtros -->
          <select v-model="filters.contract_status" @change="loadRents" class="border rounded-lg px-3 py-2">
            <option value="">Todos los estados</option>
            <option value="pendiente">Pendiente</option>
            <option value="sin_firmar">Sin Firmar</option>
            <option value="vigente">Vigente</option>
            <option value="vencido">Vencido</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Main Content -->
      <div v-else class="bg-white rounded-lg shadow border">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Contratos de Renta</h2>
        </div>
        <div class="p-6">
          <div v-if="rents.length === 0" class="text-center py-8 text-gray-500">
            No hay rentas registradas
          </div>
          <div v-else class="overflow-x-auto">
            <table class="min-w-full table-auto">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contrato</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sucursal / Área</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Equipo</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Renta</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Foráneo</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="rent in rents" :key="rent.rent_id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ rent.contract_number || 'Sin asignar' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ rent.client?.name || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div>{{ rent.branch?.name || '-' }}</div>
                    <div class="text-xs text-gray-500">{{ rent.area?.name || '' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div>{{ rent.equipment?.model || 'N/A' }}</div>
                    <div class="text-xs text-gray-500">Serie: {{ rent.equipment?.serie || '' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusClass(rent.contract_status)" class="px-2 py-1 text-xs font-medium rounded-full">
                      {{ getStatusLabel(rent.contract_status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    ${{ rent.rent?.toLocaleString() }}/mes
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span v-if="rent.is_foreign" class="text-orange-600">Sí</span>
                    <span v-else class="text-gray-400">No</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button @click="viewRent(rent)" class="text-blue-600 hover:text-blue-900 mr-3">Ver</button>
                    <button @click="editRent(rent)" class="text-green-600 hover:text-green-900 mr-3">Editar</button>
                    <button @click="confirmDelete(rent)" class="text-red-600 hover:text-red-900">Eliminar</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Crear/Editar Renta -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-screen overflow-y-auto">
        <h3 class="text-lg font-semibold mb-4">{{ isEditing ? 'Editar Renta' : 'Nueva Renta' }}</h3>
        
        <form @submit.prevent="saveRent" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Cliente *</label>
            <select v-model="form.client_id" required class="mt-1 w-full border rounded-lg px-3 py-2" @change="loadBranches">
              <option value="">Seleccionar cliente</option>
              <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                {{ client.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Sucursal</label>
            <select v-model="form.branch_id" class="mt-1 w-full border rounded-lg px-3 py-2" @change="loadAreas">
              <option value="">Sin sucursal</option>
              <option v-for="branch in branches" :key="branch.branch_id" :value="branch.branch_id">
                {{ branch.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Área</label>
            <select v-model="form.area_id" class="mt-1 w-full border rounded-lg px-3 py-2">
              <option value="">Sin área</option>
              <option v-for="area in areas" :key="area.area_id" :value="area.area_id">
                {{ area.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Equipo *</label>
            <select v-model="form.item_id" required class="mt-1 w-full border rounded-lg px-3 py-2">
              <option value="">Seleccionar equipo</option>
              <option v-for="item in equipment" :key="item.item_id" :value="item.item_id">
                {{ item.model }} - {{ item.serie }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Renta Mensual *</label>
            <input v-model.number="form.rent" type="number" step="0.01" min="0" required 
                   class="mt-1 w-full border rounded-lg px-3 py-2" placeholder="0.00">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Estado del Contrato</label>
            <select v-model="form.contract_status" class="mt-1 w-full border rounded-lg px-3 py-2">
              <option value="pendiente">Pendiente</option>
              <option value="sin_firmar">Sin Firmar</option>
              <option value="vigente">Vigente</option>
              <option value="vencido">Vencido</option>
            </select>
          </div>

          <div class="flex items-center">
            <input v-model="form.is_foreign" type="checkbox" class="mr-2">
            <label class="text-sm text-gray-700">Servicio Foráneo</label>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="closeModal" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              {{ isEditing ? 'Guardar' : 'Crear' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Confirmar Eliminación -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">Confirmar Eliminación</h3>
        <p class="text-gray-600 mb-6">¿Estás seguro de que deseas eliminar esta renta? El equipo será devuelto a bodega.</p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button @click="deleteRent" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
            Eliminar
          </button>
        </div>
      </div>
    </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import rentService from '@/services/rentService'
import clientService from '@/services/clientService'
import equipmentService from '@/services/equipmentService'

export default {
  name: 'RentasView',
  components: {
    BaseLayout
  },
  data() {
    return {
      rents: [],
      clients: [],
      branches: [],
      areas: [],
      equipment: [],
      loading: false,
      showModal: false,
      showDeleteModal: false,
      isEditing: false,
      selectedRent: null,
      filters: {
        contract_status: '',
        is_active: true
      },
      form: {
        client_id: '',
        branch_id: '',
        area_id: '',
        item_id: '',
        rent: 0,
        contract_status: 'pendiente',
        is_foreign: false
      },
      stats: {
        totalActive: 0,
        totalMonthlyRent: 0,
        vigentes: 0,
        pendientes: 0
      }
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
      try {
        const filters = { ...this.filters }
        if (!filters.contract_status) delete filters.contract_status
        
        this.rents = await rentService.getRents(filters)
        this.calculateStats()
      } catch (error) {
        console.error('Error al cargar rentas:', error)
      } finally {
        this.loading = false
      }
    },
    
    calculateStats() {
      this.stats.totalActive = this.rents.length
      this.stats.totalMonthlyRent = this.rents
        .filter(r => r.contract_status === 'vigente')
        .reduce((sum, r) => sum + (r.rent || 0), 0)
      this.stats.vigentes = this.rents.filter(r => r.contract_status === 'vigente').length
      this.stats.pendientes = this.rents.filter(r => r.contract_status === 'pendiente').length
    },
    
    async loadClients() {
      try {
        this.clients = await clientService.getClients()
      } catch (error) {
        console.error('Error al cargar clientes:', error)
      }
    },
    
    async loadEquipment() {
      try {
        const response = await equipmentService.getEquipment()
        // Filtrar solo equipos disponibles (en bodega)
        this.equipment = response.filter(e => e.location_status === 'bodega')
      } catch (error) {
        console.error('Error al cargar equipos:', error)
      }
    },
    
    async loadBranches() {
      if (!this.form.client_id) {
        this.branches = []
        this.areas = []
        return
      }
      try {
        this.branches = await clientService.getBranches(this.form.client_id)
        this.form.branch_id = ''
        this.form.area_id = ''
        this.areas = []
      } catch (error) {
        console.error('Error al cargar sucursales:', error)
      }
    },
    
    async loadAreas() {
      if (!this.form.branch_id || !this.form.client_id) {
        this.areas = []
        return
      }
      try {
        this.areas = await clientService.getAreas(this.form.client_id, this.form.branch_id)
        this.form.area_id = ''
      } catch (error) {
        console.error('Error al cargar áreas:', error)
      }
    },
    
    getStatusClass(status) {
      const classes = {
        'pendiente': 'bg-yellow-100 text-yellow-800',
        'sin_firmar': 'bg-orange-100 text-orange-800',
        'vigente': 'bg-green-100 text-green-800',
        'vencido': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    
    getStatusLabel(status) {
      const labels = {
        'pendiente': 'Pendiente',
        'sin_firmar': 'Sin Firmar',
        'vigente': 'Vigente',
        'vencido': 'Vencido'
      }
      return labels[status] || status
    },
    
    openCreateModal() {
      this.isEditing = false
      this.form = {
        client_id: '',
        branch_id: '',
        area_id: '',
        item_id: '',
        rent: 0,
        contract_status: 'pendiente',
        is_foreign: false
      }
      this.branches = []
      this.areas = []
      this.showModal = true
    },
    
    async editRent(rent) {
      this.isEditing = true
      this.selectedRent = rent
      this.form = {
        client_id: rent.client_id,
        branch_id: rent.branch_id || '',
        area_id: rent.area_id || '',
        item_id: rent.item_id,
        rent: rent.rent,
        contract_status: rent.contract_status,
        is_foreign: rent.is_foreign
      }
      
      if (rent.client_id) await this.loadBranches()
      if (rent.branch_id) await this.loadAreas()
      
      this.showModal = true
    },
    
    viewRent(rent) {
      // Por ahora solo muestra en consola, se puede expandir
      console.log('Ver renta:', rent)
      alert(`Contrato: ${rent.contract_number}\nCliente: ${rent.client?.name}\nRenta: $${rent.rent}/mes`)
    },
    
    confirmDelete(rent) {
      this.selectedRent = rent
      this.showDeleteModal = true
    },
    
    async saveRent() {
      try {
        const data = {
          ...this.form,
          client_id: Number(this.form.client_id),
          item_id: Number(this.form.item_id),
          branch_id: this.form.branch_id ? Number(this.form.branch_id) : null,
          area_id: this.form.area_id ? Number(this.form.area_id) : null,
          rent: Number(this.form.rent)
        }
        
        if (this.isEditing) {
          await rentService.updateRent(this.selectedRent.rent_id, data)
        } else {
          await rentService.createRent(data)
        }
        
        this.closeModal()
        await this.loadRents()
        await this.loadEquipment() // Recargar equipos disponibles
      } catch (error) {
        console.error('Error al guardar renta:', error)
        alert('Error al guardar: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    async deleteRent() {
      try {
        await rentService.deleteRent(this.selectedRent.rent_id)
        this.showDeleteModal = false
        await this.loadRents()
        await this.loadEquipment()
      } catch (error) {
        console.error('Error al eliminar renta:', error)
        alert('Error al eliminar: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.selectedRent = null
    }
  }
}
</script>