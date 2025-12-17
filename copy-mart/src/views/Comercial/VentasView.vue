<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-emerald-50 p-6 rounded-lg border border-emerald-200">
          <h1 class="text-3xl font-bold text-emerald-800 mb-2">Gestión de Ventas</h1>
          <p class="text-emerald-600">Administra las ventas de equipos</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Ventas Activas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.active }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Ventas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ formatCurrency(stats.totalAmount) }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Pendientes</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.pending }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Entregadas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.delivered }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4 items-center justify-between">
            <div class="flex gap-4">
              <button @click="loadSales" class="btn-primary">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Actualizar
              </button>
              <select v-model="filters.sale_status" @change="loadSales" class="input-field w-40">
                <option value="">Todos</option>
                <option value="pendiente">Pendiente</option>
                <option value="confirmada">Confirmada</option>
                <option value="entregada">Entregada</option>
                <option value="cancelada">Cancelada</option>
              </select>
            </div>
            <button @click="showCreateForm = !showCreateForm" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nueva Venta
            </button>
          </div>
        </div>

        <!-- Create Form -->
        <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold text-gray-900">Nueva Venta</h2>
            <button @click="showCreateForm = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <form @submit.prevent="createSale" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
              <select v-model="newSale.client_id" required class="input-field">
                <option value="">Seleccionar cliente...</option>
                <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                  {{ client.name }} - {{ client.comercial_name || 'Sin nombre comercial' }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Equipo *</label>
              <select v-model="newSale.item_id" required class="input-field">
                <option value="">Seleccionar equipo...</option>
                <option v-for="item in equipment" :key="item.item_id" :value="item.item_id">
                  {{ item.sku }} - {{ item.model }} (Serie: {{ item.serie }})
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Precio de Venta</label>
              <input v-model="newSale.sale_price" type="number" step="0.01" required class="input-field" placeholder="0.00">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="newSale.sale_status" class="input-field">
                <option value="pendiente">Pendiente</option>
                <option value="confirmada">Confirmada</option>
                <option value="entregada">Entregada</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="flex items-center">
                <input v-model="newSale.is_foreign" type="checkbox" class="mr-2">
                <span class="text-sm text-gray-700">Servicio Foráneo</span>
              </label>
            </div>
            <div class="md:col-span-2 flex gap-2 justify-end">
              <button type="button" @click="showCreateForm = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                Cancelar
              </button>
              <button type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">
                Crear Venta
              </button>
            </div>
          </form>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Cargando ventas...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="bg-red-50 p-6 rounded-lg border border-red-200">
          <p class="text-red-600">{{ error }}</p>
          <button @click="loadSales" class="mt-2 text-red-700 underline">Reintentar</button>
        </div>

        <!-- Table -->
        <div v-else class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Listado de Ventas ({{ filteredSales.length }})</h2>
          </div>
          <div class="p-6">
            <div v-if="filteredSales.length === 0" class="text-center py-8 text-gray-500">
              No hay ventas registradas
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Factura</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Equipo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Precio</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="sale in filteredSales" :key="sale.sale_id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-emerald-600">{{ sale.invoice_number || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ sale.client?.name || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ sale.equipment?.model || '-' }}
                      <span class="text-gray-500 text-xs block">{{ sale.equipment?.sku || '' }}</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(sale.sale_status)]">
                        {{ getStatusLabel(sale.sale_status) }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ formatCurrency(sale.sale_price) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <button @click="viewSale(sale)" class="text-blue-600 hover:text-blue-900 mr-3">Ver</button>
                      <button v-if="sale.sale_status === 'pendiente'" @click="updateStatus(sale.sale_id, 'confirmada')" class="text-green-600 hover:text-green-900 mr-3">Confirmar</button>
                      <button v-if="sale.sale_status === 'confirmada'" @click="updateStatus(sale.sale_id, 'entregada')" class="text-blue-600 hover:text-blue-900 mr-3">Entregar</button>
                      <button v-if="sale.sale_status !== 'entregada'" @click="cancelSale(sale.sale_id)" class="text-red-600 hover:text-red-900">Cancelar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { saleService } from '@/services/saleService'
import { clientService } from '@/services/clientService'
import { equipmentService } from '@/services/equipmentService'

export default {
  name: 'VentasView',
  components: {
    BaseLayout
  },
  data() {
    return {
      sales: [],
      clients: [],
      equipment: [],
      loading: false,
      error: null,
      showCreateForm: false,
      newSale: {
        client_id: '',
        item_id: '',
        sale_price: '',
        sale_status: 'pendiente',
        is_foreign: false
      },
      stats: {
        active: 0,
        totalAmount: 0,
        pending: 0,
        delivered: 0
      },
      filters: {
        sale_status: ''
      }
    }
  },
  computed: {
    filteredSales() {
      return this.sales.filter(sale => {
        if (this.filters.sale_status && sale.sale_status !== this.filters.sale_status) return false
        return true
      })
    }
  },
  async mounted() {
    await this.loadSales()
    await this.loadClients()
    await this.loadEquipment()
  },
  methods: {
    async loadSales() {
      this.loading = true
      this.error = null
      try {
        console.log('📊 loadSales - Iniciando carga de ventas...')
        this.sales = await saleService.getSales({ is_active: true })
        console.log('📊 loadSales - Ventas cargadas:', this.sales)
        this.calculateStats()
      } catch (err) {
        this.error = err.message
        console.error('❌ Error loading sales:', err)
      } finally {
        this.loading = false
      }
    },

    async loadClients() {
      try {
        this.clients = await clientService.getClients()
      } catch (err) {
        console.error('Error loading clients:', err)
      }
    },

    async loadEquipment() {
      try {
        console.log('📦 loadEquipment - Iniciando carga de equipos...')
        const allEquipment = await equipmentService.getEquipment()
        console.log('📦 loadEquipment - Todos los equipos:', allEquipment)
        // Filtrar solo equipos en bodega (disponibles para venta)
        this.equipment = allEquipment.filter(e => e.location_status === 'bodega')
        console.log('📦 loadEquipment - Equipos en bodega:', this.equipment)
      } catch (err) {
        console.error('❌ Error loading equipment:', err)
      }
    },

    async createSale() {
      try {
        const saleData = {
          client_id: parseInt(this.newSale.client_id),
          item_id: parseInt(this.newSale.item_id),
          sale_price: parseFloat(this.newSale.sale_price),
          sale_status: this.newSale.sale_status,
          is_foreign: this.newSale.is_foreign
        }
        await saleService.createSale(saleData)
        this.showCreateForm = false
        this.resetForm()
        await this.loadSales()
        alert('Venta creada exitosamente')
      } catch (err) {
        alert('Error al crear venta: ' + err.message)
      }
    },

    resetForm() {
      this.newSale = {
        client_id: '',
        item_id: '',
        sale_price: '',
        sale_status: 'pendiente',
        is_foreign: false
      }
    },

    calculateStats() {
      this.stats.active = this.sales.length
      this.stats.totalAmount = this.sales.reduce((sum, s) => sum + parseFloat(s.sale_price || 0), 0)
      this.stats.pending = this.sales.filter(s => s.sale_status === 'pendiente').length
      this.stats.delivered = this.sales.filter(s => s.sale_status === 'entregada').length
    },

    getStatusClass(status) {
      const classes = {
        'pendiente': 'bg-yellow-100 text-yellow-800',
        'confirmada': 'bg-blue-100 text-blue-800',
        'entregada': 'bg-green-100 text-green-800',
        'cancelada': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },

    getStatusLabel(status) {
      const labels = {
        'pendiente': 'Pendiente',
        'confirmada': 'Confirmada',
        'entregada': 'Entregada',
        'cancelada': 'Cancelada'
      }
      return labels[status] || status
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
      }).format(amount)
    },

    viewSale(sale) {
      alert(`Venta: ${sale.invoice_number}\nCliente: ${sale.client?.name}\nEquipo: ${sale.equipment?.model}\nPrecio: ${this.formatCurrency(sale.sale_price)}`)
    },

    async updateStatus(saleId, newStatus) {
      try {
        await saleService.updateSaleStatus(saleId, newStatus)
        await this.loadSales()
      } catch (err) {
        alert('Error al actualizar estado: ' + err.message)
      }
    },

    async cancelSale(saleId) {
      if (!confirm('¿Está seguro de cancelar esta venta?')) return
      try {
        await saleService.deleteSale(saleId)
        await this.loadSales()
      } catch (err) {
        alert('Error al cancelar venta: ' + err.message)
      }
    }
  }
}
</script>