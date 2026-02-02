<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
        <h1 class="text-3xl font-bold text-purple-800 mb-2">Control de Almacén</h1>
        <p class="text-purple-600">Gestiona el inventario, movimientos de almacén, marcas y proveedores</p>
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
                  ? 'border-purple-500 text-purple-600' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm'
              ]"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab: Inventario -->
      <div v-if="activeTab === 'inventory'">
      <!-- Loading -->
      <div v-if="loadingInventory" class="flex justify-center py-8 bg-white rounded-lg shadow border">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
      </div>

      <template v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Total Refacciones</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalProducts }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Stock Bajo</h3>
              <p class="text-2xl font-semibold text-red-600">{{ stats.lowStock }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Compras Completadas</h3>
              <p class="text-2xl font-semibold text-green-600">{{ stats.entriesCompleted }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H3" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">En Tránsito</h3>
              <p class="text-2xl font-semibold text-blue-600">{{ stats.inTransit }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white p-6 rounded-lg shadow border">
        <div class="flex flex-wrap gap-4">
          <button class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
            </svg>
            Registrar Entrada
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H3" />
            </svg>
            Registrar Salida
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Inventario Físico
          </button>
          <button class="btn-outline">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Reporte de Stock
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Productos con Stock Bajo -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Stock Bajo</h2>
          </div>
          <div class="p-6">
            <div v-if="lowStockItems.length > 0" class="space-y-4 max-h-80 overflow-y-auto">
              <div v-for="item in lowStockItems" :key="item.sparepart_id" 
                   :class="[
                     'flex items-center justify-between p-3 rounded-lg border',
                     item.stock === 0 ? 'bg-red-50 border-red-200' : 'bg-yellow-50 border-yellow-200'
                   ]">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">{{ item.name }}</h4>
                  <p class="text-xs text-gray-500">{{ item.brand || 'Sin marca' }}</p>
                </div>
                <div class="text-right">
                  <p :class="[
                    'text-sm font-medium',
                    item.stock === 0 ? 'text-red-600' : 'text-yellow-600'
                  ]">{{ item.stock || 0 }} pzs</p>
                  <p class="text-xs text-gray-500">Min: {{ item.min_stock || 0 }} pzs</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-12 h-12 mx-auto text-green-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p>No hay productos con stock bajo</p>
            </div>
          </div>
        </div>

        <!-- Compras Recientes (como movimientos) -->
        <div class="lg:col-span-2 bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Compras Recientes</h2>
          </div>
          <div class="p-6">
            <div v-if="recentPurchases.length > 0" class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="purchase in recentPurchases.slice(0, 10)" :key="purchase.purchase_id">
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ purchase.name }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="getStatusClass(purchase.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ purchase.status }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ purchase.amount }} pzs</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ purchase.type }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(purchase.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              No hay compras recientes
            </div>
          </div>
        </div>
      </div>
      </template>
      </div>

      <!-- Tab: Marcas -->
      <div v-if="activeTab === 'brands'" class="space-y-6">
        <div class="bg-white rounded-lg shadow border p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-gray-900">Gestión de Marcas</h2>
            <button @click="openBrandModal()" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nueva Marca
            </button>
          </div>

          <div v-if="loadingBrands" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>

          <div v-else-if="brands.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="brand in brands" :key="brand.brand_id" class="border rounded-lg p-4 hover:bg-gray-50 flex justify-between items-center">
              <div>
                <h4 class="font-semibold text-gray-900">{{ brand.name }}</h4>
              </div>
              <button @click="deleteBrand(brand.brand_id)" class="text-red-600 hover:text-red-800">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            No hay marcas registradas
          </div>
        </div>
      </div>

      <!-- Tab: Proveedores -->
      <div v-if="activeTab === 'suppliers'" class="space-y-6">
        <div class="bg-white rounded-lg shadow border p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-gray-900">Gestión de Proveedores</h2>
            <button @click="openSupplierModal()" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nuevo Proveedor
            </button>
          </div>

          <div v-if="loadingSuppliers" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>

          <div v-else-if="suppliers.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="supplier in suppliers" :key="supplier.supplier_id" class="border rounded-lg p-4 hover:bg-gray-50">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-semibold text-gray-900">{{ supplier.name }}</h4>
                </div>
                <button @click="deleteSupplier(supplier.supplier_id)" class="text-red-600 hover:text-red-800">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            No hay proveedores registrados
          </div>
        </div>
      </div>

      <!-- Modal Marca -->
      <div v-if="showBrandModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showBrandModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 class="text-xl font-semibold mb-4">Nueva Marca</h3>
          <form @submit.prevent="saveBrand" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
              <input v-model="brandForm.name" type="text" required class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" placeholder="Ej: Canon, HP, Xerox..." />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Prefijo *</label>
              <input v-model="brandForm.prefix" type="text" required maxlength="10" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" placeholder="Ej: CAN, HP, XRX..." />
              <p class="text-xs text-gray-500 mt-1">Código corto para identificar la marca (máx. 10 caracteres)</p>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showBrandModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
              <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal Proveedor -->
      <div v-if="showSupplierModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showSupplierModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 class="text-xl font-semibold mb-4">Nuevo Proveedor</h3>
          <form @submit.prevent="saveSupplier" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
              <input v-model="supplierForm.name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showSupplierModal = false" class="px-4 py-2 border rounded-lg">Cancelar</button>
              <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

    </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import { brandService } from '@/services/brandService'
