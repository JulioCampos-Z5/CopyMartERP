<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6 flex justify-between items-start">
        <div>
          <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Volver a Ventas
          </button>
          <h1 class="text-3xl font-bold text-gray-900">Detalle de Venta</h1>
          <p class="text-gray-600 mt-1">Folio: <span class="font-semibold text-blue-600">{{ sale?.invoice_number || `#${saleId}` }}</span></p>
        </div>
        <div class="flex gap-2">
          <button @click="editSale" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Editar
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando información...</p>
      </div>

      <!-- Content -->
      <div v-else-if="sale" class="space-y-6">
        <!-- Estado Badge -->
        <div class="flex items-center gap-4">
          <span :class="getSaleStatusClass(sale.sale_status)" class="px-4 py-2 rounded-full text-sm font-semibold">
            {{ getSaleStatusLabel(sale.sale_status) }}
          </span>
          <span v-if="sale.is_foreign" class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
            Foráneo
          </span>
        </div>

        <!-- Tabs -->
        <div class="bg-white rounded-lg shadow border">
          <div class="border-b border-gray-200">
            <nav class="flex -mb-px">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id 
                    ? 'border-blue-500 text-blue-600 bg-blue-50' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm flex items-center gap-2'
                ]"
              >
                {{ tab.label }}
                <span v-if="tab.count !== undefined" class="ml-1 px-2 py-0.5 text-xs rounded-full" 
                  :class="activeTab === tab.id ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'">
                  {{ tab.count }}
                </span>
              </button>
            </nav>
          </div>
        </div>

        <!-- Tab: Información General -->
        <div v-if="activeTab === 'info'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Datos de la Venta -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Datos de la Venta
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Número de Factura</span>
                <span class="font-medium">{{ sale.invoice_number || 'Sin asignar' }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Precio de Venta</span>
                <span class="font-bold text-green-600 text-xl">${{ formatNumber(sale.sale_price) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Estado</span>
                <span :class="getSaleStatusClass(sale.sale_status)" class="px-2 py-1 text-xs rounded-full font-medium">
                  {{ getSaleStatusLabel(sale.sale_status) }}
                </span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Foráneo</span>
                <span class="font-medium">{{ sale.is_foreign ? 'Sí' : 'No' }}</span>
              </div>
              <div class="flex justify-between py-2">
                <span class="text-gray-500">Creado</span>
                <span class="font-medium text-sm">{{ formatDateTime(sale.created_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Datos del Cliente -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Cliente
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Nombre</span>
                <span class="font-medium">{{ sale.client?.name || `Cliente #${sale.client_id}` }}</span>
              </div>
              <div class="flex justify-between py-2 border-b">
                <span class="text-gray-500">Sucursal</span>
                <span class="font-medium">{{ sale.branch?.name || 'Sin asignar' }}</span>
              </div>
              <div class="flex justify-between py-2">
                <span class="text-gray-500">Área</span>
                <span class="font-medium">{{ sale.area?.name || 'Sin asignar' }}</span>
              </div>
            </div>
          </div>

          <!-- Datos del Equipo -->
          <div class="bg-white rounded-lg shadow border p-6 lg:col-span-2">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Equipo Vendido
            </h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-xs text-gray-500 mb-1">SKU</p>
                <p class="font-medium font-mono">{{ sale.equipment?.sku || '-' }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-xs text-gray-500 mb-1">Modelo</p>
                <p class="font-medium">{{ sale.equipment?.model || '-' }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-xs text-gray-500 mb-1">Serie</p>
                <p class="font-medium font-mono">{{ sale.equipment?.serie || '-' }}</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-xs text-gray-500 mb-1">Tipo</p>
                <p class="font-medium capitalize">{{ sale.equipment?.type || '-' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Facturas -->
        <div v-if="activeTab === 'billings'" class="space-y-6">
          <div class="bg-white rounded-lg shadow border p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Factura Asociada</h2>
            </div>

            <div v-if="loadingBillings" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>

            <div v-else-if="billings.length > 0" class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Factura</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vencimiento</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="billing in billings" :key="billing.billing_id" class="hover:bg-gray-50">
                    <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ billing.invoice_number || `#${billing.billing_id}` }}</td>
                    <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(billing.target_date) }}</td>
                    <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(billing.due_date) }}</td>
                    <td class="px-4 py-3 text-sm font-semibold text-green-600">${{ formatNumber(billing.amount) }}</td>
                    <td class="px-4 py-3">
                      <span :class="getBillingStatusClass(billing.status)" class="px-2 py-1 text-xs rounded-full font-medium">
                        {{ getBillingStatusLabel(billing.status) }}
                      </span>
                    </td>
                    <td class="px-4 py-3">
                      <button @click="viewBilling(billing.billing_id)" class="text-blue-600 hover:text-blue-800">
                        Ver detalle
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p>No hay factura generada para esta venta</p>
              <p class="text-sm mt-2">La factura se genera automáticamente cuando la venta está confirmada</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="bg-red-50 border border-red-200 rounded-lg p-8 text-center">
        <svg class="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Error al cargar la venta</h2>
        <p class="text-gray-600 mb-4">No se pudo cargar la información de la venta #{{ saleId }}</p>
        <button @click="goBack" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          Volver a Ventas
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppNavigation from '@/components/AppNavigation.vue'
import { saleService } from '@/services/saleService'
import { billingService } from '@/services/billingService'

const route = useRoute()
const router = useRouter()

const saleId = computed(() => Number(route.params.id))
const loading = ref(true)
const sale = ref<any>(null)
const activeTab = ref('info')

// Billings
const billings = ref<any[]>([])
const loadingBillings = ref(false)

const tabs = computed(() => [
  { id: 'info', label: 'Información' },
  { id: 'billings', label: 'Facturas', count: billings.value.length }
])

// Load Data
const loadSale = async () => {
  loading.value = true
  try {
    sale.value = await saleService.getSaleById(saleId.value)
  } catch (error) {
    console.error('Error loading sale:', error)
    sale.value = null
  } finally {
    loading.value = false
  }
}

const loadBillings = async () => {
  loadingBillings.value = true
  try {
    const response = await billingService.getBillings({ sale_id: saleId.value })
    billings.value = response.items || []
  } catch (error) {
    console.error('Error loading billings:', error)
    billings.value = []
  } finally {
    loadingBillings.value = false
  }
}

// Actions
const editSale = () => {
  router.push(`/ventas/${saleId.value}/editar`)
}

const viewBilling = (billingId: number) => {
  router.push(`/facturacion/${billingId}`)
}

// Helpers
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' })
}

const formatDateTime = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('es-MX')
}

const formatNumber = (num: any) => {
  if (num === null || num === undefined) return '0'
  return Number(num).toLocaleString('es-MX', { minimumFractionDigits: 2 })
}

const getSaleStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'confirmada': 'bg-green-100 text-green-800',
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'entregada': 'bg-blue-100 text-blue-800',
    'cancelada': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getSaleStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    'confirmada': 'Confirmada',
    'pendiente': 'Pendiente',
    'entregada': 'Entregada',
    'cancelada': 'Cancelada'
  }
  return labels[status] || status
}

const getBillingStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'pagado': 'bg-green-100 text-green-800',
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'vencido': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getBillingStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    'pagado': 'Pagado',
    'pendiente': 'Pendiente',
    'vencido': 'Vencido'
  }
  return labels[status] || status
}

const goBack = () => {
  router.push('/ventas')
}

onMounted(async () => {
  await loadSale()
  await loadBillings()
})
</script>
