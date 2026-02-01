<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Volver a Inventario
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Detalle del Equipo</h1>
        <p class="text-gray-600 mt-2">Información completa del equipo</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando información...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {{ error }}
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Actions Bar -->
        <div class="bg-white p-4 rounded-lg shadow border flex justify-end gap-3">
          <button @click="editEquipment" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Editar
          </button>
        </div>

        <!-- Tabs Navigation -->
        <div class="bg-white rounded-lg shadow border">
          <div class="border-b border-gray-200">
            <nav class="flex -mb-px">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id 
                    ? 'border-blue-500 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm'
                ]"
              >
                {{ tab.label }}
              </button>
            </nav>
          </div>
        </div>

        <!-- Tab: Información General -->
        <div v-if="activeTab === 'info'" class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-6">Información General</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <p class="text-sm text-gray-500 mb-1">SKU</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.sku || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Marca</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.brand?.name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Modelo</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.model || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Número de Serie</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.serie || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Modelo de Toner</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.model_toner || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Tipo</p>
              <p class="text-base font-medium text-gray-900">
                <span :class="equipment.type === 'color' ? 'text-purple-600' : 'text-gray-900'">
                  {{ equipment.type === 'color' ? 'Color' : 'Monocromo' }}
                </span>
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Estado</p>
              <p class="text-base font-medium">
                <span :class="getStatusClass(equipment.location_status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ equipment.location_status || '-' }}
                </span>
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Proveedor</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.supplier?.name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Factura</p>
              <p class="text-base font-medium text-gray-900">{{ equipment.invoice || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Costo</p>
              <p class="text-base font-medium text-gray-900">
                {{ equipment.cost ? formatCurrency(equipment.cost) : '-' }}
              </p>
            </div>
          </div>

          <!-- Comentarios dentro del tab info -->
          <div v-if="equipment.comments" class="mt-6 pt-6 border-t">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Comentarios</h3>
            <p class="text-gray-700">{{ equipment.comments }}</p>
          </div>
        </div>

        <!-- Tab: Contadores de Impresión -->
        <div v-if="activeTab === 'print'" class="space-y-6">
          <div class="bg-white rounded-lg shadow border p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Contadores de Impresión</h2>
            </div>

            <div v-if="loadingPrint" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>

            <div v-else-if="printCounters.length > 0" class="space-y-4">
              <div v-for="counter in printCounters" :key="counter.counter_id" class="border rounded-lg p-4 hover:bg-gray-50">
                <div class="flex justify-between items-start">
                  <div class="flex-1 grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p class="text-xs text-gray-500">Período</p>
                      <p class="text-sm font-medium">{{ counter.period_month }}/{{ counter.period_year }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">B/N Impresas</p>
                      <p class="text-sm font-medium">{{ counter.bn_printed }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Color Impresas</p>
                      <p class="text-sm font-medium">{{ counter.color_printed }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Exceso Total</p>
                      <p class="text-sm font-medium">{{ formatCurrency(counter.total_excess_amount) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Contador B/N</p>
                      <p class="text-sm font-medium">{{ counter.bn_current }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Contador Color</p>
                      <p class="text-sm font-medium">{{ counter.color_current }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Fecha Lectura</p>
                      <p class="text-sm font-medium">{{ formatDate(counter.reading_date) }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Facturado</p>
                      <span :class="counter.is_billed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" class="inline-block px-2 py-1 text-xs font-medium rounded-full">
                        {{ counter.is_billed ? 'Sí' : 'No' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-if="counter.notes" class="mt-2 pt-2 border-t">
                  <p class="text-xs text-gray-500">Notas:</p>
                  <p class="text-sm text-gray-700">{{ counter.notes }}</p>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8 text-gray-500">
              No hay contadores de impresión registrados para este equipo
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppNavigation from '@/components/AppNavigation.vue'
import { equipmentService } from '@/services/equipmentService'
import { rentService } from '@/services/rentService'
import printService, { type PrintCounter } from '@/services/printService'
import type { Rent } from '@/types'

const route = useRoute()
const router = useRouter()

const equipment = ref<any>({})
const loading = ref(false)
const error = ref<string | null>(null)
const activeTab = ref('info')

const tabs = [
  { id: 'info', label: 'Información General' },
  { id: 'print', label: 'Contadores de Impresión' }
]

// Print counters
const printCounters = ref<PrintCounter[]>([])
const loadingPrint = ref(false)
const equipmentRents = ref<Rent[]>([])

const loadEquipment = async () => {
  loading.value = true
  error.value = null
  try {
    equipment.value = await equipmentService.getEquipmentById(Number(route.params.id))
  } catch (err: any) {
    error.value = 'Error al cargar el equipo: ' + err.message
  } finally {
    loading.value = false
  }
}

const loadPrintCounters = async () => {
  loadingPrint.value = true
  try {
    const equipmentId = Number(route.params.id)
    
    // Buscar rentas que tengan este equipo (item_id)
    const rentsResponse = await rentService.getRents({ pageSize: 100 })
    equipmentRents.value = (rentsResponse.items || []).filter(
      (rent: Rent) => rent.item_id === equipmentId
    )
    
    // Si hay rentas, cargar los contadores de todas ellas
    if (equipmentRents.value.length > 0) {
      const allCounters: PrintCounter[] = []
      
      for (const rent of equipmentRents.value) {
        try {
          const counters = await printService.getAll({ rent_id: rent.rent_id })
          allCounters.push(...counters)
        } catch (err) {
          console.warn(`No se pudieron cargar contadores para renta ${rent.rent_id}`)
        }
      }
      
      // Ordenar por fecha de lectura descendente
      printCounters.value = allCounters.sort((a, b) => 
        new Date(b.reading_date).getTime() - new Date(a.reading_date).getTime()
      )
    } else {
      printCounters.value = []
    }
  } catch (err) {
    console.error('Error loading print counters:', err)
    printCounters.value = []
  } finally {
    loadingPrint.value = false
  }
}

const editEquipment = () => {
  router.push(`/administracion/equipos/editar/${route.params.id}`)
}

const goBack = () => {
  router.push('/inventario')
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(value)
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('es-MX')
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'bodega': 'bg-green-100 text-green-800',
    'asignado': 'bg-blue-100 text-blue-800',
    'vendido': 'bg-gray-100 text-gray-800',
    'taller': 'bg-yellow-100 text-yellow-800',
    'desconocido': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

onMounted(async () => {
  await loadEquipment()
  await loadPrintCounters()
})
</script>
