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
          Volver a Clientes
        </button>
        <h1 class="text-3xl font-bold text-gray-900">{{ isEditing ? 'Editar Cliente' : 'Nuevo Cliente' }}</h1>
        <p class="text-gray-600 mt-2">{{ isEditing ? 'Actualiza la información del cliente' : 'Registra un nuevo cliente en el sistema' }}</p>
      </div>

      <!-- Formulario -->
      <form @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow-lg">
        <div class="p-6 space-y-8">
          <!-- Datos del Cliente -->
          <section>
            <div class="flex items-center mb-4">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-900">Datos del Cliente</h2>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Nombre / Razón Social <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="form.name" 
                  type="text" 
                  required 
                  class="input-field"
                  placeholder="Nombre completo o razón social"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">RFC</label>
                <input 
                  v-model="form.rfc" 
                  type="text" 
                  class="input-field"
                  placeholder="RFC del cliente"
                  maxlength="13"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Cliente</label>
                <select v-model="form.client_type" class="input-field">
                  <option value="empresa">Empresa</option>
                  <option value="persona">Persona Física</option>
                </select>
              </div>

              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
                <input 
                  v-model="form.address" 
                  type="text" 
                  class="input-field"
                  placeholder="Calle, número, colonia"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
                <input 
                  v-model="form.city" 
                  type="text" 
                  class="input-field"
                  placeholder="Ciudad"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
                <input 
                  v-model="form.state" 
                  type="text" 
                  class="input-field"
                  placeholder="Estado"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
                <input 
                  v-model="form.postal_code" 
                  type="text" 
                  class="input-field"
                  placeholder="00000"
                  maxlength="5"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Límite de Crédito</label>
                <input 
                  v-model.number="form.credit_limit" 
                  type="number" 
                  step="0.01" 
                  class="input-field"
                  placeholder="0.00"
                >
              </div>
            </div>
          </section>

          <!-- Datos de Contacto -->
          <section class="pt-4 border-t border-gray-200">
            <div class="flex items-center mb-4">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-900">Contacto Principal</h2>
            </div>
            
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <p class="text-sm text-blue-800">
                <strong>Nota:</strong> Los datos del contacto se guardarán automáticamente en el módulo de Contactos.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de Contacto</label>
                <input 
                  v-model="form.contact_name" 
                  type="text" 
                  class="input-field"
                  placeholder="Nombre del contacto principal"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Puesto / Rol</label>
                <input 
                  v-model="form.contact_rol" 
                  type="text" 
                  class="input-field"
                  placeholder="Ej. Gerente de Compras, TI, Contador"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input 
                  v-model="form.contact_email" 
                  type="email" 
                  class="input-field"
                  placeholder="contacto@ejemplo.com"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                <input 
                  v-model="form.contact_phone" 
                  type="tel" 
                  class="input-field"
                  placeholder="(000) 000-0000"
                >
              </div>
            </div>
          </section>
        </div>

        <!-- Footer con botones -->
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-end gap-3 rounded-b-lg">
          <button 
            type="button" 
            @click="goBack" 
            class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100 font-medium"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            :disabled="loading"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar Cliente' : 'Crear Cliente') }}
          </button>
        </div>
      </form>

      <!-- Alert de éxito/error -->
      <div v-if="alert.show" :class="['fixed top-20 right-4 max-w-md w-full shadow-lg rounded-lg p-4 z-50', alert.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200']">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg v-if="alert.type === 'success'" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-3 flex-1">
            <h3 :class="['text-sm font-medium', alert.type === 'success' ? 'text-green-800' : 'text-red-800']">
              {{ alert.title }}
            </h3>
            <p :class="['mt-1 text-sm', alert.type === 'success' ? 'text-green-700' : 'text-red-700']">
              {{ alert.message }}
            </p>
          </div>
          <button @click="alert.show = false" class="ml-3 flex-shrink-0">
            <svg class="h-5 w-5 text-gray-400 hover:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { clientService } from '@/services/clientService'

export default {
  name: 'ClienteFormView',
  components: {
    AppNavigation
  },
  data() {
    return {
      loading: false,
      isEditing: false,
      clientId: null,
      form: {
        name: '',
        rfc: '',
        address: '',
        city: '',
        state: '',
        postal_code: '',
        client_type: 'empresa',
        credit_limit: 0,
        contact_name: '',
        contact_email: '',
        contact_phone: '',
        contact_rol: ''
      },
      alert: {
        show: false,
        type: 'success',
        title: '',
        message: ''
      }
    }
  },
  async mounted() {
    // Si hay un ID en la ruta, estamos editando
    this.clientId = this.$route.params.id
    if (this.clientId) {
      this.isEditing = true
      await this.loadClient()
    }
  },
  methods: {
    async loadClient() {
      this.loading = true
      try {
        const client = await clientService.getClientById(this.clientId)
        
        // Llenar el formulario con los datos del cliente
        this.form = {
          name: client.name || '',
          rfc: client.rfc || '',
          address: client.address || '',
          city: client.city || '',
          state: client.state || '',
          postal_code: client.postal_code || client.zip_code || '',
          client_type: client.client_type || (client.comercial_name ? 'empresa' : 'persona'),
          credit_limit: client.credit_limit || 0,
          contact_name: client.contact?.name || '',
          contact_email: client.contact?.email || '',
          contact_phone: client.contact?.phone || '',
          contact_rol: client.contact?.rol || ''
        }
      } catch (error) {
        console.error('Error loading client:', error)
        this.showAlert('error', 'Error', 'No se pudo cargar la información del cliente')
      } finally {
        this.loading = false
      }
    },

    async handleSubmit() {
      this.loading = true
      try {
        const payload = {
          name: this.form.name,
          rfc: this.form.rfc,
          address: this.form.address,
          city: this.form.city,
          zip_code: this.form.postal_code,
          comercial_name: this.form.client_type === 'empresa' ? this.form.name : null
        }

        // Solo agregar campos de contacto si tienen valor
        if (this.form.contact_name) {
          payload.contact_name = this.form.contact_name
        }
        if (this.form.contact_email) {
          payload.contact_email = this.form.contact_email
        }
        if (this.form.contact_phone) {
          payload.contact_phone = this.form.contact_phone
        }
        if (this.form.contact_rol) {
          payload.contact_rol = this.form.contact_rol
        }

        console.log('Payload a enviar:', payload)

        if (this.isEditing) {
          await clientService.updateClient(this.clientId, payload)
          this.showAlert('success', 'Cliente Actualizado', 'Los datos del cliente se actualizaron correctamente')
        } else {
          await clientService.createClient(payload)
          this.showAlert('success', 'Cliente Creado', 'El cliente se creó exitosamente')
        }

        // Redirigir después de 2 segundos
        setTimeout(() => {
          this.$router.push('/comercial/clientes')
        }, 2000)

      } catch (error) {
        console.error('Error saving client:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido'
        this.showAlert('error', 'Error', `No se pudo guardar el cliente: ${errorMessage}`)
      } finally {
        this.loading = false
      }
    },

    showAlert(type, title, message) {
      this.alert = {
        show: true,
        type,
        title,
        message
      }
      // Auto ocultar después de 5 segundos
      setTimeout(() => {
        this.alert.show = false
      }, 5000)
    },

    goBack() {
      // Si venimos de editar, intentar volver a la página anterior
      // sino ir a la lista de clientes
      if (this.isEditing && window.history.length > 2) {
        this.$router.go(-1)
      } else {
        this.$router.push('/clientes')
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
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  ring: 2px;
  ring-color: #93c5fd;
}

.input-field:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}
</style>
