<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-green-50 p-6 rounded-lg border border-green-200">
          <h1 class="text-3xl font-bold text-green-800 mb-2">Gestión de Compras</h1>
          <p class="text-green-600">Administra las órdenes de compra de refacciones</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  📦
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total de Compras</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  ⏳
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Curso</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.inProgress }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  🚚
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Tránsito</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.inTransit }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  ✅
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Concluidas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.completed }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4 items-center justify-between">
            <button @click="showCreateModal = true" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nueva Orden de Compra
            </button>
            <button @click="loadPurchases" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <div class="flex gap-2">
              <select v-model="filterStatus" class="input-field">
                <option value="">Todos los estados</option>
                <option value="En Curso">En Curso</option>
                <option value="En Tránsito">En Tránsito</option>
                <option value="Concluido">Concluido</option>
                <option value="Pausado Back Orders">Pausado</option>
                <option value="Falta Pago Proveedor">Falta Pago</option>
              </select>
              <select v-model="filterType" class="input-field">
                <option value="">Todos los tipos</option>
                <option value="Interna">Interna</option>
                <option value="Venta">Venta</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Purchases Table -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Órdenes de Compra</h2>
          </div>
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <p class="text-gray-500">Cargando compras...</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Refacción</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cantidad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Envío</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredPurchases.length === 0">
                    <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                      No hay órdenes de compra registradas
                    </td>
                  </tr>
                  <tr v-for="purchase in filteredPurchases" :key="purchase.purchase_id">
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-green-600">#{{ purchase.purchase_id }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ purchase.name }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ purchase.sparepart?.name || '-' }}
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ purchase.amount }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="getTypeClass(purchase.type)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ purchase.type }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="getStatusClass(purchase.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ purchase.status }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ purchase.shipping_code || '-' }}
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button @click="editPurchase(purchase)" class="text-blue-600 hover:text-blue-900">Editar</button>
                      <button @click="deletePurchase(purchase.purchase_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Purchase Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-2xl font-bold text-gray-900">
            {{ editingPurchaseId ? 'Editar Orden de Compra' : 'Nueva Orden de Compra' }}
          </h2>
        </div>
        
        <form @submit.prevent="editingPurchaseId ? updatePurchase() : createPurchase()" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de la Compra *</label>
              <input v-model="purchaseForm.name" type="text" required class="input-field" placeholder="Compra de toner negro">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Refacción *</label>
              <select v-model="purchaseForm.sparepart_id" required class="input-field">
                <option value="">Seleccionar refacción</option>
                <option v-for="sp in spareparts" :key="sp.sparepart_id" :value="sp.sparepart_id">
                  {{ sp.name }} {{ sp.code ? `(${sp.code})` : '' }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Usuario Solicitante *</label>
              <select v-model="purchaseForm.user_id" required class="input-field">
                <option value="">Seleccionar usuario</option>
                <option v-for="user in users" :key="user.contact_id" :value="user.contact_id">
                  {{ user.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad *</label>
              <input v-model.number="purchaseForm.amount" type="number" min="1" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="purchaseForm.type" class="input-field">
                <option value="Interna">Interna</option>
                <option value="Venta">Venta</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="purchaseForm.status" class="input-field">
                <option value="En Curso">En Curso</option>
                <option value="En Tránsito">En Tránsito</option>
                <option value="Pausado Back Orders">Pausado Back Orders</option>
                <option value="Falta Pago Proveedor">Falta Pago Proveedor</option>
                <option value="Falta Factura">Falta Factura</option>
                <option value="Por Revisar">Por Revisar</option>
                <option value="Falta Autorización">Falta Autorización</option>
                <option value="Rechazado">Rechazado</option>
                <option value="Concluido">Concluido</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Calidad</label>
              <input v-model="purchaseForm.quality" type="text" class="input-field" placeholder="Original, Genérico...">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Método de Envío</label>
              <input v-model="purchaseForm.shipping_method" type="text" class="input-field" placeholder="FedEx, DHL...">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código de Rastreo</label>
              <input v-model="purchaseForm.shipping_code" type="text" class="input-field" placeholder="ABC123456">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo de Envío</label>
              <input v-model.number="purchaseForm.shipping_cost" type="number" step="0.01" min="0" class="input-field" placeholder="0.00">
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Justificación</label>
              <textarea v-model="purchaseForm.justification" rows="2" class="input-field" placeholder="Motivo de la compra..."></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
              <textarea v-model="purchaseForm.comments" rows="3" class="input-field" placeholder="Comentarios adicionales..."></textarea>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
              {{ editingPurchaseId ? 'Actualizar' : 'Crear' }} Compra
            </button>
          </div>
        </form>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { purchaseService } from '@/services/purchaseService'
import { sparepartService } from '@/services/sparepartService'
import { contactService } from '@/services/contactService'

export default {
  name: 'ComprasView',
  components: {
    BaseLayout
  },
  data() {
    return {
      purchases: [],
      spareparts: [],
      users: [],
      loading: false,
      error: null,
      showCreateModal: false,
      showEditModal: false,
      filterStatus: '',
      filterType: '',
      purchaseForm: {
        sparepart_id: '',
        user_id: '',
        name: '',
        amount: 1,
        quality: '',
        justification: '',
        type: 'Interna',
        shipping_method: '',
        shipping_cost: null,
        shipping_code: '',
        status: 'En Curso',
        comments: ''
      },
      editingPurchaseId: null
    }
  },
  computed: {
    filteredPurchases() {
      return this.purchases.filter(purchase => {
        const matchesStatus = !this.filterStatus || purchase.status === this.filterStatus
        const matchesType = !this.filterType || purchase.type === this.filterType
        return matchesStatus && matchesType
      })
    },
    stats() {
      return {
        total: this.purchases.length,
        inProgress: this.purchases.filter(p => p.status === 'En Curso').length,
        inTransit: this.purchases.filter(p => p.status === 'En Tránsito').length,
        completed: this.purchases.filter(p => p.status === 'Concluido').length
      }
    }
  },
  async mounted() {
    await this.loadPurchases()
    await this.loadSpareparts()
    await this.loadUsers()
  },
  methods: {
    async loadPurchases() {
      this.loading = true
      this.error = null
      try {
        const response = await purchaseService.getPurchases({ pageSize: 100 })
        this.purchases = response.items || []
      } catch (err) {
        console.error('Error loading purchases:', err)
        this.error = 'Error al cargar compras'
      } finally {
        this.loading = false
      }
    },

    async loadSpareparts() {
      try {
        const response = await sparepartService.getSpareparts({ pageSize: 100 })
        this.spareparts = response.items || []
      } catch (err) {
        console.error('❌ Error loading spareparts:', err)
        this.showError('Error al cargar refacciones')
      }
    },

    async loadUsers() {
      try {
        const response = await contactService.getContacts()
        
        // contactService.getContacts devuelve un array directo
        if (Array.isArray(response)) {
          this.users = response
        } else {
          this.users = []
        }
      } catch (err) {
        console.error('❌ Error loading contacts:', err)
        this.showError('Error al cargar contactos')
      }
    },

    async createPurchase() {
      try {
        await purchaseService.createPurchase(this.purchaseForm)
        await this.loadPurchases()
        this.closeModal()
        this.success('Compra creada exitosamente')
      } catch (err) {
        this.showError('Error al crear compra: ' + err.message)
      }
    },

    editPurchase(purchase) {
      this.editingPurchaseId = purchase.purchase_id
      this.purchaseForm = {
        sparepart_id: purchase.sparepart_id,
        user_id: purchase.user_id,
        name: purchase.name,
        amount: purchase.amount,
        quality: purchase.quality || '',
        justification: purchase.justification || '',
        type: purchase.type,
        shipping_method: purchase.shipping_method || '',
        shipping_cost: purchase.shipping_cost || null,
        shipping_code: purchase.shipping_code || '',
        status: purchase.status,
        comments: purchase.comments || ''
      }
      this.showEditModal = true
    },

    async updatePurchase() {
      try {
        await purchaseService.updatePurchase(this.editingPurchaseId, this.purchaseForm)
        await this.loadPurchases()
        this.closeModal()
        this.success('Compra actualizada exitosamente')
      } catch (err) {
        this.showError('Error al actualizar compra: ' + err.message)
      }
    },

    async deletePurchase(purchaseId) {
      if (!confirm('¿Está seguro de eliminar esta orden de compra?')) return
      
      try {
        await purchaseService.deletePurchase(purchaseId)
        await this.loadPurchases()
        this.success('Compra eliminada exitosamente')
      } catch (err) {
        this.showError('Error al eliminar compra: ' + err.message)
      }
    },

    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingPurchaseId = null
      this.purchaseForm = {
        sparepart_id: '',
        user_id: '',
        name: '',
        amount: 1,
        quality: '',
        justification: '',
        type: 'Interna',
        shipping_method: '',
        shipping_cost: null,
        shipping_code: '',
        status: 'En Curso',
        comments: ''
      }
    },

    getStatusClass(status) {
      const classes = {
        'En Curso': 'bg-yellow-100 text-yellow-800',
        'En Tránsito': 'bg-blue-100 text-blue-800',
        'Concluido': 'bg-green-100 text-green-800',
        'Pausado Back Orders': 'bg-orange-100 text-orange-800',
        'Falta Pago Proveedor': 'bg-red-100 text-red-800',
        'Falta Factura': 'bg-purple-100 text-purple-800',
        'Rechazado': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },

    getTypeClass(type) {
      return type === 'Interna' 
        ? 'bg-blue-100 text-blue-800' 
        : 'bg-green-100 text-green-800'
    },

    showError(message) {
      this.error = message
      setTimeout(() => {
        this.error = null
      }, 5000)
    },

    success(message) {
      // Success message
    }
  }
}
</script>
