<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Gestión de Equipos</h1>
          <p class="text-gray-600 mt-2">Administra el inventario de equipos de oficina</p>
        </div>
        <button 
          @click="openCreateModal"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <i class="fas fa-plus"></i>
          Nuevo Equipo
        </button>
      </div>

      <!-- Estadísticas rápidas -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <i class="fas fa-desktop text-blue-600"></i>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Total Equipos</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <i class="fas fa-check-circle text-green-600"></i>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Activos</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.active }}</p>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                <i class="fas fa-tools text-yellow-600"></i>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">En Mantenimiento</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.maintenance }}</p>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                <i class="fas fa-exclamation-triangle text-red-600"></i>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Fuera de Servicio</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.outOfService }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros y búsqueda -->
      <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
            <input
              type="text"
              v-model="searchQuery"
              @input="searchEquipment"
              placeholder="Modelo, número de serie..."
              class="w-full border border-gray-300 rounded-md px-3 py-2"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
            <select v-model="typeFilter" @change="applyFilters" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">Todos los tipos</option>
              <option value="IMPRESORA">Impresoras</option>
              <option value="COPIADORA">Copiadoras</option>
              <option value="MULTIFUNCIONAL">Multifuncionales</option>
              <option value="ESCANER">Escáneres</option>
              <option value="PLOTTER">Plotters</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
            <select v-model="statusFilter" @change="applyFilters" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">Todos los estados</option>
              <option value="ACTIVO">Activo</option>
              <option value="INACTIVO">Inactivo</option>
              <option value="MANTENIMIENTO">En Mantenimiento</option>
              <option value="FUERA_SERVICIO">Fuera de Servicio</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Marca</label>
            <select v-model="brandFilter" @change="applyFilters" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">Todas las marcas</option>
              <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                {{ brand.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tabla de equipos -->
      <div class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Equipo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Número de Serie</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ubicación</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="equipment in equipment" :key="equipment.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <i :class="getEquipmentIcon(equipment.equipment_type)" class="text-blue-600"></i>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ equipment.model }}</div>
                      <div class="text-sm text-gray-500">{{ equipment.brand_name }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ equipment.serial_number }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs">
                    {{ getEquipmentTypeLabel(equipment.equipment_type) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getEquipmentStatusColor(equipment.status)" 
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ getEquipmentStatusLabel(equipment.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ equipment.client_assigned || 'Sin asignar' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ equipment.location || 'Sin ubicación' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button 
                    @click="viewEquipment(equipment)"
                    class="text-blue-600 hover:text-blue-900"
                    title="Ver detalles"
                  >
                    <i class="fas fa-eye"></i>
                  </button>
                  <button 
                    @click="editEquipment(equipment)"
                    class="text-yellow-600 hover:text-yellow-900"
                    title="Editar"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    @click="scheduleMaintenanceModal(equipment)"
                    class="text-green-600 hover:text-green-900"
                    title="Programar mantenimiento"
                  >
                    <i class="fas fa-tools"></i>
                  </button>
                  <button 
                    @click="toggleEquipmentStatus(equipment)"
                    :class="equipment.status === 'ACTIVO' ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'"
                    :title="equipment.status === 'ACTIVO' ? 'Desactivar' : 'Activar'"
                  >
                    <i :class="equipment.status === 'ACTIVO' ? 'fas fa-ban' : 'fas fa-check'"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="equipment.length === 0">
                <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                  {{ isLoading ? 'Cargando equipos...' : 'No hay equipos registrados' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button 
              @click="previousPage" 
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Anterior
            </button>
            <button 
              @click="nextPage" 
              :disabled="currentPage >= totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Siguiente
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando <span class="font-medium">{{ Math.min((currentPage - 1) * itemsPerPage + 1, totalItems) }}</span> a 
                <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span> de 
                <span class="font-medium">{{ totalItems }}</span> resultados
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button 
                  @click="previousPage" 
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  <i class="fas fa-chevron-left"></i>
                </button>
                <template v-for="page in visiblePages" :key="page">
                  <button 
                    @click="goToPage(page)"
                    :class="page === currentPage ? 'bg-blue-50 border-blue-500 text-blue-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'"
                    class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                  >
                    {{ page }}
                  </button>
                </template>
                <button 
                  @click="nextPage" 
                  :disabled="currentPage >= totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  <i class="fas fa-chevron-right"></i>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de crear/editar equipo -->
      <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/4 shadow-lg rounded-md bg-white max-h-screen overflow-y-auto">
          <div class="mt-3">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ isEditing ? 'Editar Equipo' : 'Nuevo Equipo' }}
            </h3>
            
            <form @submit.prevent="saveEquipment">
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Información básica -->
                <div class="space-y-4">
                  <h4 class="font-medium text-gray-900">Información Básica</h4>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Número de Serie *</label>
                    <input
                      type="text"
                      v-model="equipmentForm.serial_number"
                      required
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Modelo *</label>
                    <input
                      type="text"
                      v-model="equipmentForm.model"
                      required
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Equipo *</label>
                    <select
                      v-model="equipmentForm.equipment_type"
                      required
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Seleccionar tipo</option>
                      <option value="IMPRESORA">Impresora</option>
                      <option value="COPIADORA">Copiadora</option>
                      <option value="MULTIFUNCIONAL">Multifuncional</option>
                      <option value="ESCANER">Escáner</option>
                      <option value="PLOTTER">Plotter</option>
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label>
                    <select
                      v-model="equipmentForm.brand_id"
                      required
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Seleccionar marca</option>
                      <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                        {{ brand.name }}
                      </option>
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
                    <select
                      v-model="equipmentForm.status"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="ACTIVO">Activo</option>
                      <option value="INACTIVO">Inactivo</option>
                      <option value="MANTENIMIENTO">En Mantenimiento</option>
                      <option value="FUERA_SERVICIO">Fuera de Servicio</option>
                    </select>
                  </div>
                </div>

                <!-- Información de ubicación y asignación -->
                <div class="space-y-4">
                  <h4 class="font-medium text-gray-900">Ubicación y Asignación</h4>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Cliente Asignado</label>
                    <input
                      type="text"
                      v-model="equipmentForm.client_assigned"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Ubicación</label>
                    <input
                      type="text"
                      v-model="equipmentForm.location"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Compra</label>
                    <input
                      type="date"
                      v-model="equipmentForm.purchase_date"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Precio de Compra</label>
                    <input
                      type="number"
                      step="0.01"
                      v-model="equipmentForm.purchase_price"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Meses de Garantía</label>
                    <input
                      type="number"
                      v-model="equipmentForm.warranty_months"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      <input
                        type="checkbox"
                        v-model="equipmentForm.is_rental"
                        class="mr-2"
                      >
                      Equipo en Renta
                    </label>
                  </div>
                  
                  <div v-if="equipmentForm.is_rental">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Precio de Renta Mensual</label>
                    <input
                      type="number"
                      step="0.01"
                      v-model="equipmentForm.rental_price"
                      class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                </div>
              </div>
              
              <div class="mt-6">
                <label class="block text-sm font-medium text-gray-700 mb-1">Especificaciones Técnicas</label>
                <textarea
                  v-model="equipmentForm.specifications"
                  rows="3"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Detalles técnicos del equipo..."
                ></textarea>
              </div>
              
              <div class="mt-6">
                <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
                <textarea
                  v-model="equipmentForm.notes"
                  rows="2"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Información adicional..."
                ></textarea>
              </div>
              
              <div class="mt-8 flex justify-end space-x-3">
                <button
                  type="button"
                  @click="closeModal"
                  class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isLoading"
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {{ isLoading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Loading spinner -->
      <div v-if="isLoading && !showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-4 rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span>Cargando...</span>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { equipmentService } from '@/services/equipmentService'

export default {
  name: 'InventarioView',
  components: {
    BaseLayout
  },
  data() {
    return {
      equipment: [],
      brands: [],
      suppliers: [],
      searchQuery: '',
      typeFilter: '',
      statusFilter: '',
      brandFilter: '',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      totalPages: 1,
      isLoading: false,
      showModal: false,
      isEditing: false,
      selectedEquipment: null,
      equipmentForm: {
        serie: '',
        model: '',
        model_toner: '',
        type: '',
        brand_id: '',
        supplier_id: '',
        location_status: 'bodega',
        invoice: '',
        cost: null,
        comments: '',
        is_active: true
      }
    }
  },
  computed: {
    stats() {
      return {
        total: this.equipment.length,
        active: this.equipment.filter(e => e.location_status === 'asignado').length,
        maintenance: this.equipment.filter(e => e.location_status === 'taller').length,
        outOfService: this.equipment.filter(e => e.location_status === 'bodega').length
      }
    },
    filteredEquipment() {
      return this.equipment.filter(e => {
        const matchSearch = !this.searchQuery || 
          e.model?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          e.serie?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          e.sku?.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchType = !this.typeFilter || e.type === this.typeFilter
        const matchStatus = !this.statusFilter || e.location_status === this.statusFilter
        const matchBrand = !this.brandFilter || e.brand_id == this.brandFilter
        
        return matchSearch && matchType && matchStatus && matchBrand
      })
    },
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.isLoading = true
        const [equipmentData, brandsData, suppliersData] = await Promise.all([
          equipmentService.getEquipment(),
          equipmentService.getBrands(),
          equipmentService.getSuppliers()
        ])
        this.equipment = equipmentData || []
        this.brands = brandsData || []
        this.suppliers = suppliersData || []
        this.totalItems = this.equipment.length
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage)
      } catch (error) {
        console.error('Error loading equipment:', error)
        alert('Error al cargar los equipos')
      } finally {
        this.isLoading = false
      }
    },

    async loadEquipment() {
      await this.loadData()
    },

    async searchEquipment() {
      this.currentPage = 1
    },

    async applyFilters() {
      this.currentPage = 1
    },

    getBrandName(brandId) {
      const brand = this.brands.find(b => b.brand_id === brandId)
      return brand ? brand.name : '-'
    },

    openCreateModal() {
      this.isEditing = false
      this.equipmentForm = {
        serie: '',
        model: '',
        model_toner: '',
        type: '',
        brand_id: '',
        supplier_id: '',
        location_status: 'bodega',
        invoice: '',
        cost: null,
        comments: '',
        is_active: true
      }
      this.showModal = true
    },

    editEquipment(equipment) {
      this.isEditing = true
      this.selectedEquipment = equipment
      this.equipmentForm = {
        serie: equipment.serie,
        model: equipment.model,
        model_toner: equipment.model_toner,
        type: equipment.type,
        brand_id: equipment.brand_id,
        supplier_id: equipment.supplier_id,
        location_status: equipment.location_status,
        invoice: equipment.invoice || '',
        cost: equipment.cost,
        comments: equipment.comments || '',
        is_active: equipment.is_active
      }
      this.showModal = true
    },

    viewEquipment(equipment) {
      alert(`Equipo: ${equipment.model}\nSerie: ${equipment.serie}\nSKU: ${equipment.sku}\nTipo: ${equipment.type}\nTóner: ${equipment.model_toner}`)
    },

    scheduleMaintenanceModal(equipment) {
      alert(`Programar mantenimiento para: ${equipment.model}`)
    },

    async saveEquipment() {
      try {
        this.isLoading = true
        
        const data = {
          brand_id: parseInt(this.equipmentForm.brand_id),
          model: this.equipmentForm.model,
          serie: this.equipmentForm.serie,
          model_toner: this.equipmentForm.model_toner,
          type: this.equipmentForm.type,
          supplier_id: parseInt(this.equipmentForm.supplier_id),
          invoice: this.equipmentForm.invoice || null,
          cost: this.equipmentForm.cost ? parseFloat(this.equipmentForm.cost) : null,
          location_status: this.equipmentForm.location_status,
          comments: this.equipmentForm.comments || null,
          is_active: this.equipmentForm.is_active
        }
        
        if (this.isEditing) {
          await equipmentService.updateEquipment(this.selectedEquipment.item_id, data)
          alert('Equipo actualizado correctamente')
        } else {
          await equipmentService.createEquipment(data)
          alert('Equipo creado correctamente')
        }
        
        this.closeModal()
        await this.loadData()
      } catch (error) {
        console.error('Error saving equipment:', error)
        alert('Error al guardar el equipo: ' + error.message)
      } finally {
        this.isLoading = false
      }
    },

    async toggleEquipmentStatus(equipment) {
      try {
        const newStatus = equipment.location_status === 'asignado' ? 'bodega' : 'asignado'
        await equipmentService.updateEquipmentStatus(equipment.item_id, newStatus)
        await this.loadData()
        alert(`Equipo movido a ${newStatus === 'bodega' ? 'Bodega' : 'Asignado'}`)
      } catch (error) {
        console.error('Error toggling equipment status:', error)
        alert('Error al cambiar el estado del equipo')
      }
    },

    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.selectedEquipment = null
    },

    // Métodos de utilidad
    getEquipmentIcon(type) {
      const icons = {
        'monocromo': 'fas fa-print',
        'color': 'fas fa-palette'
      }
      return icons[type] || 'fas fa-desktop'
    },

    getEquipmentTypeLabel(type) {
      const labels = {
        'monocromo': 'Monocromo',
        'color': 'Color'
      }
      return labels[type] || type
    },

    getEquipmentStatusLabel(status) {
      const labels = {
        'bodega': 'En Bodega',
        'asignado': 'Asignado',
        'taller': 'En Taller',
        'vendido': 'Vendido',
        'desconocido': 'Desconocido'
      }
      return labels[status] || status
    },

    getEquipmentStatusColor(status) {
      const colors = {
        'bodega': 'bg-blue-100 text-blue-800',
        'asignado': 'bg-green-100 text-green-800',
        'taller': 'bg-yellow-100 text-yellow-800',
        'vendido': 'bg-purple-100 text-purple-800',
        'desconocido': 'bg-gray-100 text-gray-800'
      }
      return colors[status] || 'bg-gray-100 text-gray-800'
    },

    // Métodos de paginación
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.loadEquipment()
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.loadEquipment()
      }
    },

    goToPage(page) {
      this.currentPage = page
      this.loadEquipment()
    }
  }
}
</script>