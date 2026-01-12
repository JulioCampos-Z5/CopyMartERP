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

          <!-- Equipo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Equipo *
            </label>
            <select v-model="rentForm.item_id" required class="input-field">
              <option value="">Seleccionar equipo...</option>
              <option v-for="item in equipment" :key="item.item_id" :value="item.item_id">
                {{ item.sku }} - {{ item.model }} (Serie: {{ item.serie }})
              </option>
            </select>
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
      rentForm: {
        client_id: '',
        item_id: '',
        rent: '',
        contract_status: 'pendiente',
        is_foreign: false
      }
    }
  },
  computed: {
    isEditing() {
      return this.$route.params.id !== undefined
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
          clientService.getAllClients(),
          equipmentService.getAllEquipment()
        ])
        this.clients = clientsRes.data || []
        this.equipment = equipmentRes.data || []
      } catch (err) {
        this.errorMsg = 'Error al cargar datos: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async loadRent() {
      this.loading = true
      try {
        const response = await rentService.getRentById(this.$route.params.id)
        const rent = response.data
        this.rentForm = {
          client_id: rent.client_id || '',
          item_id: rent.item_id || '',
          rent: rent.rent || '',
          contract_status: rent.contract_status || 'pendiente',
          is_foreign: rent.is_foreign || false
        }
      } catch (err) {
        this.errorMsg = 'Error al cargar la renta: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async handleSubmit() {
      this.loading = true
      this.errorMsg = null
      this.successMsg = null

      try {
        const data = {
          client_id: parseInt(this.rentForm.client_id),
          item_id: parseInt(this.rentForm.item_id),
          rent: parseFloat(this.rentForm.rent),
          contract_status: this.rentForm.contract_status,
          is_foreign: this.rentForm.is_foreign
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
