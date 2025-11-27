<template>
<<<<<<< HEAD
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Clientes</h1>
        <p class="text-gray-600 mt-2">Administra tu base de clientes</p>
      </div>
      
      <div class="card">
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Módulo de Clientes</h3>
          <p class="mt-1 text-sm text-gray-500">Este módulo se encuentra en desarrollo</p>
          <div class="mt-6">
            <button type="button" class="btn-primary">
              Próximamente
            </button>
=======
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Gestión de Clientes</h1>
          <p class="text-gray-600 mt-2">Administra tu base de clientes</p>
        </div>
        <button 
          @click="openCreateModal"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <i class="fas fa-plus"></i>
          Nuevo Cliente
        </button>
      </div>

      <!-- Filtros y búsqueda -->
      <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
            <input
              type="text"
              v-model="searchQuery"
              @input="searchClients"
              placeholder="Nombre, RFC o email..."
              class="w-full border border-gray-300 rounded-md px-3 py-2"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Industria</label>
            <select v-model="industryFilter" @change="applyFilters" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">Todas las industrias</option>
              <option value="Tecnología">Tecnología</option>
              <option value="Manufactura">Manufactura</option>
              <option value="Servicios">Servicios</option>
              <option value="Comercio">Comercio</option>
              <option value="Educación">Educación</option>
              <option value="Salud">Salud</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
            <select v-model="statusFilter" @change="applyFilters" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">Todos</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tabla de clientes -->
      <div class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RFC</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dirección</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ciudad</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sucursales</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="client in clients" :key="client.client_id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <i class="fas fa-building text-blue-600"></i>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ client.name }}</div>
                      <div class="text-sm text-gray-500">{{ client.comercial_name || 'Sin nombre comercial' }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ client.rfc || 'N/A' }}
                </td>
                <td class="px-6 py-4 text-sm text-gray-900">
                  <div class="max-w-xs truncate">{{ client.address || 'N/A' }}</div>
                  <div class="text-xs text-gray-500">{{ client.colonia || '' }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ client.city || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="client.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ client.is_active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                    {{ client.total_branches || 0 }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center gap-2">
                    <button 
                      @click="editClient(client)"
                      class="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
                      title="Editar"
                    >
                      <i class="fas fa-edit mr-1"></i>
                      Editar
                    </button>
                    <button 
                      @click="toggleClientStatus(client)"
                      :class="client.is_active ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'"
                      class="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-white focus:outline-none"
                      :title="client.is_active ? 'Desactivar' : 'Activar'"
                    >
                      <i :class="client.is_active ? 'fas fa-ban mr-1' : 'fas fa-check mr-1'"></i>
                      {{ client.is_active ? 'Desactivar' : 'Activar' }}
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="clients.length === 0">
                <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                  {{ isLoading ? 'Cargando clientes...' : 'No hay clientes registrados' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button 
              @click="previousPage" 
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Anterior
            </button>
            <button 
              @click="nextPage" 
              :disabled="currentPage >= totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Siguiente
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando <span class="font-medium">{{ Math.min((currentPage - 1) * itemsPerPage + 1, totalItems) }}</span> a 
                <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span> de 
                <span class="font-medium">{{ totalItems }}</span> resultados
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button 
                  @click="previousPage" 
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  <i class="fas fa-chevron-left"></i>
                </button>
                <template v-for="page in visiblePages" :key="page">
                  <button 
                    @click="goToPage(page)"
                    :class="page === currentPage ? 'bg-blue-50 border-blue-500 text-blue-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'"
                    class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                  >
                    {{ page }}
                  </button>
                </template>
                <button 
                  @click="nextPage" 
                  :disabled="currentPage >= totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  <i class="fas fa-chevron-right"></i>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de crear/editar cliente -->
      <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
          <div class="mt-3">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ isEditing ? 'Editar Cliente' : 'Nuevo Cliente' }}
            </h3>
            
            <form @submit.prevent="saveClient">
              <!-- Información General -->
              <div class="mb-6">
                <h4 class="text-md font-semibold text-gray-800 mb-3 border-b pb-2">Información General</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de la Empresa *</label>
                    <input
                      type="text"
                      v-model="clientForm.name"
                      required
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Comercial</label>
                    <input
                      type="text"
                      v-model="clientForm.comercial_name"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">RFC</label>
                    <input
                      type="text"
                      v-model="clientForm.rfc"
                      maxlength="13"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
                    <input
                      type="text"
                      v-model="clientForm.city"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
                    <input
                      type="text"
                      v-model="clientForm.address"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Colonia</label>
                    <input
                      type="text"
                      v-model="clientForm.colonia"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
                    <input
                      type="text"
                      v-model="clientForm.zip_code"
                      maxlength="5"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                </div>
              </div>

              <!-- Información de Contacto -->
              <div class="mb-6">
                <h4 class="text-md font-semibold text-gray-800 mb-3 border-b pb-2">Información de Contacto</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Contacto</label>
                    <input
                      type="text"
                      v-model="clientForm.contact_name"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ej: Juan Pérez"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Cargo/Puesto</label>
                    <input
                      type="text"
                      v-model="clientForm.contact_rol"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ej: Gerente General"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                    <input
                      type="tel"
                      v-model="clientForm.contact_phone"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ej: 555-1234"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input
                      type="email"
                      v-model="clientForm.contact_email"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ej: contacto@empresa.com"
                    >
                  </div>
                </div>
              </div>
              
              <div class="mt-6 flex justify-end space-x-3">
                <button
                  type="button"
                  @click="closeModal"
                  class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isLoading"
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {{ isLoading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Loading spinner -->
      <div v-if="isLoading && !showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-4 rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span>Cargando...</span>
>>>>>>> develop
          </div>
        </div>
      </div>
    </div>
<<<<<<< HEAD
  </div>
</template>

<script>
import AppNavigation from '../components/AppNavigation.vue'
=======
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { clientService } from '@/services/clientService'
>>>>>>> develop

export default {
  name: 'ClientesView',
  components: {
<<<<<<< HEAD
    AppNavigation
=======
    BaseLayout
  },
  data() {
    return {
      clients: [],
      searchQuery: '',
      industryFilter: '',
      statusFilter: '',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      totalPages: 1,
      isLoading: false,
      showModal: false,
      isEditing: false,
      selectedClient: null,
      clientForm: {
        name: '',
        comercial_name: '',
        rfc: '',
        address: '',
        colonia: '',
        zip_code: '',
        city: '',
        contact_name: '',
        contact_phone: '',
        contact_email: '',
        contact_rol: ''
      }
    }
  },
  computed: {
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    }
  },
  async mounted() {
    await this.loadClients()
  },
  methods: {
    async loadClients() {
      try {
        this.isLoading = true
        
        // Verificar si hay token antes de hacer la llamada
        const token = localStorage.getItem('token')
        if (!token) {
          console.warn('No hay token de autenticación')
          this.clients = []
          this.isLoading = false
          return
        }
        
        const response = await clientService.getClients(0, 100, this.statusFilter === 'active' ? true : this.statusFilter === 'inactive' ? false : null)
        this.clients = response || []
        
        // Aplicar filtros locales
        let filtered = [...this.clients]
        
        if (this.searchQuery) {
          filtered = filtered.filter(c => 
            c.name?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            c.rfc?.toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        }
        
        if (this.industryFilter) {
          filtered = filtered.filter(c => c.industry === this.industryFilter)
        }
        
        this.totalItems = filtered.length
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage)
      } catch (error) {
        console.error('Error loading clients:', error)
        this.clients = []
        // No mostrar alert si es solo un problema de autenticación
        if (!error.message?.includes('401') && !error.message?.includes('token')) {
          alert('Error al cargar clientes: ' + error.message)
        }
      } finally {
        this.isLoading = false
      }
    },

    async searchClients() {
      this.currentPage = 1
      await this.loadClients()
    },

    async applyFilters() {
      this.currentPage = 1
      await this.loadClients()
    },

    openCreateModal() {
      this.isEditing = false
      this.clientForm = {
        name: '',
        comercial_name: '',
        rfc: '',
        address: '',
        colonia: '',
        zip_code: '',
        city: '',
        contact_name: '',
        contact_phone: '',
        contact_email: '',
        contact_rol: ''
      }
      this.showModal = true
    },

    editClient(client) {
      this.isEditing = true
      this.selectedClient = client
      this.clientForm = {
        ...client,
        contact_name: client.contact?.name || '',
        contact_phone: client.contact?.phone || '',
        contact_email: client.contact?.email || '',
        contact_rol: client.contact?.rol || ''
      }
      this.showModal = true
    },

    viewClient(client) {
      // Implementar vista de detalles más adelante
      alert(`Ver detalles de: ${client.name}`)
      console.log('Viewing client:', client)
    },

    async saveClient() {
      try {
        this.isLoading = true
        
        if (this.isEditing) {
          await clientService.updateClient(this.selectedClient.client_id, this.clientForm)
          alert('Cliente actualizado correctamente')
        } else {
          await clientService.createClient(this.clientForm)
          alert('Cliente creado correctamente')
        }
        
        this.closeModal()
        await this.loadClients()
      } catch (error) {
        console.error('Error saving client:', error)
        alert('Error al guardar el cliente: ' + error.message)
      } finally {
        this.isLoading = false
      }
    },

    async toggleClientStatus(client) {
      try {
        const newStatus = !client.is_active
        await clientService.updateClient(client.client_id, { is_active: newStatus })
        client.is_active = newStatus
        alert(`Cliente ${newStatus ? 'activado' : 'desactivado'} correctamente`)
        await this.loadClients()
      } catch (error) {
        console.error('Error toggling client status:', error)
        alert('Error al cambiar el estado del cliente: ' + error.message)
      }
    },

    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.selectedClient = null
    },

    formatDate(date) {
      if (!date) return 'N/A'
      return new Date(date).toLocaleDateString('es-ES')
    },

    // Métodos de paginación
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.loadClients()
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.loadClients()
      }
    },

    goToPage(page) {
      this.currentPage = page
      this.loadClients()
    }
>>>>>>> develop
  }
}
</script>