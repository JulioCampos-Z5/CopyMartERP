<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <h1 class="text-3xl font-bold text-purple-800 mb-2">Gestión de Producción</h1>
          <p class="text-purple-600">Control de órdenes de producción y fabricación</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Producción</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.inProduction }}</p>
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
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Completadas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.completed }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Urgentes</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.urgent }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4 items-center justify-between">
            <div class="flex gap-4">
              <button @click="loadProduction" class="btn-primary">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Actualizar
              </button>
              <select v-model="filters.status" @change="loadProduction" class="input-field w-40">
                <option value="">Todos</option>
                <option value="pendiente">Pendiente</option>
                <option value="en_proceso">En Proceso</option>
                <option value="completada">Completada</option>
                <option value="cancelada">Cancelada</option>
              </select>
            </div>
            <button @click="showCreateForm = !showCreateForm" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nueva Orden
            </button>
          </div>
        </div>

        <!-- Create Form -->
        <div v-if="showCreateForm" class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold text-gray-900">Nueva Orden de Producción</h2>
            <button @click="showCreateForm = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <form @submit.prevent="createOrder" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Orden</label>
              <input v-model="newOrder.order_number" type="text" required class="input-field" placeholder="PROD-001">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cliente</label>
              <input v-model="newOrder.client_name" type="text" required class="input-field" placeholder="Nombre del cliente">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Producto/Servicio</label>
              <input v-model="newOrder.product" type="text" required class="input-field" placeholder="Descripción del producto">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad</label>
              <input v-model="newOrder.quantity" type="number" min="1" required class="input-field" placeholder="1">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de Entrega</label>
              <input v-model="newOrder.delivery_date" type="date" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Prioridad</label>
              <select v-model="newOrder.priority" class="input-field">
                <option value="normal">Normal</option>
                <option value="alta">Alta</option>
                <option value="urgente">Urgente</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
              <textarea v-model="newOrder.notes" rows="3" class="input-field" placeholder="Especificaciones adicionales..."></textarea>
            </div>
            <div class="md:col-span-2 flex gap-2 justify-end">
              <button type="button" @click="showCreateForm = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                Cancelar
              </button>
              <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
                Crear Orden
              </button>
            </div>
          </form>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Cargando órdenes...</p>
        </div>

        <!-- Orders Table -->
        <div v-else-if="!loading && orders.length > 0" class="bg-white rounded-lg shadow border">
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Orden</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cantidad</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Entrega</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="order in filteredOrders" :key="order.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-purple-600">{{ order.order_number }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ order.client_name }}</td>
                    <td class="px-6 py-4 text-sm text-gray-900">{{ order.product }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ order.quantity }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(order.status)]">
                        {{ getStatusLabel(order.status) }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(order.delivery_date) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div class="flex gap-2">
                        <button @click="viewOrder(order)" class="text-purple-600 hover:text-purple-800">
                          Ver
                        </button>
                        <button @click="deleteOrder(order.id)" class="text-red-600 hover:text-red-800">
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="bg-white p-12 rounded-lg shadow border text-center">
          <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="text-gray-600">No hay órdenes de producción registradas</p>
          <button @click="showCreateForm = true" class="mt-4 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
            Crear Primera Orden
          </button>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'

export default {
  name: 'ProduccionView',
  components: {
    BaseLayout
  },
  data() {
    return {
      orders: [],
      loading: false,
      showCreateForm: false,
      newOrder: {
        order_number: '',
        client_name: '',
        product: '',
        quantity: 1,
        delivery_date: new Date().toISOString().split('T')[0],
        priority: 'normal',
        notes: '',
        status: 'pendiente'
      },
      stats: {
        inProduction: 0,
        pending: 0,
        completed: 0,
        urgent: 0
      },
      filters: {
        status: ''
      }
    }
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => {
        if (this.filters.status && order.status !== this.filters.status) return false
        return true
      })
    }
  },
  mounted() {
    this.loadProduction()
  },
  methods: {
    loadProduction() {
      this.loading = true
      // Simulación de datos - reemplazar con llamada real al backend
      setTimeout(() => {
        this.orders = [
          {
            id: 1,
            order_number: 'PROD-001',
            client_name: 'Cliente Demo',
            product: 'Impresión de folletos',
            quantity: 1000,
            status: 'en_proceso',
            delivery_date: '2025-12-20',
            priority: 'alta'
          }
        ]
        this.calculateStats()
        this.loading = false
      }, 500)
    },

    createOrder() {
      const order = {
        ...this.newOrder,
        id: Date.now(),
        quantity: parseInt(this.newOrder.quantity)
      }
      this.orders.push(order)
      this.showCreateForm = false
      this.resetForm()
      this.calculateStats()
      alert('Orden creada exitosamente')
    },

    resetForm() {
      this.newOrder = {
        order_number: '',
        client_name: '',
        product: '',
        quantity: 1,
        delivery_date: new Date().toISOString().split('T')[0],
        priority: 'normal',
        notes: '',
        status: 'pendiente'
      }
    },

    calculateStats() {
      this.stats.inProduction = this.orders.filter(o => o.status === 'en_proceso').length
      this.stats.pending = this.orders.filter(o => o.status === 'pendiente').length
      this.stats.completed = this.orders.filter(o => o.status === 'completada').length
      this.stats.urgent = this.orders.filter(o => o.priority === 'urgente').length
    },

    getStatusClass(status) {
      const classes = {
        'pendiente': 'bg-yellow-100 text-yellow-800',
        'en_proceso': 'bg-blue-100 text-blue-800',
        'completada': 'bg-green-100 text-green-800',
        'cancelada': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },

    getStatusLabel(status) {
      const labels = {
        'pendiente': 'Pendiente',
        'en_proceso': 'En Proceso',
        'completada': 'Completada',
        'cancelada': 'Cancelada'
      }
      return labels[status] || status
    },

    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleDateString('es-MX')
    },

    viewOrder(order) {
      alert(`Orden: ${order.order_number}\nCliente: ${order.client_name}\nProducto: ${order.product}\nCantidad: ${order.quantity}\nPrioridad: ${order.priority}`)
    },

    deleteOrder(id) {
      if (!confirm('¿Está seguro de eliminar esta orden?')) return
      this.orders = this.orders.filter(o => o.id !== id)
      this.calculateStats()
    }
  }
}
</script>
