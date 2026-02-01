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
          Volver a Ventas
        </button>
        <h1 class="text-3xl font-bold text-gray-900">
          {{ isEditing ? 'Editar Venta' : 'Nueva Venta' }}
        </h1>
        <p class="text-gray-600 mt-2">
          {{ isEditing ? 'Actualiza la información de la venta' : 'Registra una nueva venta de equipo' }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mx-auto"></div>
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
            <select v-model="saleForm.client_id" required class="input-field">
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
            <select v-model="saleForm.item_id" required class="input-field">
              <option value="">Seleccionar equipo...</option>
              <option 
                v-for="item in equipment" 
                :key="item.item_id" 
                :value="item.item_id"
                :disabled="item.location_status !== 'bodega' && item.item_id !== saleForm.item_id"
                :class="{ 'text-gray-400': item.location_status !== 'bodega' && item.item_id !== saleForm.item_id }"
              >
                {{ item.sku }} - {{ item.model }} (Serie: {{ item.serie }}) 
                <template v-if="item.location_status === 'bodega'">✓ Disponible</template>
                <template v-else-if="item.location_status === 'rentado'">🔒 Rentado</template>
                <template v-else-if="item.location_status === 'vendido'">🔒 Vendido</template>
                <template v-else>⚠️ {{ item.location_status }}</template>
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Solo equipos en bodega están disponibles para venta</p>
          </div>

          <!-- Precio de Venta -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Precio de Venta *
            </label>
            <input 
              v-model="saleForm.sale_price" 
              type="number" 
              step="0.01" 
              required 
              class="input-field" 
              placeholder="0.00"
            >
          </div>

          <!-- Estado -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Estado
            </label>
            <select v-model="saleForm.sale_status" class="input-field">
              <option value="pendiente">Pendiente</option>
              <option value="confirmada">Confirmada</option>
              <option value="entregada">Entregada</option>
            </select>
          </div>

          <!-- Servicio Foráneo -->
          <div class="md:col-span-2">
            <label class="flex items-center">
              <input v-model="saleForm.is_foreign" type="checkbox" class="mr-2">
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
            class="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 font-medium disabled:opacity-50"
          >
            {{ isEditing ? 'Guardar Cambios' : 'Crear Venta' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { saleService } from '@/services/saleService.ts'
import { clientService } from '@/services/clientService.ts'
import { equipmentService } from '@/services/equipmentService.ts'

export default {
  name: 'VentaFormView',
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
      saleForm: {
        client_id: '',
        item_id: '',
        sale_price: '',
        sale_status: 'pendiente',
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
      await this.loadSale()
    }
  },
  methods: {
    async loadInitialData() {
      this.loading = true
      try {
        const [clientsRes, equipmentRes] = await Promise.all([
          clientService.getClients({ pageSize: 100 }),
          equipmentService.getEquipments({ pageSize: 100 })
        ])
        this.clients = clientsRes.items || []
        this.equipment = equipmentRes.items || []
      } catch (err) {
        this.errorMsg = 'Error al cargar datos: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async loadSale() {
      this.loading = true
      try {
        const sale = await saleService.getSaleById(this.$route.params.id)
        this.saleForm = {
          client_id: sale.client_id || '',
          item_id: sale.item_id || '',
          sale_price: sale.sale_price || '',
          sale_status: sale.sale_status || 'pendiente',
          is_foreign: sale.is_foreign || false
        }
      } catch (err) {
        this.errorMsg = 'Error al cargar la venta: ' + err.message
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
          client_id: parseInt(this.saleForm.client_id),
          item_id: parseInt(this.saleForm.item_id),
          sale_price: parseFloat(this.saleForm.sale_price),
          sale_status: this.saleForm.sale_status,
          is_foreign: this.saleForm.is_foreign
        }

        if (this.isEditing) {
          await saleService.updateSale(this.$route.params.id, data)
          this.successMsg = 'Venta actualizada exitosamente'
        } else {
          await saleService.createSale(data)
          this.successMsg = 'Venta creada exitosamente'
        }

        setTimeout(() => {
          this.$router.push('/ventas')
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
        this.$router.push('/ventas')
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
  border-color: #10b981;
  ring: 2px;
  ring-color: #10b98180;
}
</style>
