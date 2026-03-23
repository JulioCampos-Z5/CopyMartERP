<template>
  <BaseLayout>
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Configuración del Sistema</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">SMTP y Respaldos</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- SMTP -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Correo SMTP
          </h2>

          <div v-if="smtpLoading" class="py-4 text-center text-gray-400">Cargando...</div>
          <template v-else>
            <div class="space-y-3 mb-4">
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 dark:text-gray-400">Host</span>
                <span class="text-gray-900 dark:text-white font-mono">{{ smtp.host || 'No configurado' }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 dark:text-gray-400">Puerto</span>
                <span class="text-gray-900 dark:text-white font-mono">{{ smtp.port }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 dark:text-gray-400">Usuario</span>
                <span class="text-gray-900 dark:text-white font-mono">{{ smtp.user || 'No configurado' }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 dark:text-gray-400">Remitente</span>
                <span class="text-gray-900 dark:text-white font-mono">{{ smtp.from || '-' }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 dark:text-gray-400">Estado</span>
                <span :class="smtp.configured ? 'text-green-600' : 'text-red-600'" class="font-medium">
                  {{ smtp.configured ? 'Configurado' : 'No configurado' }}
                </span>
              </div>
            </div>

            <button
              @click="testSmtp"
              :disabled="smtpTesting || !smtp.configured"
              class="w-full bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50 text-sm"
            >
              {{ smtpTesting ? 'Probando...' : 'Probar Conexión SMTP' }}
            </button>

            <div v-if="smtpResult" class="mt-3 p-3 rounded-lg text-sm" :class="smtpResult.success ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300' : 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300'">
              {{ smtpResult.success ? smtpResult.message : smtpResult.error }}
            </div>

            <p class="text-xs text-gray-400 mt-3">La configuración SMTP se define en el archivo .env del servidor.</p>
          </template>
        </div>

        <!-- Backups -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
            </svg>
            Respaldos de Base de Datos
          </h2>

          <button
            @click="createBackup"
            :disabled="backupCreating"
            class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 text-sm mb-4"
          >
            {{ backupCreating ? 'Creando respaldo...' : 'Crear Respaldo Ahora' }}
          </button>

          <div v-if="backupResult" class="mb-4 p-3 rounded-lg text-sm" :class="backupResult.success ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300' : 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300'">
            <template v-if="backupResult.success">
              Respaldo creado: <strong>{{ backupResult.filename }}</strong> ({{ backupResult.size_mb }} MB)
            </template>
            <template v-else>Error: {{ backupResult.error }}</template>
          </div>

          <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Respaldos Disponibles</h3>
          <div v-if="backupsLoading" class="text-center text-gray-400 py-4 text-sm">Cargando...</div>
          <div v-else-if="backups.length === 0" class="text-center text-gray-400 py-4 text-sm">Sin respaldos</div>
          <div v-else class="space-y-2 max-h-64 overflow-y-auto">
            <div
              v-for="b in backups"
              :key="b.filename"
              class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded text-sm"
            >
              <div>
                <p class="text-gray-900 dark:text-white font-mono text-xs">{{ b.filename }}</p>
                <p class="text-xs text-gray-400">{{ formatDate(b.created_at) }} · {{ b.size_mb }} MB</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import systemService from '@/services/systemService'

// SMTP
const smtp = ref<any>({})
const smtpLoading = ref(true)
const smtpTesting = ref(false)
const smtpResult = ref<any>(null)

// Backups
const backups = ref<any[]>([])
const backupsLoading = ref(true)
const backupCreating = ref(false)
const backupResult = ref<any>(null)

async function loadSmtp() {
  smtpLoading.value = true
  try { smtp.value = await systemService.getSmtpConfig() } catch {}
  smtpLoading.value = false
}

async function testSmtp() {
  smtpTesting.value = true
  smtpResult.value = null
  try { smtpResult.value = await systemService.testSmtp() } catch (e: any) {
    smtpResult.value = { success: false, error: e.message }
  }
  smtpTesting.value = false
}

async function loadBackups() {
  backupsLoading.value = true
  try { backups.value = await systemService.listBackups() } catch {}
  backupsLoading.value = false
}

async function createBackup() {
  backupCreating.value = true
  backupResult.value = null
  try {
    backupResult.value = await systemService.createBackup()
    if (backupResult.value.success) loadBackups()
  } catch (e: any) {
    backupResult.value = { success: false, error: e.message }
  }
  backupCreating.value = false
}

function formatDate(d: string) {
  return new Date(d).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

onMounted(() => { loadSmtp(); loadBackups() })
</script>
