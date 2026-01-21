<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <button @click="$router.back()" class="text-green-600 hover:text-green-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Compras
        </button>
      </div>

      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>

      <div v-else-if="purchase" class="space-y-6">
        <!-- Header con acciones -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ purchase.name }}</h1>
              <span :class="getStatusBadgeClass(purchase.status)">{{ purchase.status }}</span>
            </div>
            <div class="flex gap-2">
              <button @click="editPurchase" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2">
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
                <dt class="text-sm font-medium text-gray-500">Nombre</dt>
                <dd class="text-base text-gray-900 mt-1">{{ purchase.name }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Tipo</dt>
                <dd class="text-base text-gray-900 mt-1">{{ purchase.type }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Cantidad</dt>
                <dd class="text-base text-gray-900 mt-1">{{ purchase.amount }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Calidad</dt>
                <dd class="text-base text-gray-900 mt-1">{{ purchase.quality || '-' }}</dd>
              </div>
            </dl>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Información de Envío</h2>
            <dl class="space-y-3">
              <div>
                <dt class="text-sm font-medium text-gray-500">Código de Envío</dt>
                <dd class="text-base text-gray-900 mt-1 font-mono">{{ purchase.shipping_code || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Método de Envío</dt>
                <dd class="text-base text-gray-900 mt-1">{{ purchase.shipping_method || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Costo de Envío</dt>
                <dd class="text-base text-gray-900 mt-1">{{ formatCurrency(purchase.shipping_cost) }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <!-- Detalles adicionales -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Detalles Adicionales</h2>
          <dl class="space-y-3">
            <div>
              <dt class="text-sm font-medium text-gray-500">Justificación</dt>
              <dd class="text-base text-gray-900 mt-1">{{ purchase.justification || '-' }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Comentarios</dt>
              <dd class="text-base text-gray-900 mt-1">{{ purchase.comments || '-' }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Fecha de Creación</dt>
              <dd class="text-base text-gray-900 mt-1">{{ formatDate(purchase.created_at) }}</dd>
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
import { purchaseService } from '@/services/purchaseService.ts'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const purchase = ref(null)

const loadPurchase = async () => {
  loading.value = true
  try {
    purchase.value = await purchaseService.getPurchaseById(route.params.id)
  } catch (error) {
    console.error('Error loading purchase:', error)
    alert('Error al cargar la compra')
  } finally {
    loading.value = false
  }
}

const editPurchase = () => {
  router.push({ name: 'CompraEditar', params: { id: route.params.id } })
}

const getStatusBadgeClass = (status) => {
  const statusColors = {
    'En Curso': 'bg-yellow-100 text-yellow-800',
    'En Tránsito': 'bg-blue-100 text-blue-800',
    'Concluido': 'bg-green-100 text-green-800',
    'Pausado Back Orders': 'bg-orange-100 text-orange-800',
    'Falta Pago Proveedor': 'bg-red-100 text-red-800',
    'Falta Factura': 'bg-pink-100 text-pink-800',
    'Por Revisar': 'bg-purple-100 text-purple-800',
    'Solicitud Guía Almacén': 'bg-indigo-100 text-indigo-800',
    'Rechazado': 'bg-gray-100 text-gray-800'
  }
  return `px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full ${statusColors[status] || 'bg-gray-100 text-gray-800'}`
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatCurrency = (amount) => {
  if (!amount) return '-'
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount)
}

onMounted(() => {
  loadPurchase()
})
</script>
