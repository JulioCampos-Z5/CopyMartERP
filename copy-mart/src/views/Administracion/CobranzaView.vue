<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-indigo-50 dark:bg-indigo-900/30 p-6 rounded-lg border border-indigo-200 dark:border-indigo-700">
        <h1 class="text-3xl font-bold text-indigo-800 dark:text-indigo-200 mb-2">Gestión de Cobranza</h1>
        <p class="text-indigo-600 dark:text-indigo-400">Administra las cuentas por cobrar y seguimiento de pagos</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Total por Cobrar</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ formatCurrency(stats.totalPending) }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Facturas Vencidas</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.overdueCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Cobrado este Mes</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ formatCurrency(stats.paidThisMonth) }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Pendientes</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.expiringSoon }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
        <div class="flex flex-wrap gap-4">
          <button @click="loadData" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
          <button @click="updateOverdue" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Marcar Vencidas
          </button>
          <select v-model="filters.status" class="input-field w-40">
            <option value="">Todos</option>
            <option value="pendiente">Pendiente</option>
            <option value="pagado">Pagado</option>
            <option value="vencido">Vencido</option>
          </select>
          <select v-model="filters.billing_type" class="input-field w-40">
            <option value="">Tipo</option>
            <option value="renta">Renta</option>
            <option value="venta">Venta</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white dark:bg-gray-800 p-12 rounded-lg shadow border dark:border-gray-700 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Cargando facturaciones...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/30 p-6 rounded-lg border border-red-200 dark:border-red-700">
        <p class="text-red-600">{{ error }}</p>
        <button @click="loadData" class="mt-2 text-red-700 underline">Reintentar</button>
      </div>

      <!-- Main Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Facturas por Cobrar -->
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow border dark:border-gray-700">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Facturas Pendientes de Cobro ({{ filteredBillings.length }})</h2>
          </div>
          <div class="p-6">
            <div v-if="filteredBillings.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
              No hay facturaciones registradas
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50 dark:bg-gray-700">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Factura #</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Cliente</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Monto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Vencimiento</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="billing in filteredBillings" :key="billing.billing_id">
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-indigo-600 dark:text-indigo-400">{{ billing.invoice_number || '-' }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ billing.client?.name || billing.rent?.client?.name || '-' }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ formatCurrency(billing.amount) }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ formatDate(billing.due_date) }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(billing.status)]">
                        {{ getStatusLabel(billing.status) }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm">
                      <button v-if="billing.status !== 'pagado'" @click="openPaymentModal(billing)" class="text-green-600 hover:text-green-900 mr-2">
                        Registrar Pago
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Gestión de Cobranza -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow border dark:border-gray-700">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Acciones de Cobranza</h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700 rounded-lg">
                <h4 class="text-sm font-medium text-red-800 dark:text-red-200 mb-2">Vencidas ({{ overdueBillings.length }})</h4>
                <div class="space-y-2" v-if="overdueBillings.length > 0">
                  <div v-for="billing in overdueBillings.slice(0, 5)" :key="billing.billing_id" class="flex justify-between items-center">
                    <span class="text-sm text-red-700 dark:text-red-300">{{ billing.client?.name || billing.rent?.client?.name || 'Sin cliente' }}</span>
                    <span class="text-xs text-red-600 dark:text-red-400">{{ formatCurrency(billing.amount) }}</span>
                  </div>
                </div>
                <p v-else class="text-sm text-red-600 dark:text-red-400">No hay facturas vencidas</p>
              </div>

              <div class="p-4 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700 rounded-lg">
                <h4 class="text-sm font-medium text-yellow-800 dark:text-yellow-200 mb-2">Próximas a Vencer</h4>
                <div class="space-y-2" v-if="pendingBillings.length > 0">
                  <div v-for="billing in pendingBillings.slice(0, 5)" :key="billing.billing_id" class="flex justify-between items-center">
                    <span class="text-sm text-yellow-700 dark:text-yellow-300">{{ billing.client?.name || billing.rent?.client?.name || 'Sin cliente' }}</span>
                    <span class="text-xs text-yellow-600 dark:text-yellow-400">{{ formatDate(billing.due_date) }}</span>
                  </div>
                </div>
                <p v-else class="text-sm text-yellow-600 dark:text-yellow-400">No hay facturas próximas a vencer</p>
              </div>

              <div class="p-4 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-lg">
                <h4 class="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">Estadísticas</h4>
                <div class="space-y-1 text-sm text-blue-700 dark:text-blue-300">
                  <div class="flex justify-between">
                    <span>Total Facturas:</span>
                    <span>{{ billings.length }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Pendientes:</span>
                    <span>{{ stats.expiringSoon }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Vencidas:</span>
                    <span>{{ stats.overdueCount }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Pago -->
    <div v-if="showPaymentModal && selectedBilling" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="closePaymentModal">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
        <h3 class="text-xl font-semibold mb-4 dark:text-white">Registrar Pago</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">Factura #{{ selectedBilling.billing_id }} - {{ formatCurrency(selectedBilling.amount) }}</p>
        <form @submit.prevent="registerPayment" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Pago *</label>
            <input v-model="paymentForm.payment_date" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Comentario</label>
            <textarea v-model="paymentForm.comment" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="Nota sobre el pago..."></textarea>
          </div>
          <div class="flex justify-end gap-2 pt-2">
            <button type="button" @click="closePaymentModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">Registrar Pago</button>
          </div>
        </form>
      </div>
    </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { billingService } from '@/services/billingService.ts'

export default {
  name: 'CobranzaView',
  components: {
    BaseLayout
  },
  data() {
    return {
      billings: [],
      overdueBillings: [],
      loading: false,
      error: null,
      stats: {
        totalPending: 0,
        overdueCount: 0,
        paidThisMonth: 0,
        expiringSoon: 0
      },
      filters: {
        status: '',
        billing_type: '',
        client_id: null
      },
      showPaymentModal: false,
      selectedBilling: null,
      paymentForm: {
        payment_date: new Date().toISOString().split('T')[0],
        comment: ''
      }
    }
  },
  computed: {
    filteredBillings() {
      return this.billings.filter(billing => {
        if (this.filters.status && billing.status !== this.filters.status) return false
        if (this.filters.billing_type && billing.billing_type !== this.filters.billing_type) return false
        return true
      })
    },
    pendingBillings() {
      return this.billings.filter(b => b.status === 'pendiente')
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      this.error = null
      try {
        const [billingsResponse, overdue, statsData] = await Promise.all([
          billingService.getBillings({ is_active: true }),
          billingService.getOverdueBillings(),
          billingService.getStats()
        ])
        
        this.billings = billingsResponse.items || []
        this.overdueBillings = overdue
        
        // Calcular total pendiente desde las facturas reales
        const pendientes = this.billings.filter(b => b.status === 'pendiente' || b.status === 'vencido')
        this.stats.totalPending = pendientes.reduce((sum, b) => {
          const val = Number(b.amount || 0)
          return sum + (isNaN(val) ? 0 : val)
        }, 0)
        this.stats.overdueCount = this.overdueBillings.length || statsData.by_status?.vencido || 0
        this.stats.paidThisMonth = statsData.paid_amount || 0
        this.stats.expiringSoon = this.billings.filter(b => b.status === 'pendiente').length
      } catch (err) {
        this.error = err.message
        console.error('Error loading billings:', err)
      } finally {
        this.loading = false
      }
    },

    getStatusClass(status) {
      const classes = {
        'pendiente': 'bg-yellow-100 text-yellow-800',
        'pagado': 'bg-green-100 text-green-800',
        'vencido': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },

    getStatusLabel(status) {
      const labels = {
        'pendiente': 'Pendiente',
        'pagado': 'Pagado',
        'vencido': 'Vencido'
      }
      return labels[status] || status
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

    openPaymentModal(billing) {
      this.selectedBilling = billing
      this.paymentForm = {
        payment_date: new Date().toISOString().split('T')[0],
        comment: ''
      }
      this.showPaymentModal = true
    },

    async registerPayment() {
      if (!this.selectedBilling) return
      try {
        await billingService.markAsPaid(this.selectedBilling.billing_id, this.paymentForm)
        this.showPaymentModal = false
        this.selectedBilling = null
        await this.loadData()
      } catch (err) {
        alert('Error al registrar pago: ' + err.message)
      }
    },

    async updateOverdue() {
      try {
        const result = await billingService.updateOverdueBillings()
        alert(`Se actualizaron ${result.updated} facturaciones a estado vencido`)
        await this.loadData()
      } catch (err) {
        alert('Error: ' + err.message)
      }
    },

    closePaymentModal() {
      this.showPaymentModal = false
      this.selectedBilling = null
    }
  }
}
</script>