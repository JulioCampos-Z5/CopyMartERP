<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header del Dashboard -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-2">Bienvenido al panel de control de CopyMart ERP</p>
      </div>
      
      <!-- Tarjetas de métricas -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div 
          v-for="metric in metrics" 
          :key="metric.name"
          class="card hover:shadow-lg transition-shadow duration-200"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">{{ metric.name }}</p>
              <p class="text-2xl font-bold text-gray-900 mt-2">{{ metric.value }}</p>
              <div class="flex items-center mt-2">
                <span :class="[
                  metric.change >= 0 ? 'text-green-600' : 'text-red-600',
                  'text-sm font-medium flex items-center'
                ]">
                  <svg v-if="metric.change >= 0" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  <svg v-else class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                  </svg>
                  {{ Math.abs(metric.change) }}%
                </span>
                <span class="text-gray-500 text-sm ml-2">vs mes anterior</span>
              </div>
            </div>
            <div :class="[
              'p-3 rounded-full',
              metric.bgColor
            ]">
              <svg class="h-8 w-8" :class="metric.iconColor" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="metric.icon" />
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Gráficos y tablas -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Gráfico de ventas -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Ventas Recientes</h3>
          <div class="space-y-4">
            <div v-for="sale in recentSales" :key="sale.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <span class="text-primary-600 font-semibold text-sm">{{ sale.customer.charAt(0) }}</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ sale.customer }}</p>
                  <p class="text-xs text-gray-500">{{ sale.product }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-gray-900">${{ sale.amount.toLocaleString() }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(sale.date) }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Productos más vendidos -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Productos Más Vendidos</h3>
          <div class="space-y-4">
            <div v-for="product in topProducts" :key="product.id" class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="h-10 w-10 bg-gray-200 rounded-lg flex items-center justify-center">
                  <svg class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ product.name }}</p>
                  <p class="text-xs text-gray-500">{{ product.sales }} unidades vendidas</p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full" 
                    :style="{ width: `${(product.sales / topProducts[0].sales) * 100}%` }"
                  ></div>
                </div>
                <span class="text-sm font-medium text-gray-900">${{ product.revenue.toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Acciones rápidas -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button 
            v-for="action in quickActions" 
            :key="action.name"
            @click="action.action"
            class="flex flex-col items-center p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200"
          >
            <div :class="['p-3 rounded-full mb-3', action.bgColor]">
              <svg class="h-6 w-6" :class="action.iconColor" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.icon" />
              </svg>
            </div>
            <span class="text-sm font-medium text-gray-700 text-center">{{ action.name }}</span>
          </button>
        </div>
      </div>
      
      <!-- Inventario bajo -->
      <div class="mt-8 card" v-if="lowStockItems.length > 0">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Inventario Bajo</h3>
          <span class="bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
            {{ lowStockItems.length }} productos
          </span>
        </div>
        <div class="space-y-3">
          <div v-for="item in lowStockItems" :key="item.id" class="flex items-center justify-between p-3 bg-red-50 border border-red-200 rounded-lg">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ item.name }}</p>
              <p class="text-xs text-gray-500">SKU: {{ item.sku }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-red-600">{{ item.stock }} unidades</p>
              <p class="text-xs text-gray-500">Mín: {{ item.minStock }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Generador de PDFs -->
      <div class="mt-8">
        <PdfGenerator />
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '../components/AppNavigation.vue'
import PdfGenerator from '../components/PdfGenerator.vue'

export default {
  name: 'DashboardView',
  components: {
    AppNavigation,
    PdfGenerator
  },
  data() {
    return {
      metrics: [
        {
          name: 'Ventas Hoy',
          value: '$12,450',
          change: 8.2,
          icon: 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
          bgColor: 'bg-green-100',
          iconColor: 'text-green-600'
        },
        {
          name: 'Pedidos',
          value: '24',
          change: 12.5,
          icon: 'M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h2m5 0h2a2 2 0 002-2V7a2 2 0 00-2-2h-2m-5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M9 7h6',
          bgColor: 'bg-blue-100',
          iconColor: 'text-blue-600'
        },
        {
          name: 'Clientes',
          value: '1,240',
          change: 5.7,
          icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
          bgColor: 'bg-purple-100',
          iconColor: 'text-purple-600'
        },
        {
          name: 'Productos',
          value: '456',
          change: -2.1,
          icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
          bgColor: 'bg-orange-100',
          iconColor: 'text-orange-600'
        }
      ],
      recentSales: [
        {
          id: 1,
          customer: 'María González',
          product: 'Papel A4 - 500 hojas',
          amount: 1250,
          date: new Date('2025-11-02')
        },
        {
          id: 2,
          customer: 'José Ramírez',
          product: 'Tinta para impresora HP',
          amount: 890,
          date: new Date('2025-11-02')
        },
        {
          id: 3,
          customer: 'Ana Martínez',
          product: 'Copias B/N - 1000 unid.',
          amount: 450,
          date: new Date('2025-11-01')
        },
        {
          id: 4,
          customer: 'Luis Torres',
          product: 'Encuadernación',
          amount: 320,
          date: new Date('2025-11-01')
        }
      ],
      topProducts: [
        { id: 1, name: 'Papel A4', sales: 150, revenue: 18750 },
        { id: 2, name: 'Copias B/N', sales: 120, revenue: 5400 },
        { id: 3, name: 'Tinta HP', sales: 80, revenue: 7120 },
        { id: 4, name: 'Encuadernación', sales: 65, revenue: 2080 },
        { id: 5, name: 'Copias Color', sales: 45, revenue: 2250 }
      ],
      lowStockItems: [
        { id: 1, name: 'Tinta Canon 240XL', sku: 'TNT-CN-240XL', stock: 3, minStock: 10 },
        { id: 2, name: 'Papel Fotográfico', sku: 'PPL-FOTO-A4', stock: 5, minStock: 15 },
        { id: 3, name: 'Espirales Plásticos', sku: 'ESP-PLS-12MM', stock: 8, minStock: 20 }
      ],
      quickActions: [
        {
          name: 'Nueva Venta',
          icon: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
          bgColor: 'bg-green-100',
          iconColor: 'text-green-600',
          action: () => this.$router.push('/ventas/nueva')
        },
        {
          name: 'Agregar Producto',
          icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
          bgColor: 'bg-blue-100',
          iconColor: 'text-blue-600',
          action: () => this.$router.push('/inventario/nuevo')
        },
        {
          name: 'Nuevo Cliente',
          icon: 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z',
          bgColor: 'bg-purple-100',
          iconColor: 'text-purple-600',
          action: () => this.$router.push('/clientes/nuevo')
        },
        {
          name: 'Ver Reportes',
          icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
          bgColor: 'bg-orange-100',
          iconColor: 'text-orange-600',
          action: () => this.$router.push('/reportes')
        }
      ]
    }
  },
  methods: {
    formatDate(date) {
      return date.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'short'
      })
    }
  },
  mounted() {
    // Simulación de datos en tiempo real
    console.log('Dashboard cargado exitosamente')
  }
}
</script>