import { supplierService } from '@/services/supplierService'
import { sparepartService } from '@/services/sparepartService'
import { purchaseService } from '@/services/purchaseService'
import type { Brand, Supplier, Sparepart, Purchase } from '@/types'

const activeTab = ref('inventory')
const tabs = [
  { id: 'inventory', label: 'Inventario' },
  { id: 'brands', label: 'Marcas' },
  { id: 'suppliers', label: 'Proveedores' }
]

// Inventory data
const spareparts = ref<Sparepart[]>([])
const lowStockItems = ref<Sparepart[]>([])
const recentPurchases = ref<Purchase[]>([])
const loadingInventory = ref(false)

// Stats calculadas
const stats = computed(() => ({
  totalProducts: spareparts.value.length,
  lowStock: lowStockItems.value.length,
  entriesCompleted: recentPurchases.value.filter(p => p.status === 'Concluido').length,
  inTransit: recentPurchases.value.filter(p => p.status === 'En Tránsito').length
}))

const loadInventoryData = async () => {
  loadingInventory.value = true
  try {
    // Cargar refacciones (todas)
    const sparepartsRes = await sparepartService.getSpareparts({ pageSize: 100 })
    spareparts.value = sparepartsRes.items || []
    
    // Filtrar stock bajo (items con stock <= min_stock)
    lowStockItems.value = spareparts.value.filter(sp => 
      sp.stock !== undefined && sp.min_stock !== undefined && sp.stock <= sp.min_stock
    )
    
    // Cargar compras recientes como "movimientos"
    const purchasesRes = await purchaseService.getPurchases({ pageSize: 20 })
    recentPurchases.value = purchasesRes.items || []
  } catch (error) {
    console.error('Error loading inventory data:', error)
  } finally {
    loadingInventory.value = false
  }
}

// Brands
const brands = ref<Brand[]>([])
const loadingBrands = ref(false)
const showBrandModal = ref(false)
const brandForm = ref({ name: '', prefix: '' })

const loadBrands = async () => {
  loadingBrands.value = true
  try {
    brands.value = await brandService.getBrands()
  } catch (error) {
    console.error('Error loading brands:', error)
  } finally {
    loadingBrands.value = false
  }
}

const openBrandModal = () => {
  brandForm.value = { name: '', prefix: '' }
  showBrandModal.value = true
}

const saveBrand = async () => {
  try {
    await brandService.createBrand(brandForm.value)
    showBrandModal.value = false
    await loadBrands()
  } catch (error: any) {
    console.error('Error saving brand:', error)
    alert(`Error al guardar marca: ${error.message || error}`)
  }
}

const deleteBrand = async (brandId: number) => {
  if (!confirm('¿Estás seguro de eliminar esta marca?')) return
  try {
    await brandService.deleteBrand(brandId)
    await loadBrands()
  } catch (error: any) {
    console.error('Error deleting brand:', error)
    alert(`Error al eliminar marca: ${error.message || error}`)
  }
}

// Suppliers
const suppliers = ref<Supplier[]>([])
const loadingSuppliers = ref(false)
const showSupplierModal = ref(false)
const supplierForm = ref({ name: '' })

const loadSuppliers = async () => {
  loadingSuppliers.value = true
  try {
    suppliers.value = await supplierService.getSuppliers()
  } catch (error) {
    console.error('Error loading suppliers:', error)
  } finally {
    loadingSuppliers.value = false
  }
}

const openSupplierModal = () => {
  supplierForm.value = { name: '' }
  showSupplierModal.value = true
}

const saveSupplier = async () => {
  try {
    await supplierService.createSupplier(supplierForm.value)
    showSupplierModal.value = false
    await loadSuppliers()
  } catch (error: any) {
    console.error('Error saving supplier:', error)
    alert(`Error al guardar proveedor: ${error.message || error}`)
  }
}

const deleteSupplier = async (supplierId: number) => {
  if (!confirm('¿Estás seguro de eliminar este proveedor?')) return
  try {
    await supplierService.deleteSupplier(supplierId)
    await loadSuppliers()
  } catch (error: any) {
    console.error('Error deleting supplier:', error)
    alert(`Error al eliminar proveedor: ${error.message || error}`)
  }
}

// Helper functions
const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'En Curso': 'bg-yellow-100 text-yellow-800',
    'En Tránsito': 'bg-blue-100 text-blue-800',
    'Concluido': 'bg-green-100 text-green-800',
    'Rechazado': 'bg-red-100 text-red-800',
    'Pausado Back Orders': 'bg-orange-100 text-orange-800',
    'Falta Pago Proveedor': 'bg-red-100 text-red-800',
    'Falta Factura': 'bg-pink-100 text-pink-800',
    'Por Revisar': 'bg-purple-100 text-purple-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

onMounted(() => {
  loadBrands()
  loadSuppliers()
  loadInventoryData()
})
</script>