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
        <h1 class="text-3xl font-bold text-gray-900">{{ isEditing ? 'Editar' : 'Nueva' }} Factura</h1>
      </div>

      <form @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow-md p-6 space-y-6">
        <!-- Información básica -->
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Información Básica</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Factura *</label>
              <select v-model="form.billing_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="venta">Venta</option>
                <option value="renta">Renta</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
              <select v-model="form.client_id" required @change="loadClientData" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="">Seleccione...</option>
                <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                  {{ client.name }}
                </option>
              </select>
            </div>
            <div v-if="form.billing_type === 'venta'" class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Venta *</label>
              <select v-model="form.sale_id" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="">Seleccione una venta...</option>
                <option v-for="sale in sales" :key="sale.sale_id" :value="sale.sale_id">
                  Factura: {{ sale.invoice_number || `#${sale.sale_id}` }} | Cliente: {{ sale.client_name || 'N/A' }} | Monto: {{ formatCurrency(sale.total_amount) }}
                </option>
              </select>
              <p v-if="sales.length === 0 && form.client_id" class="text-sm text-gray-500 mt-1">No hay ventas disponibles para este cliente</p>
            </div>
            <div v-if="form.billing_type === 'renta'" class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Renta *</label>
              <select v-model="form.rent_id" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="">Seleccione una renta...</option>
                <option v-for="rent in rents" :key="rent.rent_id" :value="rent.rent_id">
                  Contrato: {{ rent.contract_number || `#${rent.rent_id}` }} | Cliente: {{ rent.client_name || 'N/A' }} | Renta Mensual: {{ formatCurrency(rent.monthly_rent) }}
                </option>
              </select>
              <p v-if="rents.length === 0 && form.client_id" class="text-sm text-gray-500 mt-1">No hay rentas disponibles para este cliente</p>
            </div>
          </div>
        </div>

        <!-- Fechas -->
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Fechas</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Objetivo *</label>
              <input v-model="form.target_date" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Vencimiento *</label>
              <input v-model="form.due_date" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
              <select v-model="form.status" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                <option value="pendiente">Pendiente</option>
                <option value="pagado">Pagado</option>
                <option value="vencido">Vencido</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Opciones adicionales -->
        <div>
          <div class="flex items-center gap-2 mb-4">
            <input v-model="form.follow_up" type="checkbox" id="followUp" class="rounded text-orange-600 focus:ring-orange-500" />
            <label for="followUp" class="text-sm font-medium text-gray-700">Marcar para seguimiento</label>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
            <textarea v-model="form.comment" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" placeholder="Comentarios adicionales..."></textarea>
          </div>
        </div>

        <!-- Botones -->
        <div class="flex justify-end gap-3 pt-4">
          <button type="button" @click="$router.back()" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button type="submit" :disabled="loading" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50">
            {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear') }} Factura
          </button>
        </div>
      </form>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import { billingService } from '@/services/billingService'
import { clientService } from '@/services/clientService'
import { saleService } from '@/services/saleService'
import { rentService } from '@/services/rentService'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const clients = ref([])
const sales = ref([])
const rents = ref([])

const form = ref({
  billing_type: 'venta',
  client_id: '',
  sale_id: '',
  rent_id: '',
  target_date: '',
  due_date: '',
  status: 'pendiente',
  follow_up: false,
  comment: ''
})

const isEditing = computed(() => !!route.params.id)

const loadBilling = async () => {
  if (!isEditing.value) return
  try {
    const billing = await billingService.getBillingById(route.params.id)
    
    // Mapear los campos del billing a form
    form.value = {
      billing_type: String(billing.billing_type).toLowerCase(),
      client_id: billing.client_id,
      sale_id: billing.sale_id || '',
      rent_id: billing.rent_id || '',
      target_date: billing.target_date,
      due_date: billing.due_date,
      status: String(billing.status).toLowerCase(),
      follow_up: billing.follow_up,
      comment: billing.comment || ''
    }
    
    // Cargar las ventas/rentas del cliente
    await loadClientData()
  } catch (error) {
    console.error('Error loading billing:', error)
    alert('Error al cargar la factura')
  }
}

const loadClients = async () => {
  try {
    const response = await clientService.getClients({ pageSize: 1000 })
    clients.value = response.items || []
  } catch (error) {
    console.error('Error loading clients:', error)
  }
}

const loadClientData = async () => {
  if (!form.value.client_id) return
  try {
    const [salesResp, rentsResp] = await Promise.all([
      saleService.getSales({ client_id: form.value.client_id, pageSize: 100 }),
      rentService.getRents({ client_id: form.value.client_id, pageSize: 100 })
    ])
    sales.value = salesResp.items || []
    rents.value = rentsResp.items || []
  } catch (error) {
    console.error('Error loading client data:', error)
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    // Preparar datos según lo que espera el backend
    const payload = {
      billing_type: form.value.billing_type,
      target_date: form.value.target_date,
      due_date: form.value.due_date,
      follow_up: form.value.follow_up,
      comment: form.value.comment
    }

    // Agregar rent_id o sale_id según el tipo
    if (form.value.billing_type === 'venta' && form.value.sale_id) {
      payload.sale_id = Number(form.value.sale_id)
    } else if (form.value.billing_type === 'renta' && form.value.rent_id) {
      payload.rent_id = Number(form.value.rent_id)
    }

    if (isEditing.value) {
      await billingService.updateBilling(route.params.id, payload)
    } else {
      await billingService.createBilling(payload)
    }
    router.push({ name: 'Facturacion' })
  } catch (error) {
    console.error('Error saving billing:', error)
    alert(`Error al guardar la factura: ${error.message || error}`)
  } finally {
    loading.value = false
  }
}

const formatCurrency = (amount) => {
  if (!amount) return '$0.00'
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount)
}

onMounted(() => {
  loadClients()
  loadBilling()
})
</script>
