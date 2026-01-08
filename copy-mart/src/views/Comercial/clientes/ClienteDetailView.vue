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
          Volver a Clientes
        </button>
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">{{ client?.name || 'Cargando...' }}</h1>
            <p class="text-gray-600 mt-2">Información completa del cliente</p>
          </div>
          <div class="flex gap-3">
            <button @click="goToEdit" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Editar
            </button>
            <button @click="showDeleteModal = true" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white rounded-lg shadow-lg p-12 text-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-600">Cargando información del cliente...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <div class="flex items-center">
          <svg class="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="text-red-800 font-semibold">Error al cargar el cliente</h3>
            <p class="text-red-600 text-sm">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div v-else-if="client" class="space-y-6">
        <!-- Estado y estadísticas -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-600">Estado</p>
                <p class="text-lg font-semibold" :class="client.is_active ? 'text-green-600' : 'text-gray-600'">
                  {{ client.is_active ? 'Activo' : 'Inactivo' }}
                </p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-600">Sucursales</p>
                <p class="text-lg font-semibold text-gray-900">{{ client.branches?.length || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-600">Límite Crédito</p>
                <p class="text-lg font-semibold text-gray-900">
                  ${{ formatCurrency(client.credit_limit || 0) }}
                </p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-600">Registrado</p>
                <p class="text-lg font-semibold text-gray-900">
                  {{ formatDate(client.created_at) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Información General -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
          <div class="px-6 py-4 bg-blue-50 border-b border-blue-200">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h2 class="text-xl font-semibold text-gray-900">Información General</h2>
            </div>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Nombre / Razón Social</label>
                <p class="text-base text-gray-900 font-medium">{{ client.name || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">RFC</label>
                <p class="text-base text-gray-900">{{ client.rfc || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Nombre Comercial</label>
                <p class="text-base text-gray-900">{{ client.comercial_name || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Tipo</label>
                <span :class="['px-3 py-1 rounded-full text-sm font-medium inline-block', client.comercial_name ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800']">
                  {{ client.comercial_name ? 'Empresa' : 'Persona Física' }}
                </span>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-600 mb-1">Dirección</label>
                <p class="text-base text-gray-900">{{ client.address || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Ciudad</label>
                <p class="text-base text-gray-900">{{ client.city || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Código Postal</label>
                <p class="text-base text-gray-900">{{ client.zip_code || 'N/A' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Contacto Principal -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
          <div class="px-6 py-4 bg-green-50 border-b border-green-200">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h2 class="text-xl font-semibold text-gray-900">Contacto Principal</h2>
            </div>
          </div>
          <div class="p-6">
            <div v-if="client.contact" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Nombre</label>
                <p class="text-base text-gray-900 font-medium">{{ client.contact.name || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Puesto / Rol</label>
                <p class="text-base text-gray-900">{{ client.contact.rol || 'N/A' }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Email</label>
                <p class="text-base text-gray-900">
                  <a v-if="client.contact.email" :href="`mailto:${client.contact.email}`" class="text-blue-600 hover:underline">
                    {{ client.contact.email }}
                  </a>
                  <span v-else>N/A</span>
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Teléfono</label>
                <p class="text-base text-gray-900">
                  <a v-if="client.contact.phone" :href="`tel:${client.contact.phone}`" class="text-blue-600 hover:underline">
                    {{ client.contact.phone }}
                  </a>
                  <span v-else>N/A</span>
                </p>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-16 h-16 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <p>No hay contacto principal registrado</p>
            </div>
          </div>
        </div>

        <!-- Sucursales -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
          <div class="px-6 py-4 bg-purple-50 border-b border-purple-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <h2 class="text-xl font-semibold text-gray-900">Sucursales</h2>
              </div>
              <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                {{ client.branches?.length || 0 }} Total
              </span>
            </div>
          </div>
          <div class="p-6">
            <div v-if="client.branches && client.branches.length > 0" class="space-y-4">
              <div v-for="branch in client.branches" :key="branch.branch_id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center">
                    <h3 class="text-lg font-semibold text-gray-900">{{ branch.name }}</h3>
                    <span v-if="branch.is_main" class="ml-3 px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                      Principal
                    </span>
                  </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                  <div v-if="branch.address">
                    <span class="text-gray-600">Dirección:</span>
                    <span class="text-gray-900 ml-2">{{ branch.address }}</span>
                  </div>
                  <div v-if="branch.city">
                    <span class="text-gray-600">Ciudad:</span>
                    <span class="text-gray-900 ml-2">{{ branch.city }}</span>
                  </div>
                  <div v-if="branch.zip_code">
                    <span class="text-gray-600">C.P.:</span>
                    <span class="text-gray-900 ml-2">{{ branch.zip_code }}</span>
                  </div>
                </div>
                <div v-if="branch.areas && branch.areas.length > 0" class="mt-3 pt-3 border-t border-gray-200">
                  <p class="text-sm text-gray-600 mb-2">Áreas:</p>
                  <div class="flex flex-wrap gap-2">
                    <span v-for="area in branch.areas" :key="area.area_id" class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                      {{ area.name }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-16 h-16 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <p>No hay sucursales registradas</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de eliminación -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Confirmar eliminación</h3>
              <p class="text-sm text-gray-600">Esta acción no se puede deshacer</p>
            </div>
          </div>
          <p class="text-gray-700 mb-6">
            ¿Está seguro de que desea eliminar el cliente <strong>{{ client?.name }}</strong>?
          </p>
          <div class="flex justify-end gap-3">
            <button @click="showDeleteModal = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button @click="handleDelete" :disabled="deleting" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed">
              {{ deleting ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { clientService } from '@/services/clientService'

export default {
  name: 'ClienteDetailView',
  components: {
    AppNavigation
  },
  data() {
    return {
      client: null,
      loading: false,
      error: null,
      showDeleteModal: false,
      deleting: false
    }
  },
  async mounted() {
    const clientId = this.$route.params.id
    if (clientId) {
      await this.loadClient(clientId)
    }
  },
  methods: {
    async loadClient(clientId) {
      this.loading = true
      this.error = null
      try {
        this.client = await clientService.getClientById(clientId)
      } catch (error) {
        console.error('Error loading client:', error)
        this.error = error.response?.data?.detail || 'No se pudo cargar la información del cliente'
      } finally {
        this.loading = false
      }
    },

    formatCurrency(value) {
      if (!value) return '0.00'
      return Number(value).toLocaleString('es-MX', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('es-MX', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      } catch (error) {
        console.error('Error formatting date:', error)
        return 'N/A'
      }
    },

    goBack() {
      this.$router.push('/clientes')
    },

    goToEdit() {
      this.$router.push(`/comercial/clientes/editar/${this.client.client_id}`)
    },

    async handleDelete() {
      this.deleting = true
      try {
        await clientService.deleteClient(this.client.client_id)
        this.$router.push('/clientes')
      } catch (error) {
        console.error('Error deleting client:', error)
        alert('Error al eliminar el cliente: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.deleting = false
        this.showDeleteModal = false
      }
    }
  }
}
</script>

<style scoped>
.btn-secondary {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: white;
  color: #374151;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
}
</style>
