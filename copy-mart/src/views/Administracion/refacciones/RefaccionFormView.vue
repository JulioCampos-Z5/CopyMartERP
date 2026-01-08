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
          {{ isEditing ? 'Editar Refacción' : 'Nueva Refacción' }}
        </h1>
        <p class="text-gray-600 mt-2">
          {{ isEditing ? 'Actualiza la información de la refacción' : 'Registra una nueva refacción en el inventario' }}
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
          <!-- Código -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Código
            </label>
            <input 
              v-model="sparepartForm.code" 
              type="text" 
              class="input-field"
              placeholder="REF-001"
            >
          </div>

          <!-- Nombre -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Nombre *
            </label>
            <input 
              v-model="sparepartForm.name" 
              type="text" 
              required 
              class="input-field"
              placeholder="Ej: Toner HP 85A"
            >
          </div>

          <!-- Marca -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Marca
            </label>
            <input 
              v-model="sparepartForm.brand" 
              type="text" 
              class="input-field"
              placeholder="Ej: HP"
            >
          </div>

          <!-- Color -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Color
            </label>
            <select v-model="sparepartForm.color" class="input-field">
              <option value="">Seleccionar...</option>
              <option value="K">Negro (K)</option>
              <option value="C">Cyan (C)</option>
              <option value="M">Magenta (M)</option>
              <option value="Y">Amarillo (Y)</option>
              <option value="COLOR">Color</option>
              <option value="NA">N/A</option>
            </select>
          </div>

          <!-- Equipo Compatible -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Equipo Compatible
            </label>
            <input 
              v-model="sparepartForm.equipment" 
              type="text" 
              class="input-field"
              placeholder="Ej: LaserJet Pro M404"
            >
          </div>

          <!-- Proveedor -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Proveedor
            </label>
            <input 
              v-model="sparepartForm.supplier" 
              type="text" 
              class="input-field"
              placeholder="Ej: KONICA"
            >
          </div>

          <!-- Descripción -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Descripción
            </label>
            <textarea 
              v-model="sparepartForm.description" 
              rows="3" 
              class="input-field"
              placeholder="Descripción detallada de la refacción..."
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
            {{ isEditing ? 'Guardar Cambios' : 'Crear Refacción' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { sparepartService } from '@/services/sparepartService'

export default {
  name: 'RefaccionFormView',
  components: {
    AppNavigation
  },
  data() {
    return {
      loading: false,
      errorMsg: null,
      successMsg: null,
      sparepartForm: {
        code: '',
        name: '',
        description: '',
        color: '',
        brand: '',
        equipment: '',
        supplier: ''
      }
    }
  },
  computed: {
    isEditing() {
      return this.$route.params.id !== undefined
    }
  },
  async mounted() {
    if (this.isEditing) {
      await this.loadSparepart()
    }
  },
  methods: {
    async loadSparepart() {
      this.loading = true
      try {
        const sparepart = await sparepartService.getSparepartById(this.$route.params.id)
        this.sparepartForm = {
          code: sparepart.code || '',
          name: sparepart.name || '',
          description: sparepart.description || '',
          color: sparepart.color || '',
          brand: sparepart.brand || '',
          equipment: sparepart.equipment || '',
          supplier: sparepart.supplier || ''
        }
      } catch (err) {
        this.errorMsg = 'Error al cargar la refacción: ' + err.message
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
          await sparepartService.updateSparepart(this.$route.params.id, this.sparepartForm)
          this.successMsg = 'Refacción actualizada exitosamente'
        } else {
          await sparepartService.createSparepart(this.sparepartForm)
          this.successMsg = 'Refacción creada exitosamente'
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
