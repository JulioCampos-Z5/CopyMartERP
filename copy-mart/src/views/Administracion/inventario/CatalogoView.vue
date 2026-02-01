<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-indigo-50 p-6 rounded-lg border border-indigo-200">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-indigo-800 mb-2">Catálogo de Items</h1>
              <p class="text-indigo-600">Gestiona el catálogo de toners y refacciones</p>
            </div>
            <button @click="openModal()" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Item
            </button>
          </div>
        </div>

        <!-- Filtros -->
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
              <input v-model="filters.search" type="text" placeholder="Nombre del item..." 
                     class="w-full px-3 py-2 border rounded-lg focus:ring-indigo-500 focus:border-indigo-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="filters.item_type" class="w-full px-3 py-2 border rounded-lg">
                <option value="">Todos</option>
                <option value="toner">Toner</option>
                <option value="refaccion">Refacción</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Marca</label>
              <select v-model="filters.brand_id" class="w-full px-3 py-2 border rounded-lg">
                <option value="">Todas</option>
                <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                  {{ brand.name }}
                </option>
              </select>
            </div>
            <div class="flex items-end">
              <button @click="loadCatalog" class="w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200">
                Filtrar
              </button>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-500">Total Items</p>
                <p class="text-xl font-bold text-gray-900">{{ catalogItems.length }}</p>
              </div>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-cyan-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-500">Toners</p>
                <p class="text-xl font-bold text-gray-900">{{ catalogItems.filter(i => i.item_type === 'toner').length }}</p>
              </div>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-500">Refacciones</p>
                <p class="text-xl font-bold text-gray-900">{{ catalogItems.filter(i => i.item_type === 'refaccion').length }}</p>
              </div>
            </div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-500">Stock Bajo</p>
                <p class="text-xl font-bold text-red-600">{{ catalogItems.filter(i => i.available_items < i.stock_min).length }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Tabla de Catálogo -->
        <div v-else class="bg-white rounded-lg shadow border overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Item</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Marca</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Disponible</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Stock Mín/Máx</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in catalogItems" :key="item.catalog_id" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <div class="font-medium text-gray-900">{{ item.item_name }}</div>
                  <div v-if="item.description" class="text-sm text-gray-500">{{ item.description }}</div>
                </td>
                <td class="px-6 py-4">
                  <span :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    item.item_type === 'toner' ? 'bg-cyan-100 text-cyan-800' : 'bg-orange-100 text-orange-800'
                  ]">
                    {{ item.item_type === 'toner' ? 'Toner' : 'Refacción' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ item.brand?.name || '-' }}</td>
                <td class="px-6 py-4">
                  <span v-if="item.color" :class="[
                    'px-2 py-1 text-xs font-medium rounded',
                    colorClasses[item.color]
                  ]">
                    {{ colorLabels[item.color] }}
                  </span>
                  <span v-else class="text-gray-400">-</span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span :class="[
                    'font-medium',
                    item.available_items < item.stock_min ? 'text-red-600' : 'text-green-600'
                  ]">
                    {{ item.available_items }} / {{ item.total_items }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center text-sm text-gray-500">
                  {{ item.stock_min }} / {{ item.stock_max }}
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex justify-end gap-2">
                    <button @click="openModal(item)" class="text-indigo-600 hover:text-indigo-900">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <router-link :to="`/administracion/inventario?catalog_id=${item.catalog_id}`" class="text-green-600 hover:text-green-900">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </router-link>
                  </div>
                </td>
              </tr>
              <tr v-if="catalogItems.length === 0">
                <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                  No hay items en el catálogo
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Modal Crear/Editar -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-semibold mb-4">{{ form.catalog_id ? 'Editar' : 'Nuevo' }} Item del Catálogo</h3>
          <form @submit.prevent="saveItem" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Item *</label>
              <input v-model="form.item_name" type="text" required placeholder="Ej: TK-410, CF283A, Fusor HP 1020"
                     class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
              <select v-model="form.item_type" required class="w-full px-3 py-2 border rounded-lg">
                <option value="toner">Toner</option>
                <option value="refaccion">Refacción</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Marca</label>
              <select v-model="form.brand_id" class="w-full px-3 py-2 border rounded-lg">
                <option :value="null">Sin marca</option>
                <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                  {{ brand.name }}
                </option>
              </select>
            </div>
            <div v-if="form.item_type === 'toner'">
              <label class="block text-sm font-medium text-gray-700 mb-1">Color</label>
              <select v-model="form.color" class="w-full px-3 py-2 border rounded-lg">
                <option :value="null">N/A</option>
                <option value="k">Negro (K)</option>
                <option value="c">Cyan (C)</option>
                <option value="m">Magenta (M)</option>
                <option value="y">Amarillo (Y)</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea v-model="form.description" rows="2" class="w-full px-3 py-2 border rounded-lg" 
                        placeholder="Descripción opcional..."></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Uso / Compatibilidad</label>
              <textarea v-model="form.usage" rows="2" class="w-full px-3 py-2 border rounded-lg" 
                        placeholder="Ej: Kyocera KM-1620, KM-2020..."></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Stock Mínimo</label>
                <input v-model.number="form.stock_min" type="number" min="0" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Stock Máximo</label>
                <input v-model.number="form.stock_max" type="number" min="0" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div class="flex justify-end gap-3 pt-4">
              <button type="button" @click="showModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
                Cancelar
              </button>
              <button type="submit" :disabled="saving" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50">
                {{ saving ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import { catalogService, type ItemCatalog, type ItemCatalogCreate } from '@/services/inventoryService'
import { brandService } from '@/services/brandService'

const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const catalogItems = ref<ItemCatalog[]>([])
const brands = ref<any[]>([])

const filters = reactive({
  search: '',
  item_type: '' as '' | 'toner' | 'refaccion',
  brand_id: '' as '' | number
})

const form = reactive({
  catalog_id: null as number | null,
  item_name: '',
  item_type: 'toner' as 'toner' | 'refaccion',
  brand_id: null as number | null,
  color: null as 'k' | 'c' | 'm' | 'y' | null,
  description: '',
  usage: '',
  stock_min: 0,
  stock_max: 0
})

const colorLabels: Record<string, string> = {
  k: 'Negro',
  c: 'Cyan',
  m: 'Magenta',
  y: 'Amarillo'
}

const colorClasses: Record<string, string> = {
  k: 'bg-gray-800 text-white',
  c: 'bg-cyan-500 text-white',
  m: 'bg-pink-500 text-white',
  y: 'bg-yellow-400 text-gray-900'
}

const loadCatalog = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (filters.search) params.search = filters.search
    if (filters.item_type) params.item_type = filters.item_type
    if (filters.brand_id) params.brand_id = Number(filters.brand_id)
    
    catalogItems.value = await catalogService.getCatalogItems(params)
  } catch (error) {
    console.error('Error cargando catálogo:', error)
  } finally {
    loading.value = false
  }
}

const loadBrands = async () => {
  try {
    brands.value = await brandService.getBrands()
  } catch (error) {
    console.error('Error cargando marcas:', error)
  }
}

const openModal = (item?: ItemCatalog) => {
  if (item) {
    form.catalog_id = item.catalog_id
    form.item_name = item.item_name
    form.item_type = item.item_type
    form.brand_id = item.brand_id || null
    form.color = item.color || null
    form.description = item.description || ''
    form.usage = item.usage || ''
    form.stock_min = item.stock_min
    form.stock_max = item.stock_max
  } else {
    form.catalog_id = null
    form.item_name = ''
    form.item_type = 'toner'
    form.brand_id = null
    form.color = null
    form.description = ''
    form.usage = ''
    form.stock_min = 0
    form.stock_max = 0
  }
  showModal.value = true
}

const saveItem = async () => {
  saving.value = true
  try {
    const data: ItemCatalogCreate = {
      item_name: form.item_name,
      item_type: form.item_type,
      brand_id: form.brand_id || undefined,
      color: form.item_type === 'toner' ? form.color || undefined : undefined,
      description: form.description || undefined,
      usage: form.usage || undefined,
      stock_min: form.stock_min,
      stock_max: form.stock_max
    }

    if (form.catalog_id) {
      await catalogService.updateCatalogItem(form.catalog_id, data)
      // Actualizar stock levels
      await catalogService.updateStockLevels(form.catalog_id, {
        stock_min: form.stock_min,
        stock_max: form.stock_max
      })
    } else {
      await catalogService.createCatalogItem(data)
    }

    showModal.value = false
    await loadCatalog()
  } catch (error: any) {
    console.error('Error guardando item:', error)
    alert(error.message || 'Error al guardar el item')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadCatalog()
  loadBrands()
})
</script>
