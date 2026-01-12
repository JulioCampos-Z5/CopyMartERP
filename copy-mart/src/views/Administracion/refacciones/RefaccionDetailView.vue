<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <button @click="goBack" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Volver a Inventario
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Detalle de Refacción</h1>
        <p class="text-gray-600 mt-2">Información completa de la refacción</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white p-12 rounded-lg shadow border text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando información...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {{ error }}
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Actions Bar -->
        <div class="bg-white p-4 rounded-lg shadow border flex justify-end gap-3">
          <button @click="editSparepart" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Editar
          </button>
        </div>

        <!-- Main Info Card -->
        <div class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-6">Información General</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <p class="text-sm text-gray-500 mb-1">Código</p>
              <p class="text-base font-medium text-purple-600">{{ sparepart.code || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Nombre</p>
              <p class="text-base font-medium text-gray-900">{{ sparepart.name || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Marca</p>
              <p class="text-base font-medium text-gray-900">{{ sparepart.brand || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Color</p>
              <div class="text-base font-medium">
                <span v-if="sparepart.color" :class="{
                  'bg-gray-800 text-white': sparepart.color === 'K',
                  'bg-yellow-400 text-gray-900': sparepart.color === 'Y',
                  'bg-pink-500 text-white': sparepart.color === 'M',
                  'bg-cyan-500 text-white': sparepart.color === 'C',
                  'bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-500 text-white': sparepart.color === 'COLOR'
                }" class="px-3 py-1 text-xs font-medium rounded inline-block">
                  {{ sparepart.color }}
                </span>
                <span v-else class="text-gray-400">-</span>
              </div>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Equipo Compatible</p>
              <p class="text-base font-medium text-gray-900">{{ sparepart.equipment || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 mb-1">Proveedor</p>
              <p class="text-base font-medium text-gray-900">{{ sparepart.supplier || '-' }}</p>
            </div>
          </div>
        </div>

        <!-- Description Card -->
        <div v-if="sparepart.description" class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Descripción</h2>
          <p class="text-gray-700">{{ sparepart.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { sparepartService } from '@/services/sparepartService.ts'

export default {
  name: 'RefaccionDetailView',
  components: {
    AppNavigation
  },
  data() {
    return {
      sparepart: {},
      loading: false,
      error: null
    }
  },
  async mounted() {
    await this.loadSparepart()
  },
  methods: {
    async loadSparepart() {
      this.loading = true
      this.error = null
      try {
        this.sparepart = await sparepartService.getSparepartById(this.$route.params.id)
      } catch (err) {
        this.error = 'Error al cargar la refacción: ' + err.message
      } finally {
        this.loading = false
      }
    },

    editSparepart() {
      this.$router.push(`/administracion/refacciones/editar/${this.$route.params.id}`)
    },

    goBack() {
      this.$router.push('/inventario')
    }
  }
}
</script>
