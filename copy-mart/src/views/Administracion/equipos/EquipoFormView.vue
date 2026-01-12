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
          Volver a Inventario
        </button>
        <h1 class="text-3xl font-bold text-gray-900">
          {{ isEditing ? 'Editar Equipo' : 'Nuevo Equipo' }}
        </h1>
        <p class="text-gray-600 mt-2">
          {{ isEditing ? 'Actualiza la información del equipo' : 'Registra un nuevo equipo en el inventario' }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
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
          <!-- Marca -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Marca *
            </label>
            <select v-model="equipmentForm.brand_id" required class="input-field">
              <option :value="null">Seleccionar marca...</option>
              <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                {{ brand.name }}
              </option>
            </select>
          </div>

          <!-- Modelo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Modelo *
            </label>
            <input 
              v-model="equipmentForm.model" 
              type="text" 
              required 
              class="input-field"
              placeholder="Ej: LaserJet Pro M404"
            >
          </div>

          <!-- Número de Serie -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Número de Serie *
            </label>
            <input 
              v-model="equipmentForm.serie" 
              type="text" 
              required 
              class="input-field"
              placeholder="Ej: SN123456789"
            >
          </div>

          <!-- Modelo de Toner -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Modelo de Toner *
            </label>
            <input 
              v-model="equipmentForm.model_toner" 
              type="text" 
              required 
              class="input-field"
              placeholder="Ej: CF259A"
            >
          </div>

          <!-- Tipo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Tipo *
            </label>
            <select v-model="equipmentForm.type" required class="input-field">
              <option value="monocromo">Monocromo</option>
              <option value="color">Color</option>
            </select>
          </div>

          <!-- Proveedor -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Proveedor *
            </label>
            <select v-model="equipmentForm.supplier_id" required class="input-field">
              <option :value="null">Seleccionar proveedor...</option>
              <option v-for="supplier in suppliers" :key="supplier.supplier_id" :value="supplier.supplier_id">
                {{ supplier.name }}
              </option>
            </select>
          </div>

          <!-- Factura -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Factura
            </label>
            <input 
              v-model="equipmentForm.invoice" 
              type="text" 
              class="input-field"
              placeholder="Número de factura"
            >
          </div>

          <!-- Costo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Costo
            </label>
            <input 
              v-model="equipmentForm.cost" 
              type="number" 
              step="0.01" 
              class="input-field"
              placeholder="0.00"
            >
          </div>

          <!-- Estado de Ubicación -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Estado de Ubicación *
            </label>
            <select v-model="equipmentForm.location_status" required class="input-field">
              <option value="bodega">Bodega</option>
              <option value="asignado">Asignado</option>
              <option value="vendido">Vendido</option>
              <option value="taller">Taller</option>
              <option value="desconocido">Desconocido</option>
            </select>
          </div>

          <!-- Comentarios -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Comentarios
            </label>
            <textarea 
              v-model="equipmentForm.comments" 
              rows="3" 
              class="input-field"
              placeholder="Notas adicionales sobre el equipo..."
            ></textarea>
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
            class="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 font-medium disabled:opacity-50"
          >
            {{ isEditing ? 'Guardar Cambios' : 'Crear Equipo' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { equipmentService } from '@/services/equipmentService.ts'

export default {
  name: 'EquipoFormView',
  components: {
    AppNavigation
  },
  data() {
    return {
      loading: false,
      errorMsg: null,
      successMsg: null,
      brands: [],
      suppliers: [],
      equipmentForm: {
        brand_id: null,
        model: '',
        serie: '',
        model_toner: '',
        type: 'monocromo',
        supplier_id: null,
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: ''
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
      await this.loadEquipment()
    }
  },
  methods: {
    async loadInitialData() {
      this.loading = true
      try {
        const [brands, suppliers] = await Promise.all([
          equipmentService.getBrands(),
          equipmentService.getSuppliers()
        ])
        this.brands = brands || []
        this.suppliers = suppliers || []
      } catch (err) {
        this.errorMsg = 'Error al cargar datos: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async loadEquipment() {
      this.loading = true
      try {
        const equipment = await equipmentService.getEquipmentById(this.$route.params.id)
        this.equipmentForm = {
          brand_id: equipment.brand_id || null,
          model: equipment.model || '',
          serie: equipment.serie || '',
          model_toner: equipment.model_toner || '',
          type: equipment.type || 'monocromo',
          supplier_id: equipment.supplier_id || null,
          invoice: equipment.invoice || '',
          cost: equipment.cost || null,
          location_status: equipment.location_status || 'bodega',
          comments: equipment.comments || ''
        }
      } catch (err) {
        this.errorMsg = 'Error al cargar el equipo: ' + err.message
      } finally {
        this.loading = false
      }
    },

    async handleSubmit() {
      this.loading = true
      this.errorMsg = null
      this.successMsg = null

      try {
        if (this.isEditing) {
          await equipmentService.updateEquipment(this.$route.params.id, this.equipmentForm)
          this.successMsg = 'Equipo actualizado exitosamente'
        } else {
          await equipmentService.createEquipment(this.equipmentForm)
          this.successMsg = 'Equipo creado exitosamente'
        }

        setTimeout(() => {
          this.$router.push('/inventario')
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
        this.$router.push('/inventario')
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
  border-color: #9333ea;
  ring: 2px;
  ring-color: #9333ea80;
}
</style>
