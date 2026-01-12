<template>
  <div class="base-table">
    <!-- Filtros -->
    <div v-if="$slots.filters" class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
      <slot name="filters"></slot>
    </div>

    <!-- Acciones principales y búsqueda -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div class="flex-1 w-full sm:w-auto">
          <input
            v-if="searchable"
            v-model="searchQuery"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            @input="handleSearch"
          />
        </div>
        <div class="flex gap-2">
          <slot name="actions"></slot>
        </div>
      </div>
    </div>

    <!-- Estadísticas (opcional) -->
    <div v-if="$slots.stats" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
      <slot name="stats"></slot>
    </div>

    <!-- Tabla -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-200 border-t-blue-600"></div>
        <p class="mt-2 text-gray-600">{{ loadingText }}</p>
      </div>

      <div v-else-if="error" class="p-8 text-center text-red-600">
        <svg class="mx-auto h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <p>{{ error }}</p>
        <button v-if="onRetry" @click="onRetry" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Reintentar
        </button>
      </div>

      <div v-else-if="!data || data.length === 0" class="p-8 text-center text-gray-500">
        <svg class="mx-auto h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <p>{{ emptyText }}</p>
        <slot name="empty-action"></slot>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                v-for="column in columns"
                :key="column.key"
                :class="[
                  'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
                  column.headerClass
                ]"
              >
                {{ column.label }}
              </th>
              <th v-if="hasActions" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(row, index) in data" :key="getRowKey(row, index)" class="hover:bg-gray-50 transition-colors">
              <td
                v-for="column in columns"
                :key="column.key"
                :class="['px-6 py-4 whitespace-nowrap', column.cellClass]"
              >
                <slot :name="`cell-${column.key}`" :row="row" :value="getValue(row, column.key)">
                  <span v-if="column.badge" :class="getBadgeClass(getValue(row, column.key), column.badgeColors)">
                    {{ formatValue(row, column) }}
                  </span>
                  <span v-else :class="column.valueClass">
                    {{ formatValue(row, column) }}
                  </span>
                </slot>
              </td>
              <td v-if="hasActions" class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <slot name="row-actions" :row="row"></slot>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginación -->
      <div v-if="pagination && data && data.length > 0" class="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="text-sm text-gray-700">
            Mostrando <span class="font-medium">{{ startRecord }}</span> a <span class="font-medium">{{ endRecord }}</span> de
            <span class="font-medium">{{ pagination.total }}</span> resultados
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="goToPage(pagination.page - 1)"
              :disabled="pagination.page === 1"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <div class="hidden sm:flex gap-1">
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'px-3 py-2 border rounded-lg text-sm font-medium',
                  page === pagination.page
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                ]"
              >
                {{ page }}
              </button>
            </div>
            <button
              @click="goToPage(pagination.page + 1)"
              :disabled="pagination.page === pagination.total_pages"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true,
    // [{ key: 'name', label: 'Nombre', format: (row) => row.name, badge: false, badgeColors: {}, cellClass: '', headerClass: '', valueClass: '' }]
  },
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  pagination: {
    type: Object,
    default: null
    // { page: 1, page_size: 10, total: 0, total_pages: 0 }
  },
  searchable: {
    type: Boolean,
    default: true
  },
  searchPlaceholder: {
    type: String,
    default: 'Buscar...'
  },
  emptyText: {
    type: String,
    default: 'No hay datos para mostrar'
  },
  loadingText: {
    type: String,
    default: 'Cargando...'
  },
  rowKey: {
    type: String,
    default: 'id'
  },
  hasActions: {
    type: Boolean,
    default: true
  },
  onRetry: {
    type: Function,
    default: null
  }
})

const emit = defineEmits(['search', 'page-change'])

const searchQuery = ref('')

const handleSearch = () => {
  emit('search', searchQuery.value)
}

const getValue = (row, key) => {
  return key.split('.').reduce((obj, k) => obj?.[k], row)
}

const formatValue = (row, column) => {
  const value = getValue(row, column.key)
  if (column.format) {
    return column.format(row)
  }
  return value ?? '-'
}

const getBadgeClass = (value, colors = {}) => {
  const baseClass = 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full'
  const colorClass = colors[value] || 'bg-gray-100 text-gray-800'
  return `${baseClass} ${colorClass}`
}

const getRowKey = (row, index) => {
  return row[props.rowKey] || index
}

const startRecord = computed(() => {
  if (!props.pagination) return 0
  return (props.pagination.page - 1) * props.pagination.page_size + 1
})

const endRecord = computed(() => {
  if (!props.pagination) return 0
  return Math.min(props.pagination.page * props.pagination.page_size, props.pagination.total)
})

const visiblePages = computed(() => {
  if (!props.pagination) return []
  const { page, total_pages } = props.pagination
  const pages = []
  const maxVisible = 5
  
  let start = Math.max(1, page - Math.floor(maxVisible / 2))
  let end = Math.min(total_pages, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const goToPage = (page) => {
  if (page >= 1 && page <= props.pagination.total_pages) {
    emit('page-change', page)
  }
}
</script>

<style scoped>
.base-table {
  @apply space-y-4;
}
</style>
