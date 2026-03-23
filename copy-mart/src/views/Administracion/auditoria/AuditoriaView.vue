<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Auditoría</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Registro de actividad del sistema</p>
      </div>

      <!-- Filters -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6 flex flex-wrap gap-4 items-end">
        <div>
          <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Módulo</label>
          <select v-model="filterModule" class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-900 dark:text-white">
            <option value="">Todos</option>
            <option v-for="m in modules" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Acción</label>
          <select v-model="filterAction" class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-900 dark:text-white">
            <option value="">Todas</option>
            <option value="create">Crear</option>
            <option value="update">Editar</option>
            <option value="delete">Eliminar</option>
            <option value="login">Login</option>
            <option value="logout">Logout</option>
          </select>
        </div>
        <button @click="loadLogs" class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 text-sm">
          Filtrar
        </button>
      </div>

      <!-- Table -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div v-if="loading" class="p-8 text-center text-gray-400">Cargando...</div>
        <div v-else-if="logs.length === 0" class="p-8 text-center text-gray-400 dark:text-gray-500">
          No hay registros de auditoría
        </div>
        <table v-else class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Usuario</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Acción</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Módulo</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Detalle</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">IP</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="log in logs" :key="log.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap">{{ formatDate(log.created_at) }}</td>
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ log.user_name || 'Sistema' }}</td>
              <td class="px-4 py-3">
                <span :class="actionBadge(log.action)" class="px-2 py-1 text-xs rounded-full font-medium">
                  {{ log.action }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-700 dark:text-gray-300 capitalize">{{ log.module }}</td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate">{{ log.detail || '-' }}</td>
              <td class="px-4 py-3 text-sm text-gray-400 dark:text-gray-500 font-mono">{{ log.ip_address || '-' }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div class="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-900">
          <button @click="prevPage" :disabled="page === 0" class="px-3 py-1 bg-white dark:bg-gray-700 border rounded text-sm disabled:opacity-50">
            Anterior
          </button>
          <span class="text-sm text-gray-500 dark:text-gray-400">Página {{ page + 1 }}</span>
          <button @click="nextPage" :disabled="logs.length < pageSize" class="px-3 py-1 bg-white dark:bg-gray-700 border rounded text-sm disabled:opacity-50">
            Siguiente
          </button>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import auditService, { type AuditLog } from '@/services/auditService'

const logs = ref<AuditLog[]>([])
const loading = ref(true)
const page = ref(0)
const pageSize = 50
const filterModule = ref('')
const filterAction = ref('')

const modules = ['clients', 'sales', 'rents', 'billing', 'tickets', 'equipment', 'purchases', 'inventory', 'rh', 'auth']

async function loadLogs() {
  loading.value = true
  try {
    logs.value = await auditService.getLogs({
      skip: page.value * pageSize,
      limit: pageSize,
      module: filterModule.value || undefined,
      action: filterAction.value || undefined
    })
  } catch (e) {
    console.error('Error loading audit logs:', e)
  }
  loading.value = false
}

function prevPage() {
  if (page.value > 0) { page.value--; loadLogs() }
}

function nextPage() {
  page.value++; loadLogs()
}

function formatDate(d: string) {
  return new Date(d).toLocaleString('es-MX', { dateStyle: 'short', timeStyle: 'short' })
}

function actionBadge(action: string) {
  const map: Record<string, string> = {
    create: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    update: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    delete: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    login: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    logout: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
  }
  return map[action] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

onMounted(() => loadLogs())
</script>
