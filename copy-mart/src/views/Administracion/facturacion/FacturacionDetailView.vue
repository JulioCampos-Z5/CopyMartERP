<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <button @click="$router.back()" class="text-orange-600 hover:text-orange-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Facturación
        </button>
      </div>

      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
      </div>

      <div v-else-if="billing" class="space-y-6">
        <!-- Header con acciones -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 mb-2">Factura {{ billing.client?.name || billing.client_name || 'Sin cliente' }}</h1>
              <div class="flex gap-2 items-center">
                <span :class="getStatusBadgeClass(billing.status)">{{ billing.status }}</span>
                <span v-if="billing.follow_up" class="px-3 py-1 bg-amber-100 text-amber-800 text-sm font-semibold rounded-full">
                  En Seguimiento
                </span>
              </div>
            </div>
            <div class="flex gap-2">
              <button @click="generatePdf" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                Generar PDF
              </button>
              <button @click="editBilling" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar
              </button>
            </div>
          </div>
        </div>

        <!-- Información principal -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Información General</h2>
            <dl class="space-y-3">
              <div>
                <dt class="text-sm font-medium text-gray-500">Cliente</dt>
                <dd class="text-base text-gray-900 mt-1 font-medium">{{ billing.client?.name || billing.client_name || '-' }}</dd>
              </div>
              <div v-if="billing.branch?.name || billing.branch?.name || billing.branch_name">
                <dt class="text-sm font-medium text-gray-500">Sucursal</dt>
                <dd class="text-base text-gray-900 mt-1">{{ billing.branch?.name || billing.branch_name }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Tipo de Factura</dt>
                <dd class="text-base text-gray-900 mt-1">{{ billing.billing_type }}</dd>
              </div>
              <div v-if="billing.sale">
                <dt class="text-sm font-medium text-gray-500">Venta Asociada</dt>
                <dd class="text-base text-gray-900 mt-1">
                  <span class="font-medium">{{ billing.sale.invoice_number || `#${billing.sale.sale_id}` }}</span>
                  <span class="text-gray-600"> - {{ formatCurrency(billing.sale.sale_price) }}</span>
                </dd>
              </div>
              <div v-if="billing.rent">
                <dt class="text-sm font-medium text-gray-500">Renta Asociada</dt>
                <dd class="text-base text-gray-900 mt-1">
                  <span class="font-medium">{{ billing.rent.contract_number || `#${billing.rent.rent_id}` }}</span>
                  <span class="text-gray-600"> - {{ formatCurrency(billing.rent.rent) }}/mes</span>
                </dd>
              </div>
            </dl>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Montos</h2>
            <dl class="space-y-3">
              <div v-if="billing.amount_subtotal || billing.amount">
                <dt class="text-sm font-medium text-gray-500">Subtotal</dt>
                <dd class="text-base text-gray-900 mt-1">{{ formatCurrency(billing.amount_subtotal || (billing.amount * 0.86)) }}</dd>
              </div>
              <div v-if="billing.amount_tax || billing.amount">
                <dt class="text-sm font-medium text-gray-500">IVA</dt>
                <dd class="text-base text-gray-900 mt-1">{{ formatCurrency(billing.amount_tax || (billing.amount * 0.16)) }}</dd>
              </div>
              <div class="pt-2 border-t">
                <dt class="text-sm font-medium text-gray-500">Total</dt>
                <dd class="text-2xl font-bold text-gray-900 mt-1">{{ formatCurrency(billing.amount_total || billing.amount) }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <!-- Fechas -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Fechas</h2>
          <dl class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <dt class="text-sm font-medium text-gray-500">Fecha Objetivo</dt>
              <dd class="text-base text-gray-900 mt-1">{{ formatDate(billing.target_date) }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Fecha Vencimiento</dt>
              <dd class="text-base text-gray-900 mt-1">{{ formatDate(billing.due_date) }}</dd>
            </div>
            <div v-if="billing.payment_date">
              <dt class="text-sm font-medium text-gray-500">Fecha de Pago</dt>
              <dd class="text-base text-green-600 mt-1 font-medium">{{ formatDate(billing.payment_date) }}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import { billingService } from '@/services/billingService'
import { usePdfGenerator } from '@/composables/usePdfGenerator'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const billing = ref(null)
const { generateInvoicePdf } = usePdfGenerator()

const loadBilling = async () => {
  loading.value = true
  try {
    billing.value = await billingService.getBillingById(route.params.id)
  } catch (error) {
    console.error('Error loading billing:', error)
    alert('Error al cargar la factura')
  } finally {
    loading.value = false
  }
}

const editBilling = () => {
  router.push({ name: 'FacturacionEditar', params: { id: route.params.id } })
}

const generatePdf = () => {
  if (!billing.value) {
    alert('No hay datos de factura disponibles')
    return
  }
  
  try {
    const invoiceData = {
      billing_id: billing.value.billing_id,
      client_name: billing.value.client?.name || billing.value.client_name || 'Cliente',
      branch_name: billing.value.branch?.name || billing.value.branch_name || '',
      billing_type: billing.value.billing_type,
      invoice_number: billing.value.invoice_number || `FAC-${billing.value.billing_id}`,
      target_date: formatDate(billing.value.target_date),
      due_date: formatDate(billing.value.due_date),
      payment_date: billing.value.payment_date ? formatDate(billing.value.payment_date) : null,
      status: String(billing.value.status || 'pendiente'),
      amount_subtotal: Number(billing.value.amount_subtotal || (billing.value.amount * 0.86)),
      amount_tax: Number(billing.value.amount_tax || (billing.value.amount * 0.16)),
      amount_total: Number(billing.value.amount_total || billing.value.amount),
      sale_info: billing.value.sale ? {
        invoice_number: billing.value.sale.invoice_number || `#${billing.value.sale.sale_id}`,
        amount: Number(billing.value.sale.sale_price)
      } : null,
      rent_info: billing.value.rent ? {
        contract_number: billing.value.rent.contract_number || `#${billing.value.rent.rent_id}`,
        amount: Number(billing.value.rent.rent)
      } : null,
      comment: billing.value.comment
    }
    
    const filename = `Factura-${billing.value.billing_id}-${billing.value.client?.name || 'Cliente'}.pdf`
    const result = generateInvoicePdf(invoiceData, filename, true)
    
    if (result && result.success && result.previewUrl) {
      window.open(result.previewUrl, '_blank')
    } else if (result && !result.success) {
      console.error('Error generando PDF:', result.message)
      alert(`Error al generar el PDF: ${result.message || 'Error desconocido'}`)
    } else {
      console.error('Resultado inesperado:', result)
      alert('Error al generar el PDF')
    }
  } catch (error) {
    console.error('Error en generatePdf:', error)
    alert(`Error al generar el PDF: ${error.message || error}`)
  }
}

const getStatusBadgeClass = (status) => {
  const statusColors = {
    'Pendiente': 'bg-yellow-100 text-yellow-800',
    'Pagado': 'bg-green-100 text-green-800',
    'Vencido': 'bg-red-100 text-red-800',
    'Cancelado': 'bg-gray-100 text-gray-800'
  }
  return `px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full ${statusColors[status] || 'bg-gray-100 text-gray-800'}`
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatCurrency = (amount) => {
  if (!amount) return '$0.00'
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount)
}

onMounted(() => {
  loadBilling()
})
</script>
