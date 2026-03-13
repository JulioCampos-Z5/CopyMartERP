<template>
  <BaseLayout>
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Migraciones de Base de Datos</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Verificar y sincronizar tablas con los modelos</p>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 mb-6">
        <button @click="loadTables" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
          Actualizar
        </button>
        <button @click="runMigration" :disabled="migrating" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm disabled:opacity-50">
          {{ migrating ? 'Ejecutando...' : 'Ejecutar Migración' }}
        </button>
      </div>

      <!-- Migration Result -->
      <div v-if="migrationResult" class="mb-6 p-4 rounded-lg" :class="migrationResult.success ? 'bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-700' : 'bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700'">
        <p class="text-sm font-medium" :class="migrationResult.success ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'">
          {{ migrationResult.success ? migrationResult.message : migrationResult.error }}
        </p>
      </div>

      <div v-if="loading" class="flex justify-center py-16">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
      </div>

      <template v-else-if="tablesData">
        <!-- Overview Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ tablesData.database_tables?.length || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Tablas en BD</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
            <p class="text-2xl font-bold text-blue-600">{{ tablesData.model_tables?.length || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Tablas en Modelos</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
            <p class="text-2xl font-bold text-green-600">{{ tablesData.present?.length || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Sincronizadas</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
            <p class="text-2xl font-bold" :class="tablesData.missing?.length > 0 ? 'text-red-600' : 'text-green-600'">{{ tablesData.missing?.length || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Faltan en BD</p>
          </div>
        </div>

        <!-- Missing Tables -->
        <div v-if="tablesData.missing?.length > 0" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4 mb-6">
          <h3 class="text-sm font-semibold text-red-700 dark:text-red-300 mb-2">Tablas que faltan en la base de datos:</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="t in tablesData.missing" :key="t" class="px-2 py-1 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-xs rounded font-mono">{{ t }}</span>
          </div>
        </div>

        <!-- Extra Tables -->
        <div v-if="tablesData.extra_in_db?.length > 0" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg p-4 mb-6">
          <h3 class="text-sm font-semibold text-yellow-700 dark:text-yellow-300 mb-2">Tablas extra en BD (no tienen modelo):</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="t in tablesData.extra_in_db" :key="t" class="px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 text-xs rounded font-mono">{{ t }}</span>
          </div>
        </div>

        <!-- Table List -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Todas las Tablas</h3>
          </div>
          <div class="divide-y divide-gray-100 dark:divide-gray-700">
            <div
              v-for="table in allTables"
              :key="table"
              class="flex items-center justify-between px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <div class="flex items-center gap-3">
                <span
                  class="w-2 h-2 rounded-full"
                  :class="tableStatus(table) === 'ok' ? 'bg-green-500' : tableStatus(table) === 'missing' ? 'bg-red-500' : 'bg-yellow-500'"
                ></span>
                <span class="text-sm font-mono text-gray-900 dark:text-white">{{ table }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-xs capitalize" :class="tableStatus(table) === 'ok' ? 'text-green-600' : tableStatus(table) === 'missing' ? 'text-red-600' : 'text-yellow-600'">
                  {{ tableStatus(table) === 'ok' ? 'Sincronizada' : tableStatus(table) === 'missing' ? 'Falta en BD' : 'Solo en BD' }}
                </span>
                <button
                  v-if="tableStatus(table) !== 'missing'"
                  @click="inspectTable(table)"
                  class="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400"
                >
                  Inspeccionar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Column Inspector Modal -->
        <div v-if="selectedTable" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center" @click.self="selectedTable = null">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-3xl mx-4 max-h-[80vh] overflow-hidden flex flex-col">
            <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white font-mono">{{ selectedTable }}</h3>
              <button @click="selectedTable = null" class="text-gray-400 hover:text-gray-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="flex-1 overflow-y-auto p-4">
              <div v-if="columnsLoading" class="text-center text-gray-400 py-8">Cargando columnas...</div>
              <template v-else-if="columnsData">
                <div v-if="columnsData.missing_in_db?.length > 0" class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <p class="text-sm font-medium text-red-700 dark:text-red-300">Columnas que faltan en BD:</p>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span v-for="c in columnsData.missing_in_db" :key="c" class="px-2 py-0.5 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-xs rounded font-mono">{{ c }}</span>
                  </div>
                </div>
                <div v-if="columnsData.extra_in_db?.length > 0" class="mb-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                  <p class="text-sm font-medium text-yellow-700 dark:text-yellow-300">Columnas extra en BD:</p>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span v-for="c in columnsData.extra_in_db" :key="c" class="px-2 py-0.5 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 text-xs rounded font-mono">{{ c }}</span>
                  </div>
                </div>
                <table class="min-w-full text-sm">
                  <thead>
                    <tr class="border-b dark:border-gray-700">
                      <th class="text-left py-2 text-gray-500 dark:text-gray-400 text-xs">Columna</th>
                      <th class="text-left py-2 text-gray-500 dark:text-gray-400 text-xs">Tipo en BD</th>
                      <th class="text-left py-2 text-gray-500 dark:text-gray-400 text-xs">Tipo en Modelo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="col in allColumns" :key="col" class="border-b dark:border-gray-700">
                      <td class="py-2 font-mono text-gray-900 dark:text-white">{{ col }}</td>
                      <td class="py-2 font-mono text-xs" :class="columnsData.db_columns?.[col] ? 'text-gray-600 dark:text-gray-400' : 'text-red-500'">
                        {{ columnsData.db_columns?.[col] || '— falta' }}
                      </td>
                      <td class="py-2 font-mono text-xs" :class="columnsData.model_columns?.[col] ? 'text-gray-600 dark:text-gray-400' : 'text-yellow-500'">
                        {{ columnsData.model_columns?.[col] || '— no en modelo' }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </template>
            </div>
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
const tablesData = ref<any>(null)
const migrating = ref(false)
const migrationResult = ref<any>(null)

// Column inspector
const selectedTable = ref<string | null>(null)
const columnsData = ref<any>(null)
const columnsLoading = ref(false)

const allTables = computed(() => {
  if (!tablesData.value) return []
  const set = new Set([
    ...(tablesData.value.database_tables || []),
    ...(tablesData.value.model_tables || [])
  ])
  return Array.from(set).sort()
})

const allColumns = computed(() => {
  if (!columnsData.value) return []
  const set = new Set([
    ...Object.keys(columnsData.value.db_columns || {}),
    ...Object.keys(columnsData.value.model_columns || {})
  ])
  return Array.from(set).sort()
})

function tableStatus(table: string) {
  if (tablesData.value?.missing?.includes(table)) return 'missing'
  if (tablesData.value?.extra_in_db?.includes(table)) return 'extra'
  return 'ok'
}

async function loadTables() {
  loading.value = true
  try { tablesData.value = await systemService.getDbTables() } catch (e) { console.error(e) }
  loading.value = false
}

async function runMigration() {
  migrating.value = true
  migrationResult.value = null
  try {
    migrationResult.value = await systemService.runMigration()
    loadTables()
  } catch (e: any) {
    migrationResult.value = { success: false, error: e.message }
  }
  migrating.value = false
}

async function inspectTable(table: string) {
  selectedTable.value = table
  columnsLoading.value = true
  columnsData.value = null
  try { columnsData.value = await systemService.getTableColumns(table) } catch (e) { console.error(e) }
  columnsLoading.value = false
}

onMounted(() => loadTables())
</script>
