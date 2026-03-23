<template>
  <div class="relative">
    <!-- Bell Button -->
    <button
      @click="togglePanel"
      class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative"
      title="Notificaciones"
    >
      <svg class="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>

    <!-- Dropdown Panel -->
    <div
      v-if="showPanel"
      class="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 max-h-96 overflow-hidden flex flex-col"
    >
      <div class="flex items-center justify-between p-3 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-sm font-semibold text-gray-900 dark:text-white">Notificaciones</h3>
        <button
          v-if="unreadCount > 0"
          @click="markAllRead"
          class="text-xs text-orange-600 hover:text-orange-800"
        >
          Marcar todo leído
        </button>
      </div>
      <div class="overflow-y-auto flex-1">
        <div v-if="loading" class="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">Cargando...</div>
        <div v-else-if="notifications.length === 0" class="p-6 text-center text-gray-400 dark:text-gray-500 text-sm">
          Sin notificaciones
        </div>
        <template v-else>
          <div
            v-for="n in notifications"
            :key="n.id"
            @click="handleClick(n)"
            class="px-3 py-3 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer flex gap-3"
            :class="{ 'bg-orange-50 dark:bg-orange-900/20': !n.is_read }"
          >
            <div class="flex-shrink-0 mt-0.5">
              <span :class="typeIcon(n.type).color" class="w-8 h-8 rounded-full flex items-center justify-center text-sm">
                {{ typeIcon(n.type).emoji }}
              </span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ n.title }}</p>
              <p v-if="n.message" class="text-xs text-gray-500 dark:text-gray-400 line-clamp-2">{{ n.message }}</p>
              <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">{{ timeAgo(n.created_at) }}</p>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Overlay -->
    <div v-if="showPanel" @click="showPanel = false" class="fixed inset-0 z-40"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import notificationService, { type AppNotification } from '@/services/notificationService'

const router = useRouter()
const showPanel = ref(false)
const loading = ref(false)
const notifications = ref<AppNotification[]>([])
const unreadCount = ref(0)
let pollInterval: ReturnType<typeof setInterval> | null = null

function togglePanel() {
  showPanel.value = !showPanel.value
  if (showPanel.value) loadNotifications()
}

async function loadNotifications() {
  loading.value = true
  try {
    notifications.value = await notificationService.getAll({ limit: 20 })
    unreadCount.value = await notificationService.getUnreadCount()
  } catch { /* ignore */ }
  loading.value = false
}

async function pollUnread() {
  try {
    unreadCount.value = await notificationService.getUnreadCount()
  } catch { /* ignore */ }
}

async function markAllRead() {
  await notificationService.markAllRead()
  notifications.value.forEach(n => n.is_read = true)
  unreadCount.value = 0
}

async function handleClick(n: AppNotification) {
  if (!n.is_read) {
    await notificationService.markAsRead(n.id)
    n.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
  }
  showPanel.value = false
  if (n.link) router.push(n.link)
}

function typeIcon(type: string) {
  const map: Record<string, { emoji: string; color: string }> = {
    cobranza_vencida: { emoji: '💰', color: 'bg-red-100 dark:bg-red-900' },
    cobranza_por_vencer: { emoji: '⏰', color: 'bg-yellow-100 dark:bg-yellow-900' },
    ticket_urgente: { emoji: '🔥', color: 'bg-orange-100 dark:bg-orange-900' },
    compra_pendiente: { emoji: '📦', color: 'bg-blue-100 dark:bg-blue-900' },
    vacacion_pendiente: { emoji: '🏖️', color: 'bg-green-100 dark:bg-green-900' },
    renta_por_vencer: { emoji: '📋', color: 'bg-purple-100 dark:bg-purple-900' },
    sistema: { emoji: '⚙️', color: 'bg-gray-100 dark:bg-gray-700' },
    info: { emoji: 'ℹ️', color: 'bg-blue-100 dark:bg-blue-900' }
  }
  return map[type] || map.info
}

function timeAgo(dateStr: string) {
  const d = new Date(dateStr)
  const diff = Date.now() - d.getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'Justo ahora'
  if (mins < 60) return `Hace ${mins}m`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `Hace ${hrs}h`
  const days = Math.floor(hrs / 24)
  return `Hace ${days}d`
}

onMounted(() => {
  pollUnread()
  pollInterval = setInterval(pollUnread, 60000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>
