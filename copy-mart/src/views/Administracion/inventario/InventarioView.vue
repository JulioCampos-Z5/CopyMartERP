<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-emerald-50 p-6 rounded-lg border border-emerald-200">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-emerald-800 mb-2">Inventario</h1>
              <p class="text-emerald-600">Gestión de items físicos en almacén</p>
            </div>
            <div class="flex gap-2">
              <button @click="openBulkModal()" class="bg-emerald-100 text-emerald-700 px-4 py-2 rounded-lg hover:bg-emerald-200 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Entrada Masiva
              </button>
              <button @click="openModal()" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Nueva Entrada
              </button>
            </div>
          </div>
        </div>

        <!-- Filtros -->
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="grid grid-cols-1 md:grid-cols-6 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
              <input v-model="filters.search" type="text" placeholder="Código o nombre..." 
                     class="w-full px-3 py-2 border rounded-lg text-sm" @keyup.enter="loadInventory" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="filters.item_type" class="w-full px-3 py-2 border rounded-lg text-sm" @change="loadInventory">
                <option value="">Todos</option>
                <option value="toner">Toner</option>
                <option value="refaccion">Refacción</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Sección</label>
              <select v-model="filters.section" class="w-full px-3 py-2 border rounded-lg text-sm" @change="loadInventory">
                <option value="">Todas</option>
                <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Calidad</label>
              <select v-model="filters.quality" class="w-full px-3 py-2 border rounded-lg text-sm" @change="loadInventory">
                <option value="">Todas</option>
                <option v-for="q in qualities" :key="q.value" :value="q.value">{{ q.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Disponibilidad</label>
              <select v-model="filters.is_available" class="w-full px-3 py-2 border rounded-lg text-sm" @change="loadInventory">
                <option value="">Todos</option>
                <option :value="true">Disponible</option>
                <option :value="false">No disponible</option>
              </select>
            </div>
            <div class="flex items-end">
              <button @click="clearFilters" class="w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 text-sm">
                Limpiar
              </button>
            </div>
          </div>
        </div>

        <!-- Stats Rápidos -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white p-4 rounded-lg shadow border text-center">
            <p class="text-2xl font-bold text-emerald-600">{{ inventoryItems.length }}</p>
            <p class="text-sm text-gray-500">Items en lista</p>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border text-center">
            <p class="text-2xl font-bold text-blue-600">{{ inventoryItems.filter(i => i.is_available).length }}</p>
            <p class="text-sm text-gray-500">Disponibles</p>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border text-center">
            <p class="text-2xl font-bold text-cyan-600">{{ inventoryItems.filter(i => i.catalog_item?.item_type === 'toner').length }}</p>
            <p class="text-sm text-gray-500">Toners</p>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border text-center">
            <p class="text-2xl font-bold text-orange-600">{{ inventoryItems.filter(i => i.catalog_item?.item_type === 'refaccion').length }}</p>
            <p class="text-sm text-gray-500">Refacciones</p>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
        </div>

        <!-- Tabla de Inventario -->
        <div v-else class="bg-white rounded-lg shadow border overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Item</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sección</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estante</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Calidad</th>
                  <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Proveedor</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Costo</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in inventoryItems" :key="item.inventory_id" class="hover:bg-gray-50">
                  <td class="px-4 py-3">
                    <span class="font-mono text-sm font-medium text-emerald-700">{{ item.item_code }}</span>
                  </td>
                  <td class="px-4 py-3">
                    <div class="font-medium text-gray-900">{{ item.catalog_item?.item_name || '-' }}</div>
                    <div class="text-xs text-gray-500">
                      <span :class="item.catalog_item?.item_type === 'toner' ? 'text-cyan-600' : 'text-orange-600'">
                        {{ item.catalog_item?.item_type === 'toner' ? 'Toner' : 'Refacción' }}
                      </span>
                      <span v-if="item.catalog_item?.color" class="ml-2">• {{ colorLabels[item.catalog_item.color] }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-500">{{ sectionLabels[item.section] }}</td>
                  <td class="px-4 py-3 text-sm text-gray-500">{{ item.shelf?.name || '-' }}</td>
                  <td class="px-4 py-3">
                    <span :class="['px-2 py-1 text-xs font-medium rounded', qualityClasses[item.quality]]">
                      {{ qualityLabels[item.quality] }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      item.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    ]">
                      {{ item.is_available ? 'Disponible' : 'No disponible' }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-500">{{ item.supplier?.name || '-' }}</td>
                  <td class="px-4 py-3 text-right text-sm text-gray-900">
                    {{ item.cost ? `$${Number(item.cost).toFixed(2)}` : '-' }}
                  </td>
                  <td class="px-4 py-3 text-right">
                    <div class="flex justify-end gap-2">
                      <button @click="openModal(item)" class="text-emerald-600 hover:text-emerald-900" title="Editar">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button @click="toggleAvailability(item)" :class="item.is_available ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'" :title="item.is_available ? 'Marcar no disponible' : 'Marcar disponible'">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="inventoryItems.length === 0">
                  <td colspan="9" class="px-6 py-8 text-center text-gray-500">
                    No hay items en inventario
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Modal Crear/Editar Individual -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-semibold mb-4">{{ form.inventory_id ? 'Editar' : 'Nueva' }} Entrada de Inventario</h3>
          <form @submit.prevent="saveItem" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Item del Catálogo *</label>
              <select v-model="form.catalog_id" required class="w-full px-3 py-2 border rounded-lg">
                <option :value="null" disabled>Seleccionar item...</option>
                <option v-for="cat in catalogItems" :key="cat.catalog_id" :value="cat.catalog_id">
                  {{ cat.item_name }} ({{ cat.item_type }})
                </option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Sección *</label>
                <select v-model="form.section" required class="w-full px-3 py-2 border rounded-lg">
                  <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Estante</label>
                <select v-model="form.shelf_id" class="w-full px-3 py-2 border rounded-lg">
                  <option :value="null">Sin asignar</option>
                  <option v-for="shelf in filteredShelves" :key="shelf.shelf_id" :value="shelf.shelf_id">
                    {{ shelf.name }}
                  </option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Calidad *</label>
              <select v-model="form.quality" required class="w-full px-3 py-2 border rounded-lg">
                <option v-for="q in qualities" :key="q.value" :value="q.value">{{ q.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
              <select v-model="form.supplier_id" class="w-full px-3 py-2 border rounded-lg">
                <option :value="null">Sin proveedor</option>
                <option v-for="sup in suppliers" :key="sup.supplier_id" :value="sup.supplier_id">
                  {{ sup.name }}
                </option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
                <input v-model="form.invoice" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
                <input v-model.number="form.cost" type="number" step="0.01" min="0" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
              <textarea v-model="form.comments" rows="2" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
            <div class="flex justify-end gap-3 pt-4">
              <button type="button" @click="showModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
                Cancelar
              </button>
              <button type="submit" :disabled="saving" class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50">
                {{ saving ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal Entrada Masiva -->
      <div v-if="showBulkModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showBulkModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-semibold mb-4">Entrada Masiva de Inventario</h3>
          <form @submit.prevent="saveBulk" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Item del Catálogo *</label>
              <select v-model="bulkForm.catalog_id" required class="w-full px-3 py-2 border rounded-lg">
                <option :value="null" disabled>Seleccionar item...</option>
                <option v-for="cat in catalogItems" :key="cat.catalog_id" :value="cat.catalog_id">
                  {{ cat.item_name }} ({{ cat.item_type }})
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad *</label>
              <input v-model.number="bulkForm.quantity" type="number" min="1" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Sección *</label>
                <select v-model="bulkForm.section" required class="w-full px-3 py-2 border rounded-lg">
                  <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Calidad *</label>
                <select v-model="bulkForm.quality" required class="w-full px-3 py-2 border rounded-lg">
                  <option v-for="q in qualities" :key="q.value" :value="q.value">{{ q.label }}</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
              <select v-model="bulkForm.supplier_id" class="w-full px-3 py-2 border rounded-lg">
                <option :value="null">Sin proveedor</option>
                <option v-for="sup in suppliers" :key="sup.supplier_id" :value="sup.supplier_id">
                  {{ sup.name }}
                </option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
                <input v-model="bulkForm.invoice" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Costo (c/u)</label>
                <input v-model.number="bulkForm.cost" type="number" step="0.01" min="0" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div class="flex justify-end gap-3 pt-4">
              <button type="button" @click="showBulkModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
                Cancelar
              </button>
              <button type="submit" :disabled="saving" class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50">
                {{ saving ? 'Guardando...' : `Crear ${bulkForm.quantity} entrada(s)` }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import { inventoryService, catalogService, shelfService, type InventoryItem, type ItemCatalog, type Shelf, type SectionLocation, type QualityType } from '@/services/inventoryService'
import { supplierService } from '@/services/supplierService'

const route = useRoute()
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const showBulkModal = ref(false)

const inventoryItems = ref<InventoryItem[]>([])
const catalogItems = ref<ItemCatalog[]>([])
const shelves = ref<Shelf[]>([])
const suppliers = ref<any[]>([])

const filters = reactive({
  search: '',
  item_type: '' as '' | 'toner' | 'refaccion',
  section: '' as '' | SectionLocation,
  quality: '' as '' | QualityType,
  is_available: '' as '' | boolean
})

const form = reactive({
  inventory_id: null as number | null,
  catalog_id: null as number | null,
  section: 'seccion_1' as SectionLocation,
  shelf_id: null as number | null,
  quality: 'original' as QualityType,
  supplier_id: null as number | null,
  invoice: '',
  cost: null as number | null,
  comments: ''
})

const bulkForm = reactive({
  catalog_id: null as number | null,
  quantity: 1,
  section: 'seccion_1' as SectionLocation,
  quality: 'original' as QualityType,
  supplier_id: null as number | null,
  invoice: '',
  cost: null as number | null
})

const sections = [
  { value: 'seccion_1', label: 'Sección 1' },
  { value: 'seccion_2', label: 'Sección 2' },
  { value: 'seccion_3', label: 'Sección 3' },
  { value: 'seccion_4', label: 'Sección 4' },
  { value: 'seccion_5', label: 'Sección 5' },
  { value: 'seccion_6', label: 'Sección 6' }
]

const qualities = [
  { value: 'original', label: 'Original' },
  { value: 'generico', label: 'Genérico' },
  { value: 'reparado', label: 'Reparado' },
  { value: 'nueva', label: 'Nueva' },
  { value: 'usado', label: 'Usado' },
  { value: 'n/a', label: 'N/A' }
]

const sectionLabels: Record<string, string> = {
  seccion_1: 'Sección 1',
  seccion_2: 'Sección 2',
  seccion_3: 'Sección 3',
  seccion_4: 'Sección 4',
  seccion_5: 'Sección 5',
  seccion_6: 'Sección 6'
}

const qualityLabels: Record<string, string> = {
  original: 'Original',
  generico: 'Genérico',
  reparado: 'Reparado',
  nueva: 'Nueva',
  usado: 'Usado',
  'n/a': 'N/A'
}

const qualityClasses: Record<string, string> = {
  original: 'bg-green-100 text-green-800',
  generico: 'bg-blue-100 text-blue-800',
  reparado: 'bg-yellow-100 text-yellow-800',
  nueva: 'bg-purple-100 text-purple-800',
  usado: 'bg-gray-100 text-gray-800',
  'n/a': 'bg-gray-100 text-gray-500'
}

const colorLabels: Record<string, string> = {
  k: 'Negro',
  c: 'Cyan',
  m: 'Magenta',
  y: 'Amarillo'
}

const filteredShelves = computed(() => {
  return shelves.value.filter(s => s.section === form.section)
})

const loadInventory = async () => {
  loading.value = true
  try {
    const params: any = { is_active: true }
    if (filters.search) params.search = filters.search
    if (filters.item_type) params.item_type = filters.item_type
    if (filters.section) params.section = filters.section
    if (filters.quality) params.quality = filters.quality
    if (filters.is_available !== '') params.is_available = filters.is_available
    
    inventoryItems.value = await inventoryService.getInventoryItems(params)
  } catch (error) {
    console.error('Error cargando inventario:', error)
  } finally {
    loading.value = false
  }
}

const loadCatalog = async () => {
  try {
    catalogItems.value = await catalogService.getCatalogItems({ is_active: true })
  } catch (error) {
    console.error('Error cargando catálogo:', error)
  }
}

const loadShelves = async () => {
  try {
    shelves.value = await shelfService.getShelves()
  } catch (error) {
    console.error('Error cargando estantes:', error)
  }
}

const loadSuppliers = async () => {
  try {
    suppliers.value = await supplierService.getSuppliers()
  } catch (error) {
    console.error('Error cargando proveedores:', error)
  }
}

const clearFilters = () => {
  filters.search = ''
  filters.item_type = ''
  filters.section = ''
  filters.quality = ''
  filters.is_available = ''
  loadInventory()
}

const openModal = (item?: InventoryItem) => {
  if (item) {
    form.inventory_id = item.inventory_id
    form.catalog_id = item.catalog_id
    form.section = item.section
    form.shelf_id = item.shelf_id || null
    form.quality = item.quality
    form.supplier_id = item.supplier_id || null
    form.invoice = item.invoice || ''
    form.cost = item.cost ? Number(item.cost) : null
    form.comments = item.comments || ''
  } else {
    form.inventory_id = null
    form.catalog_id = null
    form.section = 'seccion_1'
    form.shelf_id = null
    form.quality = 'original'
    form.supplier_id = null
    form.invoice = ''
    form.cost = null
    form.comments = ''
  }
  showModal.value = true
}

const openBulkModal = () => {
  bulkForm.catalog_id = null
  bulkForm.quantity = 1
  bulkForm.section = 'seccion_1'
  bulkForm.quality = 'original'
  bulkForm.supplier_id = null
  bulkForm.invoice = ''
  bulkForm.cost = null
  showBulkModal.value = true
}

const saveItem = async () => {
  if (!form.catalog_id) return
  saving.value = true
  try {
    const data = {
      catalog_id: form.catalog_id,
      section: form.section,
      shelf_id: form.shelf_id || undefined,
      quality: form.quality,
      supplier_id: form.supplier_id || undefined,
      invoice: form.invoice || undefined,
      cost: form.cost || undefined,
      comments: form.comments || undefined
    }

    if (form.inventory_id) {
      await inventoryService.updateInventoryItem(form.inventory_id, data)
    } else {
      await inventoryService.createInventoryItem(data)
    }

    showModal.value = false
    await loadInventory()
  } catch (error: any) {
    console.error('Error guardando item:', error)
    alert(error.message || 'Error al guardar')
  } finally {
    saving.value = false
  }
}

const saveBulk = async () => {
  if (!bulkForm.catalog_id) return
  saving.value = true
  try {
    await inventoryService.createBulkInventory({
      catalog_id: bulkForm.catalog_id,
      quantity: bulkForm.quantity,
      section: bulkForm.section,
      quality: bulkForm.quality,
      supplier_id: bulkForm.supplier_id || undefined,
      invoice: bulkForm.invoice || undefined,
      cost: bulkForm.cost || undefined
    })

    showBulkModal.value = false
    await loadInventory()
  } catch (error: any) {
    console.error('Error en entrada masiva:', error)
    alert(error.message || 'Error al crear entradas')
  } finally {
    saving.value = false
  }
}

const toggleAvailability = async (item: InventoryItem) => {
  try {
    await inventoryService.updateInventoryItem(item.inventory_id, {
      is_available: !item.is_available
    })
    await loadInventory()
  } catch (error) {
    console.error('Error actualizando disponibilidad:', error)
  }
}

// Si viene con catalog_id en la URL, filtrar por ese catálogo
watch(() => route.query.catalog_id, (newVal) => {
  if (newVal) {
    // Cargar solo items de ese catálogo
    loadInventory()
  }
}, { immediate: true })

onMounted(async () => {
  await Promise.all([
    loadCatalog(),
    loadShelves(),
    loadSuppliers()
  ])
  await loadInventory()
})
</script>
