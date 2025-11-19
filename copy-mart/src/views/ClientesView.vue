<template>
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
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contacto</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Industria</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sucursales</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="client in clients" :key="client.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <i class="fas fa-building text-blue-600"></i>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ client.name }}</div>
                      <div class="text-sm text-gray-500">{{ client.email }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ client.rfc || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ client.phone || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ client.industry || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="client.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ client.is_active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                    {{ client.branches?.length || 0 }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button 
                    @click="viewClient(client)"
                    class="text-blue-600 hover:text-blue-900"
                    title="Ver detalles"
                  >
                    <i class="fas fa-eye"></i>
                  </button>
                  <button 
                    @click="editClient(client)"
                    class="text-yellow-600 hover:text-yellow-900"
                    title="Editar"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    @click="toggleClientStatus(client)"
                    :class="client.is_active ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'"
                    :title="client.is_active ? 'Desactivar' : 'Activar'"
                  >
                    <i :class="client.is_active ? 'fas fa-ban' : 'fas fa-check'"></i>
                  </button>
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
                  <label class="block text-sm font-medium text-gray-700 mb-1">RFC</label>
                  <input
                    type="text"
                    v-model="clientForm.rfc"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    v-model="clientForm.email"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                  <input
                    type="tel"
                    v-model="clientForm.phone"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Sitio Web</label>
                  <input
                    type="url"
                    v-model="clientForm.website"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Industria</label>
                  <select
                    v-model="clientForm.industry"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Seleccionar industria</option>
                    <option value="Tecnología">Tecnología</option>
                    <option value="Manufactura">Manufactura</option>
                    <option value="Servicios">Servicios</option>
                    <option value="Comercio">Comercio</option>
                    <option value="Educación">Educación</option>
                    <option value="Salud">Salud</option>
                    <option value="Construcción">Construcción</option>
                    <option value="Agricultura">Agricultura</option>
                    <option value="Turismo">Turismo</option>
                    <option value="Financiero">Financiero</option>
                  </select>
                </div>
              </div>
              
              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
                <textarea
                  v-model="clientForm.notes"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Información adicional sobre el cliente..."
                ></textarea>
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
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { clientService } from '@/services/clientService'

export default {
  name: 'ClientesView',
  components: {
    BaseLayout
  },
  data() {
    return {
      clients: [
        // Datos de ejemplo mientras no esté conectado el backend
        {
          id: 1,
          name: 'Ejemplo Corp',
          rfc: 'EJE123456789',
          email: 'contacto@ejemplo.com',
          phone: '555-1234',
          website: 'www.ejemplo.com',
          industry: 'Tecnología',
          is_active: true,
          branches: []
        },
        {
          id: 2,
          name: 'Servicios Integrales SA',
          rfc: 'SIN987654321',
          email: 'info@servicios.mx',
          phone: '555-5678',
          website: 'www.servicios.mx',
          industry: 'Servicios',
          is_active: true,
          branches: [{ id: 1, name: 'Sucursal Centro' }]
        },
        {
          id: 3,
          name: 'Manufacturas del Norte',
          rfc: 'MAN456789123',
          email: 'ventas@manufacturasdn.com',
          phone: '555-9012',
          website: 'www.manufacturasdn.com',
          industry: 'Manufactura',
          is_active: false,
          branches: []
        }
      ],
      searchQuery: '',
      industryFilter: '',
      statusFilter: '',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 3,
      totalPages: 1,
      isLoading: false,
      showModal: false,
      isEditing: false,
      selectedClient: null,
      clientForm: {
        name: '',
        rfc: '',
        email: '',
        phone: '',
        website: '',
        industry: '',
        notes: ''
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
        // Simulación de carga - cuando el backend esté listo, usar:
        // const response = await clientService.getClients(this.currentPage, this.itemsPerPage, this.searchQuery)
        // this.clients = response.items || response.data || []
        // this.totalItems = response.total || 0
        // this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage)
        
        // Datos de simulación
        setTimeout(() => {
          this.totalItems = this.clients.length
          this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage)
          this.isLoading = false
        }, 500)
      } catch (error) {
        console.error('Error loading clients:', error)
        this.isLoading = false
        // this.$notify (implementar notificaciones más adelante)
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
        rfc: '',
        email: '',
        phone: '',
        website: '',
        industry: '',
        notes: ''
      }
      this.showModal = true
    },

    editClient(client) {
      this.isEditing = true
      this.selectedClient = client
      this.clientForm = { ...client }
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
          // Simular actualización
          const index = this.clients.findIndex(c => c.id === this.selectedClient.id)
          if (index !== -1) {
            this.clients[index] = { ...this.clients[index], ...this.clientForm }
          }
          alert('Cliente actualizado correctamente')
        } else {
          // Simular creación
          const newClient = {
            id: Date.now(),
            ...this.clientForm,
            is_active: true,
            branches: []
          }
          this.clients.push(newClient)
          alert('Cliente creado correctamente')
        }
        
        this.closeModal()
        await this.loadClients()
      } catch (error) {
        console.error('Error saving client:', error)
        alert('Error al guardar el cliente')
      } finally {
        this.isLoading = false
      }
    },

    async toggleClientStatus(client) {
      try {
        client.is_active = !client.is_active
        alert(`Cliente ${client.is_active ? 'activado' : 'desactivado'} correctamente`)
        // Cuando el backend esté listo:
        // await clientService.toggleClientStatus(client.id)
      } catch (error) {
        console.error('Error toggling client status:', error)
        alert('Error al cambiar el estado del cliente')
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
  }
}
</script>