<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <h1 class="text-3xl font-bold text-purple-800 mb-2">Gestión de Inventario</h1>
          <p class="text-purple-600">Administra el inventario de equipos y suministros</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Equipos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Disponibles</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.available }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Renta</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.rented }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Vendidos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.sold }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4">
            <button @click="showCreateModal = true" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Agregar Equipo
            </button>
            <button @click="openBrandModal" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              Registrar Marca
            </button>
            <button @click="loadEquipment" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <select v-model="filterCategory" class="input-field w-40">
              <option value="">Todas las categorías</option>
              <option value="copiadoras">Copiadoras</option>
              <option value="impresoras">Impresoras</option>
              <option value="multifuncionales">Multifuncionales</option>
              <option value="consumibles">Consumibles</option>
            </select>
            <select v-model="filterStatus" class="input-field w-40">
              <option value="">Todos los estados</option>
              <option value="disponible">Disponible</option>
              <option value="rentado">En Renta</option>
              <option value="vendido">Vendido</option>
              <option value="mantenimiento">Mantenimiento</option>
            </select>
          </div>
        </div>

        <!-- Inventory Table -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Equipos en Inventario</h2>
          </div>
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <p class="text-gray-500">Cargando equipos...</p>
            </div>
            <div v-else-if="error" class="text-center py-8">
              <p class="text-red-500">{{ error }}</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Marca</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Modelo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serie</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredEquipment.length === 0">
                    <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                      No hay equipos registrados
                    </td>
                  </tr>
                  <tr v-for="item in filteredEquipment" :key="item.item_id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.sku }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ getBrandName(item.brand_id) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.model }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.serie }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.type }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(item.location_status)]">
                        {{ item.location_status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button @click="editEquipment(item)" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                      <button @click="deleteEquipment(item.item_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ showCreateModal ? 'Agregar Equipo' : 'Editar Equipo' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <form @submit.prevent="showCreateModal ? createEquipment() : updateEquipment()" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label>
              <select v-model="equipmentForm.brand_id" required class="input-field">
                <option :value="null">Seleccionar marca...</option>
                <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                  {{ brand.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modelo *</label>
              <input v-model="equipmentForm.model" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Serie *</label>
              <input v-model="equipmentForm.serie" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modelo de Toner *</label>
              <input v-model="equipmentForm.model_toner" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
              <select v-model="equipmentForm.type" required class="input-field">
                <option value="monocromo">Monocromo</option>
                <option value="color">Color</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor *</label>
              <select v-model="equipmentForm.supplier_id" required class="input-field">
                <option :value="null">Seleccionar proveedor...</option>
                <option v-for="supplier in suppliers" :key="supplier.supplier_id" :value="supplier.supplier_id">
                  {{ supplier.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
              <input v-model="equipmentForm.invoice" type="text" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
              <input v-model="equipmentForm.cost" type="number" step="0.01" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado de Ubicación *</label>
              <select v-model="equipmentForm.location_status" required class="input-field">
                <option value="bodega">Bodega</option>
                <option value="asignado">Asignado</option>
                <option value="vendido">Vendido</option>
                <option value="taller">Taller</option>
                <option value="desconocido">Desconocido</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
              <textarea v-model="equipmentForm.comments" rows="3" class="input-field"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
              {{ showCreateModal ? 'Crear Equipo' : 'Actualizar Equipo' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Brand Modal -->
    <div v-if="showBrandModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">Gestión de Marcas</h3>
            <button @click="closeBrandModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <!-- Lista de Marcas -->
          <div class="mb-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Marcas Registradas</h4>
            <div v-if="loadingBrands" class="text-center py-4">
              <p class="text-gray-500">Cargando marcas...</p>
            </div>
            <div v-else-if="brands.length === 0" class="text-center py-8 bg-gray-50 rounded-lg">
              <p class="text-gray-500">No hay marcas registradas</p>
            </div>
            <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div v-for="brand in brands" :key="brand.brand_id" 
                   class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                <span class="text-sm font-medium text-gray-900">{{ brand.name }}</span>
                <button @click="deleteBrand(brand.brand_id)" 
                        class="text-red-500 hover:text-red-700">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Formulario para Nueva Marca -->
          <div class="border-t pt-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Registrar Nueva Marca</h4>
            <form @submit.prevent="createBrand" class="grid grid-cols-2 gap-3">
              <input v-model="brandForm.name" 
                     type="text" 
                     required 
                     placeholder="Nombre de la marca (Ej: Canon, HP, Xerox...)" 
                     class="input-field">
              <input v-model="brandForm.prefix" 
                     type="text" 
                     required 
                     placeholder="Prefijo (Ej: CAN, HP, XER...)" 
                     class="input-field">
              <button type="submit" 
                      class="col-span-2 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 whitespace-nowrap">\n                Agregar Marca
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Agregar
                </span>
              </button>
            </form>
          </div>
        </div>

        <div class="p-6 border-t flex justify-end">
          <button @click="closeBrandModal" class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { equipmentService } from '@/services/equipmentService'

export default {
  name: 'InventarioView',
  components: {
    AppNavigation
  },
  data() {
    return {
      equipment: [],
      brands: [],
      loading: false,
      loadingBrands: false,
      error: null,
      showCreateModal: false,
      showEditModal: false,
      showBrandModal: false,
      filterCategory: '',
      filterStatus: '',
      equipmentForm: {
        brand_id: null,
        model: '',
        serie: '',
        model_toner: '',
        type: 'monocromo',
        supplier_id: null,
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: ''
      },
      brandForm: {
        name: '',
        prefix: ''
      },
      suppliers: [],
      editingEquipmentId: null
    }
  },
  computed: {
    filteredEquipment() {
      return this.equipment.filter(item => {
        const matchesCategory = !this.filterCategory || item.category === this.filterCategory
        const matchesStatus = !this.filterStatus || item.status === this.filterStatus
        return matchesCategory && matchesStatus
      })
    },
    stats() {
      return {
        total: this.equipment.length,
        available: this.equipment.filter(e => e.location_status === 'bodega').length,
        rented: this.equipment.filter(e => e.location_status === 'asignado').length,
        sold: this.equipment.filter(e => e.location_status === 'vendido').length
      }
    }
  },
  async mounted() {
    await this.loadEquipment()
    await this.loadBrands()
    await this.loadSuppliers()
  },
  methods: {
    async loadEquipment() {
      this.loading = true
      this.error = null
      try {
        this.equipment = await equipmentService.getEquipment()
      } catch (err) {
        this.error = 'Error al cargar equipos: ' + err.message
        console.error('Error loading equipment:', err)
      } finally {
        this.loading = false
      }
    },
    
    async loadSuppliers() {
      try {
        this.suppliers = await equipmentService.getSuppliers()
      } catch (err) {
        console.error('Error loading suppliers:', err)
      }
    },
    
    async createEquipment() {
      try {
        await equipmentService.createEquipment(this.equipmentForm)
        await this.loadEquipment()
        this.closeModal()
        alert('Equipo creado exitosamente')
      } catch (err) {
        alert('Error al crear equipo: ' + err.message)
      }
    },
    
    editEquipment(item) {
      console.log('Editing equipment:', item)
      console.log('Item ID:', item.item_id)
      this.editingEquipmentId = item.item_id
      this.equipmentForm = { ...item }
      this.showEditModal = true
      console.log('editingEquipmentId set to:', this.editingEquipmentId)
    },
    
    async updateEquipment() {
      console.log('Updating equipment with ID:', this.editingEquipmentId)
      console.log('Form data:', this.equipmentForm)
      try {
        await equipmentService.updateEquipment(this.editingEquipmentId, this.equipmentForm)
        await this.loadEquipment()
        this.closeModal()
        alert('Equipo actualizado exitosamente')
      } catch (err) {
        console.error('Update error:', err)
        alert('Error al actualizar equipo: ' + err.message)
      }
    },
    
    async deleteEquipment(equipmentId) {
      if (!confirm('¿Está seguro de eliminar este equipo?')) return
      
      try {
        await equipmentService.deleteEquipment(equipmentId)
        await this.loadEquipment()
        alert('Equipo eliminado exitosamente')
      } catch (err) {
        alert('Error al eliminar equipo: ' + err.message)
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingEquipmentId = null
      this.equipmentForm = {
        brand_id: null,
        model: '',
        serie: '',
        model_toner: '',
        type: 'monocromo',
        supplier_id: null,
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: ''
      }
    },
    
    getStatusClass(status) {
      const classes = {
        'bodega': 'bg-green-100 text-green-800',
        'asignado': 'bg-blue-100 text-blue-800',
        'vendido': 'bg-gray-100 text-gray-800',
        'taller': 'bg-yellow-100 text-yellow-800',
        'desconocido': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    
    getBrandName(brandId) {
      const brand = this.brands.find(b => b.brand_id === brandId)
      return brand ? brand.name : '-'
    },
    
    async createBrand() {
      try {
        await equipmentService.createBrand(this.brandForm)
        this.brandForm = { name: '', prefix: '' }
        await this.loadBrands()
        alert('Marca registrada exitosamente')
      } catch (err) {
        alert('Error al registrar marca: ' + err.message)
      }
    },
    
    async loadBrands() {
      this.loadingBrands = true
      try {
        this.brands = await equipmentService.getBrands()
      } catch (err) {
        console.error('Error loading brands:', err)
      } finally {
        this.loadingBrands = false
      }
    },
    
    async deleteBrand(brandId) {
      if (!confirm('¿Está seguro de eliminar esta marca?')) return
      
      try {
        await equipmentService.deleteBrand(brandId)
        await this.loadBrands()
        alert('Marca eliminada exitosamente')
      } catch (err) {
        alert('Error al eliminar marca: ' + err.message)
      }
    },
    
    async openBrandModal() {
      this.showBrandModal = true
      await this.loadBrands()
    },
    
    closeBrandModal() {
      this.showBrandModal = false
      this.brandForm = { name: '' }
    }
  }
}
</script>
