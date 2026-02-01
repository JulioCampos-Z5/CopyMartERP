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
        <h1 class="text-3xl font-bold text-gray-900">{{ isEditing ? 'Editar' : 'Nueva' }} Compra</h1>
      </div>

      <form @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow-md p-6 space-y-6">
        <!-- Información básica -->
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Información Básica</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
              <input v-model="form.name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Refacción *</label>
              <select v-model="form.sparepart_id" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                <option value="">Seleccione...</option>
                <option v-for="sp in spareparts" :key="sp.sparepart_id" :value="sp.sparepart_id">
                  {{ sp.name }} - {{ sp.sku }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad Solicitada *</label>
              <input v-model.number="form.amount" type="number" min="1" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad Autorizada</label>
              <input v-model.number="form.authorized_amount" type="number" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
              <select v-model="form.type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                <option value="Interna">Interna</option>
                <option value="Venta">Venta</option>
              </select>
            </div>
            <div v-if="form.type === 'Venta'">
              <label class="block text-sm font-medium text-gray-700 mb-1">¿Está Pagado?</label>
              <select v-model="form.is_paid" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                <option :value="null">Sin Confirmar</option>
                <option :value="true">Sí - Pagado</option>
                <option :value="false">No - Pendiente</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Proveedores (máximo 3) -->
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Cotizaciones de Proveedores</h2>
          <div class="space-y-4">
            <!-- Proveedor 1 -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <h3 class="font-medium text-gray-800 mb-3">Proveedor 1</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                  <input v-model="form.supplier1_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
                  <input v-model.number="form.supplier1_cost" type="number" step="0.01" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                </div>
              </div>
            </div>
            
            <!-- Proveedor 2 -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <h3 class="font-medium text-gray-800 mb-3">Proveedor 2</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                  <input v-model="form.supplier2_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
                  <input v-model.number="form.supplier2_cost" type="number" step="0.01" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                </div>
              </div>
            </div>
            
            <!-- Proveedor 3 -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <h3 class="font-medium text-gray-800 mb-3">Proveedor 3</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                  <input v-model="form.supplier3_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
                  <input v-model.number="form.supplier3_cost" type="number" step="0.01" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Archivos -->
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Documentos</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Archivo de Cotización</label>
              <input v-model="form.quotation_file" type="text" placeholder="URL o ruta del archivo" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Archivo de Pago Proveedor</label>
              <input v-model="form.supplier_payment_file" type="text" placeholder="URL o ruta del archivo" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Factura Proveedor</label>
              <input v-model="form.supplier_invoice_file" type="text" placeholder="URL o ruta del archivo" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500" />
            </div>
          </div>
        </div>

        <!-- Información de envío -->
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Información de Envío</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código de Envío</label>
              <input v-model="form.shipping_code" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Método de Envío</label>
              <input v-model="form.shipping_method" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo de Envío</label>
              <input v-model.number="form.shipping_cost" type="number" step="0.01" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
              <select v-model="form.status" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                <option value="En Curso">En Curso</option>
                <option value="En Tránsito">En Tránsito</option>
                <option value="Solicitud Guía Almacén">Solicitud Guía</option>
                <option value="Falta Pago Proveedor">Falta Pago</option>
                <option value="Falta Factura">Falta Factura</option>
                <option value="Por Revisar">Por Revisar</option>
                <option value="Pausado Back Orders">Pausado</option>
                <option value="Concluido">Concluido</option>
                <option value="Rechazado">Rechazado</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Detalles adicionales -->
        <div>
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Detalles Adicionales</h2>
          <div class="grid grid-cols-1 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Calidad</label>
              <input v-model="form.quality" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Justificación</label>
              <textarea v-model="form.justification" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
              <textarea v-model="form.comments" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"></textarea>
            </div>
          </div>
        </div>

        <!-- Botones -->
        <div class="flex justify-end gap-3 pt-4">
          <button type="button" @click="$router.back()" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button type="submit" :disabled="loading" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50">
            {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear') }} Compra
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
import { purchaseService } from '@/services/purchaseService.ts'
import { sparepartService } from '@/services/sparepartService.ts'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const spareparts = ref([])

const form = ref({
  name: '',
  sparepart_id: '',
  user_id: 1, // TODO: get from auth
  amount: 1,
  authorized_amount: null,
  type: 'Interna',
  shipping_code: '',
  shipping_method: '',
  shipping_cost: 0,
  status: 'En Curso',
  quality: '',
  justification: '',
  comments: '',
  
  // Proveedores
  supplier1_name: '',
  supplier1_cost: null,
  supplier2_name: '',
  supplier2_cost: null,
  supplier3_name: '',
  supplier3_cost: null,
  
  // Archivos
  quotation_file: '',
  supplier_payment_file: '',
  supplier_invoice_file: '',
  
  // Para ventas
  is_paid: null
})

const isEditing = computed(() => !!route.params.id)

const loadPurchase = async () => {
  if (!isEditing.value) return
  try {
    const purchase = await purchaseService.getPurchaseById(route.params.id)
    Object.assign(form.value, purchase)
  } catch (error) {
    console.error('Error loading purchase:', error)
    alert('Error al cargar la compra')
  }
}

const loadSpareparts = async () => {
  try {
    const response = await sparepartService.getSpareparts({ pageSize: 100 })
    spareparts.value = response.items || []
  } catch (error) {
    console.error('Error loading spareparts:', error)
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    if (isEditing.value) {
      await purchaseService.updatePurchase(route.params.id, form.value)
    } else {
      await purchaseService.createPurchase(form.value)
    }
    router.push({ name: 'Compras' })
  } catch (error) {
    console.error('Error saving purchase:', error)
    alert('Error al guardar la compra')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSpareparts()
  loadPurchase()
})
</script>
