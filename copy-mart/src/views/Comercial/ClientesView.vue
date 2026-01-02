<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h1 class="text-3xl font-bold text-blue-800 mb-2">Gestión de Clientes</h1>
          <p class="text-blue-600">Administra la información de tus clientes</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Clientes</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Activos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.active }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Empresas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.companies }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Personas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.persons }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4">
            <button @click="showCreateModal = true" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Cliente
            </button>
            <button @click="loadClients" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <div class="flex-1">
              <input v-model="searchQuery" type="text" placeholder="Buscar clientes..." class="input-field w-full">
            </div>
            <select v-model="filterStatus" class="input-field w-40">
              <option value="">Todos</option>
              <option value="activo">Activos</option>
              <option value="inactivo">Inactivos</option>
            </select>
          </div>
        </div>

        <!-- Clients Table -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Listado de Clientes</h2>
          </div>
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <p class="text-gray-500">Cargando clientes...</p>
            </div>
            <div v-else-if="error" class="text-center py-8">
              <p class="text-red-500">{{ error }}</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre/Razón Social</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">RFC</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contacto</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredClients.length === 0">
                    <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                      No hay clientes registrados
                    </td>
                  </tr>
                  <tr v-for="client in filteredClients" :key="client.client_id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ client.client_id }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ client.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ client.rfc || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div class="font-medium text-gray-800">{{ client.contact_name || '-' }}</div>
                      <div class="text-gray-500">{{ client.contact_email || '-' }}</div>
                      <div class="text-gray-500">{{ client.contact_phone || client.contact_rol || '-' }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ client.client_type || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', client.status === 'activo' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
                        {{ client.status || 'activo' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button @click="editClient(client)" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                      <button @click="deleteClient(client.client_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ showCreateModal ? 'Nuevo Cliente' : 'Editar Cliente' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <form @submit.prevent="showCreateModal ? createClient() : updateClient()" class="p-6">
          <div class="space-y-8">
            <section>
              <h4 class="text-sm font-semibold text-gray-800 mb-3">Datos del Cliente</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nombre / Razón Social *</label>
                  <input v-model="clientForm.name" type="text" required class="input-field">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">RFC</label>
                  <input v-model="clientForm.rfc" type="text" class="input-field">
                </div>
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
                  <input v-model="clientForm.address" type="text" class="input-field">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
                  <input v-model="clientForm.city" type="text" class="input-field">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
                  <input v-model="clientForm.state" type="text" class="input-field">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
                  <input v-model="clientForm.postal_code" type="text" class="input-field">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Límite de Crédito</label>
                  <input v-model="clientForm.credit_limit" type="number" step="0.01" class="input-field">
                </div>
              </div>
            </section>

            <section class="pt-4 border-t border-gray-200">
              <h4 class="text-sm font-semibold text-gray-800 mb-3">Datos de Contacto</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de Contacto</label>
                  <input v-model="clientForm.contact_name" type="text" class="input-field" placeholder="Nombre del contacto principal">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Puesto / Rol</label>
                  <input v-model="clientForm.contact_rol" type="text" class="input-field" placeholder="Ej. Compras, TI">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input v-model="clientForm.contact_email" type="email" class="input-field">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                  <input v-model="clientForm.contact_phone" type="tel" class="input-field">
                </div>
              </div>
            </section>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              {{ showCreateModal ? 'Crear Cliente' : 'Actualizar Cliente' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Message Modal -->
    <div v-if="showMessageModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold" :class="messageType === 'success' ? 'text-green-800' : 'text-red-800'">
              {{ messageTitle }}
            </h3>
            <button @click="closeMessageModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p class="text-gray-700 mb-6">{{ messageText }}</p>
          <div class="flex justify-end">
            <button @click="closeMessageModal" :class="['px-4 py-2 rounded-lg text-white font-medium', messageType === 'success' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700']">
              Aceptar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Confirmar eliminación</h3>
          <p class="text-gray-700 mb-6">¿Está seguro de que desea eliminar este cliente? Esta acción no se puede deshacer.</p>
          <div class="flex justify-end gap-3">
            <button @click="cancelDelete" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
              Eliminar
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
  name: 'ClientesView',
  components: {
    AppNavigation
  },
  data() {
    return {
      clients: [],
      loading: false,
      error: null,
      showCreateModal: false,
      showEditModal: false,
      searchQuery: '',
      filterStatus: '',
      clientForm: {
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
      editingClientId: null,
      showMessageModal: false,
      messageType: 'success',
      messageTitle: '',
      messageText: '',
      showDeleteConfirm: false,
      deleteClientId: null,
      messageTimeout: null
    }
  },
  computed: {
    filteredClients() {
      return this.clients.filter(client => {
        const matchesSearch = !this.searchQuery || 
          client.name?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          client.rfc?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          client.email?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          client.contact_name?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          client.contact_email?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          client.contact_phone?.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchesStatus = !this.filterStatus || client.status === this.filterStatus
        
        return matchesSearch && matchesStatus
      })
    },
    stats() {
      return {
        total: this.clients.length,
        active: this.clients.filter(c => c.status === 'activo').length,
        companies: this.clients.filter(c => c.client_type === 'empresa').length,
        persons: this.clients.filter(c => c.client_type === 'persona').length
      }
    }
  },
  async mounted() {
    await this.loadClients()
  },
  methods: {
    normalizeContact(client) {
      // Usa campos planos, luego el contacto principal, luego el primero de la lista
      const primary = client.contact || client.primary_contact || (client.contacts && client.contacts[0]) || {}
      return {
        contact_name: client.contact_name || primary.name || '',
        contact_email: client.contact_email || primary.email || '',
        contact_phone: client.contact_phone || primary.phone || '',
        contact_rol: client.contact_rol || primary.rol || ''
      }
    },

    async loadClients() {
      this.loading = true
      this.error = null
      try {
        const clients = await clientService.getClients()
        console.log('API clients raw:', clients)
        this.clients = clients.map(c => ({
          ...c,
          ...this.normalizeContact(c),
          client_type: c.client_type || (c.comercial_name ? 'empresa' : 'persona'),
          status: c.is_active ? 'activo' : 'inactivo'
        }))
      } catch (err) {
        this.error = 'Error al cargar clientes: ' + err.message
        console.error('Error loading clients:', err)
      } finally {
        this.loading = false
      }
    },
    
    async createClient() {
      try {
        const payload = {
          name: this.clientForm.name,
          rfc: this.clientForm.rfc,
          address: this.clientForm.address,
          city: this.clientForm.city,
          state: this.clientForm.state,
          zip_code: this.clientForm.postal_code,
          comercial_name: this.clientForm.client_type === 'empresa' ? this.clientForm.name : null,
          credit_limit: this.clientForm.credit_limit,
          contact_name: this.clientForm.contact_name || this.clientForm.name,
          contact_email: this.clientForm.contact_email,
          contact_phone: this.clientForm.contact_phone,
          contact_rol: this.clientForm.contact_rol
        }

        console.log('Create payload:', payload)

        await clientService.createClient(payload)
        await this.loadClients()
        this.closeModal()
        this.showMessage('success', 'Éxito', 'Cliente creado exitosamente')
      } catch (err) {
        this.showMessage('error', 'Error', 'Error al crear cliente: ' + err.message)
      }
    },
    
    editClient(client) {
      this.editingClientId = client.client_id
      const normalized = this.normalizeContact(client)
      this.clientForm = {
        name: client.name || '',
        rfc: client.rfc || '',
        address: client.address || '',
        city: client.city || '',
        state: client.state || '',
        postal_code: client.postal_code || client.zip_code || '',
        client_type: client.client_type || (client.comercial_name ? 'empresa' : 'persona'),
        credit_limit: client.credit_limit ?? 0,
        ...normalized
      }
      this.showEditModal = true
    },
    
    async updateClient() {
      try {
        const payload = {
          name: this.clientForm.name,
          rfc: this.clientForm.rfc,
          address: this.clientForm.address,
          city: this.clientForm.city,
          state: this.clientForm.state,
          zip_code: this.clientForm.postal_code,
          comercial_name: this.clientForm.client_type === 'empresa' ? this.clientForm.name : null,
          credit_limit: this.clientForm.credit_limit,
          contact_name: this.clientForm.contact_name || this.clientForm.name,
          contact_email: this.clientForm.contact_email,
          contact_phone: this.clientForm.contact_phone,
          contact_rol: this.clientForm.contact_rol
        }

        console.log('Update payload:', payload)

        await clientService.updateClient(this.editingClientId, payload)
        await this.loadClients()
        this.closeModal()
        this.showMessage('success', 'Éxito', 'Cliente actualizado exitosamente')
      } catch (err) {
        this.showMessage('error', 'Error', 'Error al actualizar cliente: ' + err.message)
      }
    },
    
    deleteClient(clientId) {
      this.deleteClientId = clientId
      this.showDeleteConfirm = true
    },

    async confirmDelete() {
      try {
        console.log('Eliminando cliente ID:', this.deleteClientId)
        await clientService.deleteClient(this.deleteClientId)
        console.log('Cliente eliminado exitosamente')
        await this.loadClients()
        this.showDeleteConfirm = false
        this.deleteClientId = null
        this.showMessage('success', 'Éxito', 'Cliente eliminado exitosamente')
      } catch (err) {
        console.error('Error al eliminar:', err)
        this.showDeleteConfirm = false
        this.deleteClientId = null
        this.showMessage('error', 'Error', 'Error al eliminar cliente: ' + err.message)
      }
    },

    cancelDelete() {
      this.showDeleteConfirm = false
      this.deleteClientId = null
    },

    showMessage(type, title, text) {
      this.messageType = type
      this.messageTitle = title
      this.messageText = text
      this.showMessageModal = true

      // Auto-close after 2.5 seconds
      if (this.messageTimeout) clearTimeout(this.messageTimeout)
      this.messageTimeout = setTimeout(() => {
        this.closeMessageModal()
      }, 2500)
    },

    closeMessageModal() {
      if (this.messageTimeout) clearTimeout(this.messageTimeout)
      this.showMessageModal = false
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingClientId = null
      this.clientForm = {
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
      }
    }
  }
}
</script>
