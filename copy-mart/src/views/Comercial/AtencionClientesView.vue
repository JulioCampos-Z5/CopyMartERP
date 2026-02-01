<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 ">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-rose-50 p-6 rounded-lg border border-rose-200">
        <h1 class="text-3xl font-bold text-rose-800 mb-2">Atención a Clientes</h1>
        <p class="text-rose-600">Centro de soporte y gestión de la experiencia del cliente</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-rose-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Tickets Abiertos</h3>
              <p class="text-2xl font-semibold text-gray-900">23</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Tiempo Promedio</h3>
              <p class="text-2xl font-semibold text-gray-900">2.4h</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m-5-14V3a2 2 0 012-2h2a2 2 0 012 2v1h6v20H7V4h2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Satisfacción</h3>
              <p class="text-2xl font-semibold text-gray-900">4.7/5</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Resueltos Hoy</h3>
              <p class="text-2xl font-semibold text-gray-900">18</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <button @click="showCreateClient = true" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            Registrar Cliente
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nuevo Ticket
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Chat en Vivo
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            Seguimiento Telefónico
          </button>
        </div>
      </div>

      <!-- Client Registration/Edit Form -->
      <div v-if="showCreateClient || showEditClient" class="bg-white p-6 rounded-lg shadow border">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900">{{ showEditClient ? 'Editar Cliente' : 'Registrar Nuevo Cliente' }}</h2>
          <button @click="showCreateClient = false; showEditClient = false; editingClient = null; resetForm()" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="showEditClient ? updateClient() : registerClient()" class="space-y-6">
          <!-- Información Básica -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">Información Básica</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre / Razón Social *</label>
                <input v-model="newClient.name" type="text" required class="input-field" placeholder="Empresa S.A. de C.V.">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">RFC</label>
                <input v-model="newClient.rfc" type="text" class="input-field" placeholder="ABC123456XYZ">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                <input v-model="newClient.email" type="email" required class="input-field" placeholder="contacto@empresa.com">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono *</label>
                <input v-model="newClient.phone" type="tel" required class="input-field" placeholder="55-1234-5678">
              </div>
            </div>
          </div>

          <!-- Dirección -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">Dirección</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Calle y Número</label>
                <input v-model="newClient.address" type="text" class="input-field" placeholder="Av. Principal #123">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Colonia</label>
                <input v-model="newClient.colony" type="text" class="input-field" placeholder="Centro">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
                <input v-model="newClient.city" type="text" class="input-field" placeholder="Ciudad de México">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
                <input v-model="newClient.state" type="text" class="input-field" placeholder="CDMX">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
                <input v-model="newClient.zip" type="text" class="input-field" placeholder="01000">
              </div>
            </div>
          </div>

          <!-- Información Comercial -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">Información Comercial</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Cliente</label>
                <select v-model="newClient.client_type" class="input-field">
                  <option value="persona_fisica">Persona Física</option>
                  <option value="persona_moral">Persona Moral</option>
                  <option value="gobierno">Gobierno</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Categoría</label>
                <select v-model="newClient.category" class="input-field">
                  <option value="regular">Regular</option>
                  <option value="vip">VIP</option>
                  <option value="mayorista">Mayorista</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Método de Pago Preferido</label>
                <select v-model="newClient.payment_method" class="input-field">
                  <option value="efectivo">Efectivo</option>
                  <option value="transferencia">Transferencia</option>
                  <option value="tarjeta">Tarjeta</option>
                  <option value="credito">Crédito</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Límite de Crédito</label>
                <input v-model="newClient.credit_limit" type="number" step="0.01" class="input-field" placeholder="0.00">
              </div>
            </div>
          </div>

          <!-- Contacto Principal -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">Contacto Principal</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Contacto</label>
                <input v-model="newClient.contact_name" type="text" class="input-field" placeholder="Juan Pérez">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Puesto</label>
                <input v-model="newClient.contact_position" type="text" class="input-field" placeholder="Gerente de Compras">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono del Contacto</label>
                <input v-model="newClient.contact_phone" type="tel" class="input-field" placeholder="55-9876-5432">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email del Contacto</label>
                <input v-model="newClient.contact_email" type="email" class="input-field" placeholder="contacto@empresa.com">
              </div>
            </div>
          </div>

          <!-- Notas -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Notas Adicionales</label>
            <textarea v-model="newClient.notes" rows="3" class="input-field" placeholder="Información adicional sobre el cliente..."></textarea>
          </div>

          <!-- Actions -->
          <div class="flex gap-3 justify-end pt-4 border-t">
            <button type="button" @click="showCreateClient = false; showEditClient = false; editingClient = null; resetForm()" class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-rose-600 text-white px-6 py-2 rounded-lg hover:bg-rose-700">
              {{ showEditClient ? 'Actualizar Cliente' : 'Registrar Cliente' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Lista de Clientes -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200 flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-900">Clientes Registrados</h2>
            <span class="text-sm text-gray-500">{{ clients.length }} clientes</span>
          </div>
          <div v-if="loadingClients" class="p-12 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-600 mx-auto"></div>
            <p class="mt-4 text-gray-600">Cargando clientes...</p>
          </div>
          <div v-else class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RFC</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Teléfono</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ciudad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="client in clients" :key="client.client_id" class="hover:bg-gray-50">
                    <td class="px-4 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-10 h-10 bg-rose-100 rounded-full flex items-center justify-center text-rose-600 font-semibold">
                          {{ client.name.charAt(0).toUpperCase() }}
                        </div>
                        <div class="ml-3">
                          <div class="text-sm font-medium text-gray-900">{{ client.name }}</div>
                          <div class="text-xs text-gray-500">{{ client.email || 'Sin email' }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ client.rfc || '-' }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ client.phone || '-' }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ client.city || '-' }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', client.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
                        {{ client.is_active ? 'Activo' : 'Inactivo' }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div class="flex gap-2">
                        <button @click="viewClient(client)" class="text-rose-600 hover:text-rose-800">
                          Ver
                        </button>
                        <button @click="editClient(client)" class="text-blue-600 hover:text-blue-800">
                          Editar
                        </button>
                        <button @click="deleteClient(client.client_id)" class="text-red-600 hover:text-red-800">
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="clients.length === 0">
                    <td colspan="6" class="px-4 py-8 text-center text-gray-500">
                      No hay clientes registrados
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Panel de Soporte -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Centro de Soporte</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 class="text-sm font-medium text-red-800 mb-2">Tickets Críticos</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">#T-001 - Empresa ABC</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Atender</button>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-red-700">#T-007 - Hospital San José</span>
                    <button class="text-xs bg-red-600 text-white px-2 py-1 rounded">Atender</button>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 class="text-sm font-medium text-green-800 mb-2">Chat en Vivo</h4>
                <div class="flex items-center">
                  <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span class="text-sm text-green-700">3 conversaciones activas</span>
                </div>
                <div class="mt-2 space-y-1 text-xs text-green-600">
                  <div>• Cliente: ¿Tienen papel A3?</div>
                  <div>• Cliente: Problema con pedido #123</div>
                  <div>• Cliente: Horarios de entrega</div>
                </div>
              </div>

              <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 mb-2">Métricas de Rendimiento</h4>
                <div class="space-y-1 text-sm text-blue-700">
                  <div class="flex justify-between">
                    <span>Tiempo de Respuesta:</span>
                    <span>12 min</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Primera Resolución:</span>
                    <span>78%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Tickets Cerrados:</span>
                    <span>18/23</span>
                  </div>
                </div>
              </div>

              <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 mb-2">Agentes Activos</h4>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Ana García</span>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Disponible</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Luis Martín</span>
                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Ocupado</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700">Carmen Ruiz</span>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Disponible</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { clientService } from '@/services/clientService.ts'

export default {
  name: 'AtencionClientesView',
  components: {
    BaseLayout
  },
  data() {
    return {
      showCreateClient: false,
      showEditClient: false,
      editingClient: null,
      clients: [],
      loadingClients: false,
      newClient: {
        name: '',
        rfc: '',
        email: '',
        phone: '',
        address: '',
        colony: '',
        city: '',
        state: '',
        zip: '',
        client_type: 'persona_moral',
        category: 'regular',
        payment_method: 'transferencia',
        credit_limit: 0,
        contact_name: '',
        contact_position: '',
        contact_phone: '',
        contact_email: '',
        notes: ''
      }
    }
  },
  mounted() {
    this.loadClients()
  },
  methods: {
    async loadClients() {
      this.loadingClients = true
      try {
        this.clients = await clientService.getClients(0, 100, true)
      } catch (err) {
        console.error('Error loading clients:', err)
        alert('Error al cargar clientes: ' + err.message)
      } finally {
        this.loadingClients = false
      }
    },

    async registerClient() {
      try {
        const clientData = {
          name: this.newClient.name,
          rfc: this.newClient.rfc,
          email: this.newClient.email,
          phone: this.newClient.phone,
          address: this.newClient.address,
          city: this.newClient.city,
          state: this.newClient.state,
          postal_code: this.newClient.zip,
          client_type: this.newClient.client_type,
          payment_terms: this.newClient.payment_method,
          credit_limit: parseFloat(this.newClient.credit_limit) || 0,
          notes: this.newClient.notes
        }
        
        await clientService.createClient(clientData)
        alert('Cliente registrado exitosamente')
        this.showCreateClient = false
        this.resetForm()
        await this.loadClients()
      } catch (err) {
        alert('Error al registrar cliente: ' + err.message)
      }
    },

    viewClient(client) {
      alert(`Cliente: ${client.name}\nRFC: ${client.rfc || 'N/A'}\nTeléfono: ${client.phone || 'N/A'}\nCiudad: ${client.city || 'N/A'}\nEstado: ${client.state || 'N/A'}`)
    },

    editClient(client) {
      this.editingClient = { ...client }
      this.newClient = {
        name: client.name,
        rfc: client.rfc || '',
        email: client.email || '',
        phone: client.phone || '',
        address: client.address || '',
        colony: '',
        city: client.city || '',
        state: client.state || '',
        zip: client.postal_code || '',
        client_type: client.client_type || 'persona_moral',
        category: 'regular',
        payment_method: client.payment_terms || 'transferencia',
        credit_limit: client.credit_limit || 0,
        contact_name: '',
        contact_position: '',
        contact_phone: '',
        contact_email: '',
        notes: client.notes || ''
      }
      this.showEditClient = true
    },

    async updateClient() {
      try {
        const clientData = {
          name: this.newClient.name,
          rfc: this.newClient.rfc,
          email: this.newClient.email,
          phone: this.newClient.phone,
          address: this.newClient.address,
          city: this.newClient.city,
          state: this.newClient.state,
          postal_code: this.newClient.zip,
          client_type: this.newClient.client_type,
          payment_terms: this.newClient.payment_method,
          credit_limit: parseFloat(this.newClient.credit_limit) || 0,
          notes: this.newClient.notes
        }
        
        await clientService.updateClient(this.editingClient.client_id, clientData)
        alert('Cliente actualizado exitosamente')
        this.showEditClient = false
        this.editingClient = null
        this.resetForm()
        await this.loadClients()
      } catch (err) {
        alert('Error al actualizar cliente: ' + err.message)
      }
    },

    async deleteClient(clientId) {
      if (!confirm('¿Está seguro de eliminar este cliente?')) return
      
      try {
        await clientService.deleteClient(clientId)
        alert('Cliente eliminado exitosamente')
        await this.loadClients()
      } catch (err) {
        alert('Error al eliminar cliente: ' + err.message)
      }
    },
    
    resetForm() {
      this.newClient = {
        name: '',
        rfc: '',
        email: '',
        phone: '',
        address: '',
        colony: '',
        city: '',
        state: '',
        zip: '',
        client_type: 'persona_moral',
        category: 'regular',
        payment_method: 'transferencia',
        credit_limit: 0,
        contact_name: '',
        contact_position: '',
        contact_phone: '',
        contact_email: '',
        notes: ''
      }
    }
  }
}
</script>