<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-orange-50 p-6 rounded-lg border border-orange-200">
          <h1 class="text-3xl font-bold text-orange-800 mb-2">Sistema de Facturación</h1>
          <p class="text-orange-600">Genera y administra facturas fiscales y no fiscales</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Facturas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Facturado</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ formatCurrency(stats.totalAmount) }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Pagadas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.paid }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Pendientes</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.pending }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4">
            <button @click="showCreateModal = true" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nueva Factura
            </button>
            <button @click="loadBillings" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <select v-model="filterStatus" class="input-field w-40">
              <option value="">Todos</option>
              <option value="pendiente">Pendientes</option>
              <option value="pagada">Pagadas</option>
              <option value="vencida">Vencidas</option>
              <option value="cancelada">Canceladas</option>
            </select>
          </div>
        </div>

        <!-- Billings Table -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Facturas Registradas</h3>
          </div>
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <p class="text-gray-500">Cargando facturas...</p>
            </div>
            <div v-else-if="error" class="text-center py-8">
              <p class="text-red-500">{{ error }}</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Folio</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vencimiento</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredBillings.length === 0">
                    <td colspan="7" class="px-4 py-8 text-center text-gray-500">
                      No hay facturas registradas
                    </td>
                  </tr>
                  <tr v-for="billing in filteredBillings" :key="billing.billing_id">
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ billing.invoice_number }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ billing.client?.name || '-' }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ formatCurrency(billing.amount) }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(billing.billing_date) }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(billing.due_date) }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(billing.status)]">
                        {{ getStatusLabel(billing.status) }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium">
                      <button v-if="billing.status === 'pendiente'" @click="markAsPaid(billing.billing_id)" class="text-green-600 hover:text-green-900 mr-3">Pagar</button>
                      <button @click="editBilling(billing)" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                      <button @click="deleteBilling(billing.billing_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
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
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ showCreateModal ? 'Nueva Factura' : 'Editar Factura' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <form @submit.prevent="showCreateModal ? createBilling() : updateBilling()" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cliente ID *</label>
              <input v-model="billingForm.client_id" type="number" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Factura *</label>
              <input v-model="billingForm.invoice_number" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Monto *</label>
              <input v-model="billingForm.amount" type="number" step="0.01" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Factura *</label>
              <input v-model="billingForm.billing_date" type="date" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Vencimiento *</label>
              <input v-model="billingForm.due_date" type="date" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="billingForm.status" class="input-field">
                <option value="pendiente">Pendiente</option>
                <option value="pagada">Pagada</option>
                <option value="vencida">Vencida</option>
                <option value="cancelada">Cancelada</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
              <textarea v-model="billingForm.notes" rows="3" class="input-field"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700">
              {{ showCreateModal ? 'Crear Factura' : 'Actualizar Factura' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { billingService } from '@/services/billingService'

export default {
  name: 'FacturacionView',
  components: {
    BaseLayout
  },
  data() {
    return {
      billings: [],
      loading: false,
      error: null,
      showCreateModal: false,
      showEditModal: false,
      filterStatus: '',
      billingForm: {
        client_id: '',
        invoice_number: '',
        amount: '',
        billing_date: new Date().toISOString().split('T')[0],
        due_date: '',
        status: 'pendiente',
        notes: ''
      },
      editingBillingId: null
    }
  },
  computed: {
    filteredBillings() {
      return this.billings.filter(billing => {
        if (!this.filterStatus) return true
        return billing.status === this.filterStatus
      })
    },
    stats() {
      return {
        total: this.billings.length,
        totalAmount: this.billings.reduce((sum, b) => sum + parseFloat(b.amount || 0), 0),
        paid: this.billings.filter(b => b.status === 'pagada').length,
        pending: this.billings.filter(b => b.status === 'pendiente').length
      }
    }
  },
  async mounted() {
    await this.loadBillings()
  },
  methods: {
    async loadBillings() {
      this.loading = true
      this.error = null
      try {
        this.billings = await billingService.getBillings()
      } catch (err) {
        this.error = 'Error al cargar facturas: ' + err.message
        console.error('Error loading billings:', err)
      } finally {
        this.loading = false
      }
    },
    
    async createBilling() {
      try {
        const data = {
          ...this.billingForm,
          client_id: parseInt(this.billingForm.client_id),
          amount: parseFloat(this.billingForm.amount)
        }
        await billingService.createBilling(data)
        await this.loadBillings()
        this.closeModal()
        alert('Factura creada exitosamente')
      } catch (err) {
        alert('Error al crear factura: ' + err.message)
      }
    },
    
    editBilling(billing) {
      this.editingBillingId = billing.billing_id
      this.billingForm = { ...billing }
      this.showEditModal = true
    },
    
    async updateBilling() {
      try {
        const data = {
          ...this.billingForm,
          client_id: parseInt(this.billingForm.client_id),
          amount: parseFloat(this.billingForm.amount)
        }
        await billingService.updateBilling(this.editingBillingId, data)
        await this.loadBillings()
        this.closeModal()
        alert('Factura actualizada exitosamente')
      } catch (err) {
        alert('Error al actualizar factura: ' + err.message)
      }
    },
    
    async deleteBilling(billingId) {
      if (!confirm('¿Está seguro de eliminar esta factura?')) return
      
      try {
        await billingService.deleteBilling(billingId)
        await this.loadBillings()
        alert('Factura eliminada exitosamente')
      } catch (err) {
        alert('Error al eliminar factura: ' + err.message)
      }
    },
    
    async markAsPaid(billingId) {
      try {
        await billingService.markAsPaid(billingId)
        await this.loadBillings()
        alert('Factura marcada como pagada')
      } catch (err) {
        alert('Error al marcar factura como pagada: ' + err.message)
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingBillingId = null
      this.billingForm = {
        client_id: '',
        invoice_number: '',
        amount: '',
        billing_date: new Date().toISOString().split('T')[0],
        due_date: '',
        status: 'pendiente',
        notes: ''
      }
    },
    
    formatCurrency(amount) {
      return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
      }).format(amount)
    },
    
    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('es-MX')
    },
    
    getStatusClass(status) {
      const classes = {
        'pendiente': 'bg-yellow-100 text-yellow-800',
        'pagada': 'bg-green-100 text-green-800',
        'vencida': 'bg-red-100 text-red-800',
        'cancelada': 'bg-gray-100 text-gray-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    
    getStatusLabel(status) {
      const labels = {
        'pendiente': 'Pendiente',
        'pagada': 'Pagada',
        'vencida': 'Vencida',
        'cancelada': 'Cancelada'
      }
      return labels[status] || status
    }
  }
}
</script>
