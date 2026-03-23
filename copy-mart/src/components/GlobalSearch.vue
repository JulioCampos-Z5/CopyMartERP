<template>
  <div class="relative">
    <button
      @click="openSearch"
      class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      title="Buscar (Ctrl+K)"
    >
      <svg class="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </button>

    <!-- Search Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/50 z-[70] flex items-start justify-center pt-24" @click.self="showModal = false">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden">
          <div class="flex items-center gap-3 px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              ref="searchInput"
              v-model="query"
              type="text"
              placeholder="Buscar clientes, equipos, tickets..."
              class="flex-1 bg-transparent text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none"
              @input="onInput"
              @keydown.escape="showModal = false"
            />
            <kbd class="hidden sm:inline text-xs text-gray-400 border border-gray-300 dark:border-gray-600 rounded px-1.5 py-0.5">ESC</kbd>
          </div>

          <div class="max-h-80 overflow-y-auto">
            <div v-if="loading" class="p-6 text-center text-gray-400 text-sm">Buscando...</div>
            <div v-else-if="query.length > 0 && results.length === 0 && !loading" class="p-6 text-center text-gray-400 text-sm">
              Sin resultados para "{{ query }}"
            </div>
            <template v-else>
              <div
                v-for="r in results"
                :key="`${r.type}-${r.id}`"
                @click="goTo(r)"
                class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-100 dark:border-gray-700 last:border-0"
              >
                <span class="w-8 h-8 rounded-lg flex items-center justify-center text-sm" :class="typeColor(r.type)">
                  {{ typeEmoji(r.type) }}
                </span>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ r.title }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ r.subtitle }}</p>
                </div>
                <span class="text-xs text-gray-400 capitalize">{{ typeLabel(r.type) }}</span>
              </div>
            </template>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import systemService, { type SearchResult } from '@/services/systemService'

const router = useRouter()
const showModal = ref(false)
const query = ref('')
const results = ref<SearchResult[]>([])
const loading = ref(false)
const searchInput = ref<HTMLInputElement | null>(null)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function openSearch() {
  showModal.value = true
  query.value = ''
  results.value = []
  nextTick(() => searchInput.value?.focus())
}

function onInput() {
  if (debounceTimer) clearTimeout(debounceTimer)
  if (query.value.length < 2) { results.value = []; return }
  debounceTimer = setTimeout(doSearch, 300)
}

async function doSearch() {
  if (query.value.length < 2) return
  loading.value = true
  try {
    results.value = await systemService.globalSearch(query.value)
  } catch { results.value = [] }
  loading.value = false
}

function goTo(r: SearchResult) {
  showModal.value = false
  router.push(r.link)
}

function typeColor(type: string) {
  const map: Record<string, string> = {
    client: 'bg-blue-100 dark:bg-blue-900',
    equipment: 'bg-green-100 dark:bg-green-900',
    ticket: 'bg-yellow-100 dark:bg-yellow-900',
    sale: 'bg-purple-100 dark:bg-purple-900'
  }
  return map[type] || 'bg-gray-100 dark:bg-gray-700'
}

function typeEmoji(type: string) {
  const map: Record<string, string> = { client: '👤', equipment: '🖨️', ticket: '🎫', sale: '💰' }
  return map[type] || '📄'
}

function typeLabel(type: string) {
  const map: Record<string, string> = { client: 'Cliente', equipment: 'Equipo', ticket: 'Ticket', sale: 'Venta' }
  return map[type] || type
}

function onKeydown(e: KeyboardEvent) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    openSearch()
  }
}

onMounted(() => document.addEventListener('keydown', onKeydown))
onUnmounted(() => document.removeEventListener('keydown', onKeydown))
</script>
