<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-gradient-to-r from-orange-50 to-amber-50 p-6 rounded-lg border border-orange-200 mb-6">
        <h1 class="text-3xl font-bold text-orange-800 mb-2">Sistema de Facturación</h1>
        <p class="text-orange-600">Genera y administra facturas fiscales y no fiscales</p>
      </div>

      <BaseTable
        :columns="columns"
        :data="billings"
        :loading="loading"
        :error="error"
        :pagination="pagination"
        :searchable="true"
        search-placeholder="Buscar por folio, cliente..."
        empty-text="No hay facturas registradas"
        @search="handleSearch"
        @page-change="handlePageChange"
      >
        <!-- Filtros -->
        <template #filters>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="localFilters.status" @change="handleFilterChange('status', localFilters.status)" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="">Todos</option>
                <option value="pendiente">Pendiente</option>
                <option value="pagado">Pagado</option>
                <option value="vencido">Vencido</option>
                <option value="cancelado">Cancelado</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="localFilters.type" @change="handleFilterChange('type', localFilters.type)" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="">Todos</option>
                <option value="venta">Venta</option>
                <option value="renta">Renta</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Desde</label>
              <input v-model="localFilters.startDate" @change="handleFilterChange('startDate', localFilters.startDate)" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Hasta</label>
              <input v-model="localFilters.endDate" @change="handleFilterChange('endDate', localFilters.endDate)" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
          </div>
        </template>

        <!-- Estadísticas -->
        <template #stats>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">Total Facturas</div>
            <div class="text-2xl font-bold text-gray-900">{{ stats.total || 0 }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">Pendientes</div>
            <div class="text-2xl font-bold text-red-600">{{ stats.pending || 0 }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">Pagadas</div>
            <div class="text-2xl font-bold text-green-600">{{ stats.paid || 0 }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">Total Monto</div>
            <div class="text-2xl font-bold text-blue-600">{{ formatCurrency(stats.totalAmount) }}</div>
          </div>
        </template>

        <!-- Acciones principales -->
        <template #actions>
          <button @click="goToCreate" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Factura
          </button>
          <button @click="loadBillings" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
        </template>

        <!-- Celda de estado personalizada -->
        <template #cell-status="{ value }">
          <span :class="getStatusBadgeClass(value)">
            {{ value.charAt(0).toUpperCase() + value.slice(1) }}
          </span>
        </template>

        <!-- Celda de tipo personalizada -->
        <template #cell-type="{ value }">
          <span :class="value === 'fiscal' ? 'px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full' : 'px-2 py-1 bg-purple-100 text-purple-800 text-xs font-semibold rounded-full'">
            {{ value === 'fiscal' ? 'Fiscal' : 'No Fiscal' }}
          </span>
        </template>

        <!-- Celda de monto -->
        <template #cell-amount="{ value }">
          <span class="font-semibold text-gray-900">{{ formatCurrency(value) }}</span>
        </template>

        <!-- Acciones por fila -->
        <template #row-actions="{ row }">
          <div class="flex gap-2 justify-end">
            <button @click="viewDetails(row)" class="text-blue-600 hover:text-blue-800" title="Ver detalles">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
            <button v-if="canEdit(row)" @click="editBilling(row)" class="text-green-600 hover:text-green-800" title="Editar">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button v-if="canMarkAsPaid(row)" @click="markAsPaid(row)" class="text-indigo-600 hover:text-indigo-800" title="Marcar como pagada">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
            <button v-if="canToggleFollowUp(row)" @click="toggleFollowUp(row)" :class="row.follow_up ? 'text-yellow-600 hover:text-yellow-800' : 'text-gray-400 hover:text-gray-600'" :title="row.follow_up ? 'Quitar seguimiento' : 'Marcar para seguimiento'">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </button>
          </div>
        </template>
      </BaseTable>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseTable from '@/components/BaseTable.vue'
import { billingService } from '@/services/billingService'
import { useAuthStore } from '@/stores/auth'
import { useFiltersStore } from '@/stores/filters'
import type { Billing } from '@/types'

// Router
const router = useRouter()

// Stores
const authStore = useAuthStore()
const filtersStore = useFiltersStore()

// Estado local
const billings = ref<Billing[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// Filtros locales que se sincronizan con el store
const localFilters = ref({
  status: '',
  type: '',
  startDate: '',
  endDate: ''
})

// Computados desde stores
const filters = computed(() => filtersStore.filters.billings || {})
const pagination = computed(() => filtersStore.pagination.billings || { page: 1, page_size: 10, total: 0, total_pages: 0 })

const stats = ref({
  total: 0,
  pending: 0,
  paid: 0,
  totalAmount: 0
})

const columns = [
  {
    key: 'billing_id',
    label: 'ID',
    cellClass: 'text-sm font-medium text-gray-900'
  },
  {
    key: 'client_name',
    label: 'Cliente',
        format: (row: Billing) => row.client?.name || row.client_name || '-',
    cellClass: 'text-sm text-gray-900'
  },
  {
    key: 'billing_type',
    label: 'Tipo',
    format: (row: Billing) => row.billing_type === 'Venta' ? 'Venta' : 'Renta',
    cellClass: 'text-sm'
  },
  {
    key: 'reference',
    label: 'Referencia',
    format: (row: Billing) => {
      if (row.sale) {
        return `Venta: ${row.sale.invoice_number || row.sale.sale_id} - ${formatCurrency(row.sale.sale_price)}`
      } else if (row.rent) {
        return `Renta: ${row.rent.contract_number || row.rent.rent_id} - ${formatCurrency(row.rent.rent)}`
      }
      return '-'
    },
    cellClass: 'text-sm text-gray-600'
  },
  {
    key: 'status',
    label: 'Estado',
    badge: true,
    cellClass: 'text-sm'
  },
  {
    key: 'amount_total',
    label: 'Monto',
    format: (row: Billing) => formatCurrency(row.amount_total || row.amount),
    cellClass: 'text-sm text-gray-900'
  },
  {
    key: 'target_date',
    label: 'Fecha Objetivo',
    format: (row: Billing) => formatDate(row.target_date),
    cellClass: 'text-sm text-gray-600'
  },
  {
    key: 'due_date',
    label: 'Vencimiento',
    format: (row: Billing) => formatDate(row.due_date),
    cellClass: 'text-sm text-gray-600'
  }
]

const loadBillings = async () => {
  loading.value = true
  error.value = null
  try {
    const options = filtersStore.getRequestConfig('billings')
    const response = await billingService.getBillings(options)
    
    billings.value = response.items || []
    filtersStore.setPagination('billings', {
      page: response.page || 1,
      page_size: response.page_size || 10,
      total: response.total || 0,
      total_pages: response.total_pages || 0
    })
    
    calculateStats()
  } catch (err: any) {
    error.value = err.message || 'Error al cargar las facturas'
    console.error('Error loading billings:', err)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.value.total = pagination.value.total
  stats.value.pending = billings.value.filter(b => String(b.status).toLowerCase() === 'pendiente').length
  stats.value.paid = billings.value.filter(b => String(b.status).toLowerCase() === 'pagado').length
  stats.value.totalAmount = billings.value.reduce((sum, b) => sum + (b.amount_total || b.amount || 0), 0)
}

const handleSearch = (query: string) => {
  filtersStore.setFilter('billings', 'search', query)
  filtersStore.setPage('billings', 1)
  loadBillings()
}

const handlePageChange = (page: number) => {
  filtersStore.setPage('billings', page)
  loadBillings()
}

const handleFilterChange = (key: string, value: any) => {
  filtersStore.setFilter('billings', key, value)
  filtersStore.setPage('billings', 1)
  loadBillings()
}

const getStatusBadgeClass = (status: string): string => {
  const statusColors: Record<string, string> = {
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'pagada': 'bg-green-100 text-green-800',
    'vencida': 'bg-red-100 text-red-800',
    'cancelada': 'bg-gray-100 text-gray-800'
  }
  return `px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${statusColors[status] || 'bg-gray-100 text-gray-800'}`
}

const viewDetails = (billing: Billing) => {
  router.push({ name: 'FacturacionDetalle', params: { id: billing.billing_id } })
}

const editBilling = (billing: Billing) => {
  router.push({ name: 'FacturacionEditar', params: { id: billing.billing_id } })
}

const goToCreate = () => {
  router.push({ name: 'FacturacionNueva' })
}

const markAsPaid = async (billing: Billing) => {
  if (!confirm(`¿Marcar factura #${billing.billing_id} como pagada?`)) return
  
  try {
    await billingService.markAsPaid(billing.billing_id, {
      payment_date: new Date().toISOString().split('T')[0],
      payment_method: 'efectivo'
    })
    await loadBillings()
  } catch (err: any) {
    alert('Error al marcar como pagada: ' + err.message)
  }
}

const toggleFollowUp = async (billing: Billing) => {
  try {
    await billingService.toggleFollowUp(billing.billing_id, !billing.follow_up)
    await loadBillings()
  } catch (err: any) {
    alert('Error al cambiar seguimiento: ' + err.message)
  }
}

const canEdit = (billing: Billing): boolean => {
  if (!authStore.hasPermission('update_billing')) return false
  const status = String(billing.status).toLowerCase()
  return status !== 'pagado' && status !== 'cancelado'
}

const canMarkAsPaid = (billing: Billing): boolean => {
  if (!authStore.hasPermission('update_billing')) return false
  const status = String(billing.status).toLowerCase()
  return status === 'pendiente' || status === 'vencido'
}

const canToggleFollowUp = (billing: Billing): boolean => {
  if (!authStore.hasPermission('update_billing')) return false
  const status = String(billing.status).toLowerCase()
  return status !== 'cancelado'
}

const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' })
}

const formatCurrency = (amount: number | null | undefined): string => {
  if (!amount) return '-'
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount)
}

onMounted(() => {
  filtersStore.initialize()
  
  // Limpiar valores antiguos incompatibles del filtro de estado
  const currentFilters = filtersStore.filters.billings || {}
  const currentStatus = currentFilters.status
  
  if (currentStatus && !['pendiente', 'pagado', 'vencido', 'cancelado', ''].includes(currentStatus)) {
    filtersStore.setFilter('billings', 'status', '')
    localFilters.value.status = ''
  } else {
    localFilters.value.status = currentStatus || ''
  }
  
  // Sincronizar otros filtros
  localFilters.value.type = currentFilters.billing_type || currentFilters.type || ''
  localFilters.value.startDate = currentFilters.startDate || currentFilters.start_date || ''
  localFilters.value.endDate = currentFilters.endDate || currentFilters.end_date || ''
  
  loadBillings()
})
</script>
