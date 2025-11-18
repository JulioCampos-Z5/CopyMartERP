<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header del Dashboard -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-2">Bienvenido, {{ userName }}</p>
        <p class="text-sm text-gray-500">Última actualización: {{ currentDateTime }}</p>
      </div>
        
        <!-- Tarjetas de métricas -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div 
            v-for="metric in metrics" 
            :key="metric.name"
            class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200 border-l-4"
            :class="metric.borderColor"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">{{ metric.name }}</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ metric.value }}</p>
                <div class="flex items-center mt-3">
                  <span :class="[
                    metric.change >= 0 ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50',
                    'text-xs font-semibold px-2 py-1 rounded-full flex items-center'
                  ]">
                    <svg v-if="metric.change >= 0" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                    <svg v-else class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                    </svg>
                    {{ metric.change >= 0 ? '+' : '' }}{{ metric.change }}%
                  </span>
                  <span class="text-gray-500 text-xs ml-2">vs mes anterior</span>
                </div>
              </div>
              <div :class="['p-4 rounded-full', metric.bgColor]">
                <svg class="h-8 w-8" :class="metric.iconColor" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="metric.icon" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Gráficos y tablas -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <!-- Ventas Recientes -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-bold text-gray-900">Ventas Recientes</h3>
              <router-link to="/ventas" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
                Ver todas →
              </router-link>
            </div>
            <div class="space-y-4">
              <div v-for="sale in recentSales" :key="sale.id" 
                   class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div class="flex items-center space-x-4">
                  <div class="h-12 w-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-md">
                    <span class="text-white font-bold text-lg">{{ sale.customer.charAt(0) }}</span>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-gray-900">{{ sale.customer }}</p>
                    <p class="text-xs text-gray-600">{{ sale.product }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ formatDate(sale.date) }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-lg font-bold text-green-600">${{ sale.amount.toLocaleString() }}</p>
                  <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">Completado</span>
                </div>
              </div>
              <div v-if="recentSales.length === 0" class="text-center py-8 text-gray-500">
                <svg class="h-12 w-12 mx-auto mb-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                No hay ventas recientes
              </div>
            </div>
          </div>
          
          <!-- Productos más vendidos -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-bold text-gray-900">Productos Más Vendidos</h3>
              <router-link to="/inventario" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
                Ver inventario →
              </router-link>
            </div>
            <div class="space-y-4">
              <div v-for="(product, index) in topProducts" :key="product.id" 
                   class="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition-colors">
                <div class="flex items-center space-x-4 flex-1">
                  <div class="flex items-center justify-center h-8 w-8 rounded-full font-bold text-sm"
                       :class="index === 0 ? 'bg-yellow-100 text-yellow-700' : 
                               index === 1 ? 'bg-gray-100 text-gray-700' : 
                               index === 2 ? 'bg-orange-100 text-orange-700' : 
                               'bg-blue-50 text-blue-600'">
                    {{ index + 1 }}
                  </div>
                  <div class="flex-1">
                    <p class="text-sm font-semibold text-gray-900">{{ product.name }}</p>
                    <p class="text-xs text-gray-500">{{ product.sales }} unidades vendidas</p>
                  </div>
                </div>
                <div class="flex items-center space-x-3">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div 
                      class="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500" 
                      :style="{ width: `${(product.sales / topProducts[0].sales) * 100}%` }"
                    ></div>
                  </div>
                  <span class="text-sm font-bold text-gray-900 min-w-[80px] text-right">${{ product.revenue.toLocaleString() }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Acciones rápidas -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
          <h3 class="text-lg font-bold text-gray-900 mb-6">Acciones Rápidas</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button 
              v-for="action in quickActions" 
              :key="action.name"
              @click="action.action"
              class="flex flex-col items-center p-6 bg-gradient-to-br hover:scale-105 rounded-xl transition-all duration-200 shadow-sm hover:shadow-md border border-gray-100"
              :class="action.gradient"
            >
              <div :class="['p-4 rounded-full mb-3 shadow-md', action.bgColor]">
                <svg class="h-7 w-7" :class="action.iconColor" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.icon" />
                </svg>
              </div>
              <span class="text-sm font-semibold text-gray-700 text-center">{{ action.name }}</span>
            </button>
          </div>
        </div>
        
        <!-- Alertas e Inventario bajo -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <!-- Inventario bajo -->
          <div class="bg-white rounded-lg shadow-md p-6" v-if="lowStockItems.length > 0">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center space-x-2">
                <svg class="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <h3 class="text-lg font-bold text-gray-900">Inventario Bajo</h3>
              </div>
              <span class="bg-red-100 text-red-800 text-xs font-bold px-3 py-1 rounded-full">
                {{ lowStockItems.length }} productos
              </span>
            </div>
            <div class="space-y-3">
              <div v-for="item in lowStockItems" :key="item.id" 
                   class="flex items-center justify-between p-4 bg-red-50 border-l-4 border-red-500 rounded-lg hover:bg-red-100 transition-colors">
                <div>
                  <p class="text-sm font-semibold text-gray-900">{{ item.name }}</p>
                  <p class="text-xs text-gray-600 mt-1">SKU: {{ item.sku }}</p>
                </div>
                <div class="text-right">
                  <p class="text-lg font-bold text-red-600">{{ item.stock }}</p>
                  <p class="text-xs text-gray-500">Mín: {{ item.minStock }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Actividad Reciente -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-6">Actividad Reciente</h3>
            <div class="space-y-4">
              <div v-for="activity in recentActivity" :key="activity.id" 
                   class="flex items-start space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                <div :class="['p-2 rounded-full', activity.iconBg]">
                  <svg class="h-4 w-4" :class="activity.iconColor" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="activity.icon" />
                  </svg>
                </div>
                <div class="flex-1">
                  <p class="text-sm text-gray-900">{{ activity.description }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ activity.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '../components/BaseLayout.vue'

export default {
  name: 'DashboardView',
  components: {
    BaseLayout
  },
  data() {
    return {
      userName: 'Usuario',
      currentDateTime: '',
      metrics: [
        {
          name: 'Ventas del Día',
          value: '$12,450',
          change: 8.2,
          icon: 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
          bgColor: 'bg-green-100',
          iconColor: 'text-green-600',
          borderColor: 'border-green-500',
          gradient: 'from-green-50 to-white'
        },
        {
          name: 'Pedidos Activos',
          value: '24',
          change: 12.5,
          icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
          bgColor: 'bg-blue-100',
          iconColor: 'text-blue-600',
          borderColor: 'border-blue-500',
          gradient: 'from-blue-50 to-white'
        },
        {
          name: 'Total Clientes',
          value: '1,240',
          change: 5.7,
          icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
          bgColor: 'bg-purple-100',
          iconColor: 'text-purple-600',
          borderColor: 'border-purple-500',
          gradient: 'from-purple-50 to-white'
        },
        {
          name: 'En Inventario',
          value: '456',
          change: -2.1,
          icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
          bgColor: 'bg-orange-100',
          iconColor: 'text-orange-600',
          borderColor: 'border-orange-500',
          gradient: 'from-orange-50 to-white'
        }
      ],
      recentSales: [
        {
          id: 1,
          customer: 'María González',
          product: 'Papel Bond A4 - Resma 500 hojas',
          amount: 1250,
          date: new Date()
        },
        {
          id: 2,
          customer: 'José Ramírez',
          product: 'Tinta HP 664XL Negro',
          amount: 890,
          date: new Date()
        },
        {
          id: 3,
          customer: 'Ana Martínez',
          product: 'Copias B/N - 1000 unidades',
          amount: 450,
          date: new Date(Date.now() - 86400000)
        },
        {
          id: 4,
          customer: 'Luis Torres',
          product: 'Encuadernación + Anillado',
          amount: 320,
          date: new Date(Date.now() - 86400000)
        },
        {
          id: 5,
          customer: 'Carmen Díaz',
          product: 'Impresión Color A3 - 50 copias',
          amount: 650,
          date: new Date(Date.now() - 172800000)
        }
      ],
      topProducts: [
        { id: 1, name: 'Papel Bond A4', sales: 150, revenue: 18750 },
        { id: 2, name: 'Copias Blanco y Negro', sales: 120, revenue: 5400 },
        { id: 3, name: 'Tinta HP 664XL', sales: 80, revenue: 7120 },
        { id: 4, name: 'Servicio de Encuadernación', sales: 65, revenue: 2080 },
        { id: 5, name: 'Copias a Color', sales: 45, revenue: 2250 }
      ],
      lowStockItems: [
        { id: 1, name: 'Tinta Canon 240XL Negro', sku: 'TNT-CN-240XL', stock: 3, minStock: 10 },
        { id: 2, name: 'Papel Fotográfico A4', sku: 'PPL-FOTO-A4', stock: 5, minStock: 15 },
        { id: 3, name: 'Espirales Plástico 12mm', sku: 'ESP-PLS-12MM', stock: 8, minStock: 20 }
      ],
      quickActions: [
        {
          name: 'Nueva Venta',
          icon: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
          bgColor: 'bg-green-500',
          iconColor: 'text-white',
          gradient: 'from-green-50 to-green-100',
          action: () => this.navigateTo('/ventas')
        },
        {
          name: 'Registrar Producto',
          icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
          bgColor: 'bg-blue-500',
          iconColor: 'text-white',
          gradient: 'from-blue-50 to-blue-100',
          action: () => this.navigateTo('/inventario')
        },
        {
          name: 'Nuevo Cliente',
          icon: 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z',
          bgColor: 'bg-purple-500',
          iconColor: 'text-white',
          gradient: 'from-purple-50 to-purple-100',
          action: () => this.navigateTo('/clientes')
        },
        {
          name: 'Ver Reportes',
          icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
          bgColor: 'bg-orange-500',
          iconColor: 'text-white',
          gradient: 'from-orange-50 to-orange-100',
          action: () => this.navigateTo('/reportes')
        }
      ],
      recentActivity: [
        {
          id: 1,
          description: 'Nueva venta registrada - María González',
          time: 'Hace 5 minutos',
          icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
          iconBg: 'bg-green-100',
          iconColor: 'text-green-600'
        },
        {
          id: 2,
          description: 'Producto actualizado - Papel Bond A4',
          time: 'Hace 15 minutos',
          icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
          iconBg: 'bg-blue-100',
          iconColor: 'text-blue-600'
        },
        {
          id: 3,
          description: 'Cliente registrado - Luis Torres',
          time: 'Hace 1 hora',
          icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
          iconBg: 'bg-purple-100',
          iconColor: 'text-purple-600'
        },
        {
          id: 4,
          description: 'Alerta de stock bajo - Tinta Canon 240XL',
          time: 'Hace 2 horas',
          icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
          iconBg: 'bg-red-100',
          iconColor: 'text-red-600'
        }
      ]
    }
  },
  methods: {
    formatDate(date) {
      const now = new Date()
      const diff = now - date
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      
      if (days === 0) {
        return 'Hoy'
      } else if (days === 1) {
        return 'Ayer'
      } else {
        return date.toLocaleDateString('es-ES', {
          day: 'numeric',
          month: 'short'
        })
      }
    },
    navigateTo(path) {
      this.$router.push(path).catch(() => {
        console.log(`Navegando a ${path}`)
      })
    },
    updateDateTime() {
      const now = new Date()
      this.currentDateTime = now.toLocaleString('es-ES', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    loadUserData() {
      try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
          const user = JSON.parse(userStr)
          this.userName = user.full_name || 'Usuario'
        }
      } catch (error) {
        console.error('Error loading user data:', error)
      }
    }
  },
  mounted() {
    this.loadUserData()
    this.updateDateTime()
    // Actualizar el reloj cada minuto
    setInterval(() => {
      this.updateDateTime()
    }, 60000)
  }
}
</script>