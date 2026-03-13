<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Reportes</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Resumen general y métricas del sistema</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-16">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
      </div>

      <template v-else>
        <!-- KPI Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Clientes</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ summary.clients }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Ventas del Mes</p>
            <p class="text-3xl font-bold text-blue-600 dark:text-blue-400">{{ summary.sales?.this_month || 0 }}</p>
            <p class="text-xs text-gray-400">Total: {{ summary.sales?.total || 0 }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Rentas Activas</p>
            <p class="text-3xl font-bold text-green-600 dark:text-green-400">{{ summary.rents?.active || 0 }}</p>
            <p class="text-xs text-gray-400">Total: {{ summary.rents?.total || 0 }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Facturas Vencidas</p>
            <p class="text-3xl font-bold text-red-600 dark:text-red-400">{{ summary.billing?.overdue || 0 }}</p>
            <p class="text-xs text-gray-400">Pendientes: {{ summary.billing?.pending || 0 }}</p>
          </div>
        </div>

        <!-- Second row KPIs -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Tickets Abiertos</p>
            <p class="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{{ summary.tickets?.open || 0 }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Equipos</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ summary.equipment?.total || 0 }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Reparaciones Pendientes</p>
            <p class="text-3xl font-bold text-orange-600 dark:text-orange-400">{{ summary.repairs?.pending || 0 }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-5">
            <p class="text-sm text-gray-500 dark:text-gray-400">Compras Activas</p>
            <p class="text-3xl font-bold text-purple-600 dark:text-purple-400">{{ summary.purchases?.active || 0 }}</p>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Ventas por Mes -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Ventas por Mes</h3>
            <div v-if="salesByMonth.length" class="space-y-2">
              <div v-for="item in salesByMonth" :key="item.month" class="flex items-center gap-3">
                <span class="text-xs text-gray-500 dark:text-gray-400 w-16">{{ item.month }}</span>
                <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-6 overflow-hidden">
                  <div
                    class="bg-blue-500 h-6 rounded-full flex items-center justify-end pr-2"
                    :style="{ width: Math.max(barPercent(item.count, maxSalesMonth), 5) + '%' }"
                  >
                    <span class="text-xs text-white font-medium">{{ item.count }}</span>
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm text-center py-8">Sin datos de ventas</p>
          </div>

          <!-- Rentas por Estado -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Rentas por Estado</h3>
            <div v-if="rentsByStatus.length" class="space-y-3">
              <div v-for="item in rentsByStatus" :key="item.status" class="flex items-center gap-3">
                <span class="text-xs text-gray-500 dark:text-gray-400 w-24 capitalize">{{ item.status }}</span>
                <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-6 overflow-hidden">
                  <div
                    :class="statusColor(item.status)"
                    class="h-6 rounded-full flex items-center justify-end pr-2"
                    :style="{ width: Math.max(barPercent(item.count, maxRentsStatus), 5) + '%' }"
                  >
                    <span class="text-xs text-white font-medium">{{ item.count }}</span>
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm text-center py-8">Sin datos de rentas</p>
          </div>

          <!-- Cobranza (Aging) -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Estado de Cobranza</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center p-4 bg-green-50 dark:bg-green-900/30 rounded-lg">
                <p class="text-2xl font-bold text-green-700 dark:text-green-400">{{ billingAging.pagado || 0 }}</p>
                <p class="text-xs text-green-600 dark:text-green-500">Pagado</p>
              </div>
              <div class="text-center p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                <p class="text-2xl font-bold text-blue-700 dark:text-blue-400">{{ billingAging.vigente || 0 }}</p>
                <p class="text-xs text-blue-600 dark:text-blue-500">Vigente</p>
              </div>
              <div class="text-center p-4 bg-yellow-50 dark:bg-yellow-900/30 rounded-lg">
                <p class="text-2xl font-bold text-yellow-700 dark:text-yellow-400">{{ billingAging.vencido_pendiente || 0 }}</p>
                <p class="text-xs text-yellow-600 dark:text-yellow-500">Por Vencer</p>
              </div>
              <div class="text-center p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
                <p class="text-2xl font-bold text-red-700 dark:text-red-400">{{ billingAging.vencido || 0 }}</p>
                <p class="text-xs text-red-600 dark:text-red-500">Vencido</p>
              </div>
            </div>
          </div>

          <!-- Tickets por Tipo -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Tickets por Tipo</h3>
            <div v-if="ticketsByType.length" class="space-y-2">
              <div v-for="item in ticketsByType" :key="item.type" class="flex items-center gap-3">
                <span class="text-xs text-gray-500 dark:text-gray-400 w-24 capitalize">{{ item.type }}</span>
                <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-5 overflow-hidden">
                  <div
                    class="bg-orange-500 h-5 rounded-full flex items-center justify-end pr-2"
                    :style="{ width: Math.max(barPercent(item.count, maxTicketsType), 5) + '%' }"
                  >
                    <span class="text-xs text-white font-medium">{{ item.count }}</span>
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm text-center py-8">Sin datos</p>
          </div>

          <!-- Equipos por Ubicación -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 lg:col-span-2">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Equipos por Ubicación</h3>
            <div v-if="equipByLocation.length" class="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div v-for="item in equipByLocation" :key="item.location" class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ item.count }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400 capitalize">{{ item.location }}</p>
              </div>
            </div>
            <p v-else class="text-gray-400 text-sm text-center py-8">Sin datos</p>
          </div>
        </div>
      </template>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import systemService from '@/services/systemService'

const loading = ref(true)
const summary = ref<any>({})
const salesByMonth = ref<any[]>([])
const rentsByStatus = ref<any[]>([])
const billingAging = ref<any>({})
const ticketsByType = ref<any[]>([])
const equipByLocation = ref<any[]>([])

const maxSalesMonth = computed(() => Math.max(...salesByMonth.value.map((i: any) => i.count), 1))
const maxRentsStatus = computed(() => Math.max(...rentsByStatus.value.map((i: any) => i.count), 1))
const maxTicketsType = computed(() => Math.max(...ticketsByType.value.map((i: any) => i.count), 1))

function barPercent(value: number, max: number) {
  return Math.round((value / max) * 100)
}

function statusColor(status: string) {
  const map: Record<string, string> = {
    vigente: 'bg-green-500',
    pendiente: 'bg-yellow-500',
    finalizado: 'bg-gray-500',
    cancelado: 'bg-red-500',
    sin_firmar: 'bg-blue-500'
  }
  return map[status] || 'bg-gray-500'
}

onMounted(async () => {
  try {
    const [s, sm, rs, ba, tt, el] = await Promise.all([
      systemService.getReportsSummary(),
      systemService.getSalesByMonth(),
      systemService.getRentsByStatus(),
      systemService.getBillingAging(),
      systemService.getTicketsByType(),
      systemService.getEquipmentByLocation()
    ])
    summary.value = s
    salesByMonth.value = sm
    rentsByStatus.value = rs
    billingAging.value = ba
    ticketsByType.value = tt
    equipByLocation.value = el
  } catch (e) {
    console.error('Error loading reports:', e)
  }
  loading.value = false
})
</script>
