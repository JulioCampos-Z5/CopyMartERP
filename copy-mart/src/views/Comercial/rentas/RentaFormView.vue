<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Volver a Rentas
        </button>
        <h1 class="text-3xl font-bold text-gray-900">
          {{ isEditing ? 'Editar Renta' : 'Nueva Renta' }}
        </h1>
        <p class="text-gray-600 mt-2">
          {{ isEditing ? 'Actualiza la información de la renta' : 'Registra un nuevo contrato de renta de equipo' }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando datos...</p>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMsg" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
        {{ errorMsg }}
      </div>

      <!-- Success Alert -->
      <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6">
        {{ successMsg }}
      </div>

      <!-- Form -->
      <form v-if="!loading" @submit.prevent="handleSubmit" class="bg-white shadow rounded-lg p-6 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Cliente -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Cliente *
            </label>
            <select v-model="rentForm.client_id" required class="input-field">
              <option value="">Seleccionar cliente...</option>
              <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                {{ client.name }}
              </option>
            </select>
          </div>

          <!-- Sucursal -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Sucursal <span v-if="branches.length > 0">*</span>
            </label>
            <select v-model="rentForm.branch_id" :disabled="!rentForm.client_id" :required="branches.length > 0" class="input-field">
              <option value="">Seleccionar sucursal...</option>
              <option v-for="branch in branches" :key="branch.branch_id" :value="branch.branch_id">
                {{ branch.name }}<span v-if="branch.is_main"> (Principal)</span>
              </option>
            </select>
          </div>

          <!-- Equipo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Equipo *
            </label>
            <select v-model="rentForm.item_id" required class="input-field">
              <option value="">Seleccionar equipo...</option>
              <option 
                v-for="item in equipment" 
                :key="item.item_id" 
                :value="item.item_id"
                :disabled="item.location_status !== 'bodega' && item.item_id !== rentForm.item_id"
                :class="{ 'text-gray-400': item.location_status !== 'bodega' && item.item_id !== rentForm.item_id }"
              >
                {{ item.sku }} - {{ item.model }} (Serie: {{ item.serie }}) 
                <template v-if="item.location_status === 'bodega'">✓ Disponible</template>
                <template v-else-if="item.location_status === 'rentado'">🔒 Rentado</template>
                <template v-else-if="item.location_status === 'vendido'">🔒 Vendido</template>
                <template v-else>⚠️ {{ item.location_status }}</template>
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Solo equipos en bodega están disponibles para renta</p>
          </div>

          <!-- Renta Mensual -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Renta Mensual *
            </label>
            <input 
              v-model="rentForm.rent" 
              type="number" 
              step="0.01" 
              required 
              class="input-field" 
              placeholder="0.00"
            >
          </div>

          <!-- Fecha de Inicio -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Fecha de Inicio *
            </label>
            <input 
              v-model="rentForm.start_date" 
              type="date" 
              required 
              class="input-field"
            >
          </div>

          <!-- Estado del Contrato -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Estado del Contrato
            </label>
            <select v-model="rentForm.contract_status" class="input-field">
              <option value="pendiente">Pendiente</option>
              <option value="vigente">Vigente</option>
              <option value="sin_firmar">Sin Firmar</option>
              <option value="vencido">Vencido</option>
            </select>
          </div>

          <!-- Servicio Foráneo -->
          <div class="md:col-span-2">
            <label class="flex items-center">
              <input v-model="rentForm.is_foreign" type="checkbox" class="mr-2">
              <span class="text-sm text-gray-700">Servicio Foráneo</span>
            </label>
          </div>

          <!-- Servicio de Impresión -->
          <div class="md:col-span-2 border-t pt-4 mt-4">
            <label class="flex items-center mb-4">
              <input v-model="rentForm.has_print_service" type="checkbox" class="mr-2">
              <span class="text-sm font-medium text-gray-700">Incluye Servicio de Impresión</span>
            </label>

            <div v-if="rentForm.has_print_service" class="grid grid-cols-1 md:grid-cols-2 gap-4 pl-6 border-l-2 border-blue-200">
              <!-- Contadores B/N -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Impresiones B/N Incluidas *
                </label>
                <input 
                  v-model.number="rentForm.bn_included" 
                  type="number" 
                  min="0"
                  :required="rentForm.has_print_service"
                  class="input-field" 
                  placeholder="ej: 1000"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Costo Exceso B/N (por página) *
                </label>
                <input 
                  v-model.number="rentForm.bn_cost_per_excess" 
                  type="number" 
                  step="0.0001"
                  min="0"
                  :required="rentForm.has_print_service"
                  class="input-field" 
                  placeholder="ej: 0.50"
                >
              </div>

              <!-- Contadores Color -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Impresiones Color Incluidas *
                </label>
                <input 
                  v-model.number="rentForm.color_included" 
                  type="number" 
                  min="0"
                  :required="rentForm.has_print_service"
                  class="input-field" 
                  placeholder="ej: 500"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Costo Exceso Color (por página) *
                </label>
                <input 
                  v-model.number="rentForm.color_cost_per_excess" 
                  type="number" 
                  step="0.0001"
                  min="0"
                  :required="rentForm.has_print_service"
                  class="input-field" 
                  placeholder="ej: 1.50"
                >
              </div>

              <!-- Notas de Impresión -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Notas sobre Impresión
                </label>
                <textarea 
                  v-model="rentForm.print_notes" 
                  rows="3"
                  class="input-field" 
                  placeholder="Información adicional sobre el servicio de impresión..."
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex gap-4 justify-end pt-6 border-t">
          <button type="button" @click="goBack" class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium">
            Cancelar
          </button>
          <button 
            type="submit" 
            :disabled="loading" 
            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium disabled:opacity-50"
          >
            {{ isEditing ? 'Guardar Cambios' : 'Crear Renta' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { rentService } from '@/services/rentService.ts'
import { clientService } from '@/services/clientService.ts'
import { equipmentService } from '@/services/equipmentService.ts'

export default {
  name: 'RentaFormView',
  components: {
    AppNavigation
  },
  data() {
    return {
      loading: false,
      errorMsg: null,
      successMsg: null,
      clients: [],
      equipment: [],
      branches: [],
      rentForm: {
        client_id: '',
        branch_id: '',
        item_id: '',
        rent: '',
        start_date: new Date().toISOString().split('T')[0],
        contract_status: 'pendiente',
        is_foreign: false,
        has_print_service: false,
        bn_included: 0,
        bn_cost_per_excess: 0,
        color_included: 0,
        color_cost_per_excess: 0,
        print_notes: ''
      }
    }
  },
  computed: {
    isEditing() {
      return this.$route.params.id !== undefined
    }
  },
  watch: {
    'rentForm.client_id': {
      handler(newVal) {
        this.rentForm.branch_id = ''
        if (newVal) {
          this.loadBranches(parseInt(newVal))
        } else {
          this.branches = []
        }
      }
    }
  },
  async mounted() {
    await this.loadInitialData()
    if (this.isEditing) {
      await this.loadRent()
    }
  },
  methods: {
    async loadInitialData() {
      this.loading = true
      try {
        const [clientsRes, equipmentRes] = await Promise.all([
          clientService.getClients({ pageSize: 100, is_active: true }),
          equipmentService.getEquipments({ pageSize: 100, is_active: true })
        ])
        this.clients = clientsRes.items || []
        this.equipment = equipmentRes.items || []
      } catch (err) {
        this.errorMsg = 'Error al cargar datos: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async loadRent() {
      this.loading = true
      try {
        const rent = await rentService.getRentById(this.$route.params.id)
        this.rentForm = {
          client_id: rent.client_id || '',
          branch_id: '',
          item_id: rent.item_id || '',
          rent: rent.rent || '',
          start_date: rent.start_date || new Date().toISOString().split('T')[0],
          contract_status: rent.contract_status || 'pendiente',
          is_foreign: rent.is_foreign || false,
          has_print_service: rent.has_print_service || false,
          bn_included: rent.bn_included || 0,
          bn_cost_per_excess: rent.bn_cost_per_excess || 0,
          color_included: rent.color_included || 0,
          color_cost_per_excess: rent.color_cost_per_excess || 0,
          print_notes: rent.print_notes || ''
        }

        if (rent.client_id) {
          await this.loadBranches(rent.client_id)
          if (rent.branch_id) {
            this.rentForm.branch_id = String(rent.branch_id)
          }
        }
      } catch (err) {
        this.errorMsg = 'Error al cargar la renta: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async loadBranches(clientId) {
      try {
        const branches = await clientService.getClientBranches(clientId)
        this.branches = branches || []
      } catch (err) {
        this.errorMsg = 'Error al cargar sucursales: ' + err.message
        this.branches = []
      }
    },

    async handleSubmit() {
      this.loading = true
      this.errorMsg = null
      this.successMsg = null

      try {
        if (this.branches.length > 0 && !this.rentForm.branch_id) {
          this.errorMsg = 'Por favor selecciona una sucursal'
          return
        }

        const data = {
          client_id: parseInt(this.rentForm.client_id),
          branch_id: this.rentForm.branch_id ? parseInt(this.rentForm.branch_id) : null,
          item_id: parseInt(this.rentForm.item_id),
          rent: parseFloat(this.rentForm.rent),
          start_date: this.rentForm.start_date,
          contract_status: this.rentForm.contract_status,
          is_foreign: this.rentForm.is_foreign,
          has_print_service: this.rentForm.has_print_service,
          bn_included: this.rentForm.has_print_service ? parseInt(this.rentForm.bn_included) : 0,
          bn_cost_per_excess: this.rentForm.has_print_service ? parseFloat(this.rentForm.bn_cost_per_excess) : 0,
          color_included: this.rentForm.has_print_service ? parseInt(this.rentForm.color_included) : 0,
          color_cost_per_excess: this.rentForm.has_print_service ? parseFloat(this.rentForm.color_cost_per_excess) : 0,
          print_notes: this.rentForm.print_notes || null
        }

        if (this.isEditing) {
          await rentService.updateRent(this.$route.params.id, data)
          this.successMsg = 'Renta actualizada exitosamente'
        } else {
          await rentService.createRent(data)
          this.successMsg = 'Renta creada exitosamente'
        }

        setTimeout(() => {
          this.$router.push('/rentas')
        }, 1500)
      } catch (err) {
        this.errorMsg = 'Error al guardar: ' + (err.response?.data?.detail || err.message)
      } finally {
        this.loading = false
      }
    },

    goBack() {
      if (this.isEditing && window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/rentas')
      }
    }
  }
}
</script>

<style scoped>
.input-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  ring: 2px;
  ring-color: #3b82f680;
}
</style>
