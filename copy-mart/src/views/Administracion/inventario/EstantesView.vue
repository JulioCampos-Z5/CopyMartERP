<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-amber-50 p-6 rounded-lg border border-amber-200">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-amber-800 mb-2">Estantes</h1>
              <p class="text-amber-600">Gestiona los estantes del almacén por sección</p>
            </div>
            <button @click="openModal()" class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Estante
            </button>
          </div>
        </div>

        <!-- Filtro por Sección -->
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="flex flex-wrap gap-2">
            <button 
              @click="selectedSection = ''" 
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                selectedSection === '' ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              Todas
            </button>
            <button 
              v-for="s in sections" 
              :key="s.value"
              @click="selectedSection = s.value" 
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                selectedSection === s.value ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              {{ s.label }}
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-600"></div>
        </div>

        <!-- Grid de Estantes -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="shelf in filteredShelves" 
            :key="shelf.shelf_id" 
            class="bg-white rounded-lg shadow border hover:shadow-md transition-shadow"
          >
            <div class="p-5">
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">{{ shelf.name }}</h3>
                  <span :class="['px-2 py-1 text-xs font-medium rounded mt-2 inline-block', sectionClasses[shelf.section]]">
                    {{ sectionLabels[shelf.section] }}
                  </span>
                </div>
                <div class="flex gap-2">
                  <button @click="openModal(shelf)" class="text-amber-600 hover:text-amber-900" title="Editar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button @click="confirmDelete(shelf)" class="text-red-600 hover:text-red-900" title="Eliminar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
              <p v-if="shelf.description" class="text-sm text-gray-500 mt-3">{{ shelf.description }}</p>
              <div class="mt-4 pt-4 border-t border-gray-100">
                <router-link 
                  :to="`/administracion/inventario?shelf_id=${shelf.shelf_id}`" 
                  class="text-sm text-amber-600 hover:text-amber-800 flex items-center gap-1"
                >
                  Ver items en este estante
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-if="filteredShelves.length === 0" class="col-span-full text-center py-12 text-gray-500">
            No hay estantes {{ selectedSection ? 'en esta sección' : '' }}
          </div>
        </div>
      </div>

      <!-- Modal Crear/Editar -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h3 class="text-xl font-semibold mb-4">{{ form.shelf_id ? 'Editar' : 'Nuevo' }} Estante</h3>
          <form @submit.prevent="saveShelf" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
              <input v-model="form.name" type="text" required placeholder="Ej: Estante A-1" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Sección *</label>
              <select v-model="form.section" required class="w-full px-3 py-2 border rounded-lg">
                <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea v-model="form.description" rows="3" class="w-full px-3 py-2 border rounded-lg" placeholder="Descripción opcional..."></textarea>
            </div>
            <div class="flex justify-end gap-3 pt-4">
              <button type="button" @click="showModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
                Cancelar
              </button>
              <button type="submit" :disabled="saving" class="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 disabled:opacity-50">
                {{ saving ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import { shelfService, type Shelf, type SectionLocation } from '@/services/inventoryService'

const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const selectedSection = ref<string>('')

const shelves = ref<Shelf[]>([])

const form = reactive({
  shelf_id: null as number | null,
  name: '',
  section: 'seccion_1' as SectionLocation,
  description: ''
})

const sections = [
  { value: 'seccion_1', label: 'Sección 1' },
  { value: 'seccion_2', label: 'Sección 2' },
  { value: 'seccion_3', label: 'Sección 3' },
  { value: 'seccion_4', label: 'Sección 4' },
  { value: 'seccion_5', label: 'Sección 5' },
  { value: 'seccion_6', label: 'Sección 6' }
]

const sectionLabels: Record<string, string> = {
  seccion_1: 'Sección 1',
  seccion_2: 'Sección 2',
  seccion_3: 'Sección 3',
  seccion_4: 'Sección 4',
  seccion_5: 'Sección 5',
  seccion_6: 'Sección 6'
}

const sectionClasses: Record<string, string> = {
  seccion_1: 'bg-red-100 text-red-800',
  seccion_2: 'bg-orange-100 text-orange-800',
  seccion_3: 'bg-yellow-100 text-yellow-800',
  seccion_4: 'bg-green-100 text-green-800',
  seccion_5: 'bg-blue-100 text-blue-800',
  seccion_6: 'bg-purple-100 text-purple-800'
}

const filteredShelves = computed(() => {
  if (!selectedSection.value) return shelves.value
  return shelves.value.filter(s => s.section === selectedSection.value)
})

const loadShelves = async () => {
  loading.value = true
  try {
    shelves.value = await shelfService.getShelves()
  } catch (error) {
    console.error('Error cargando estantes:', error)
  } finally {
    loading.value = false
  }
}

const openModal = (shelf?: Shelf) => {
  if (shelf) {
    form.shelf_id = shelf.shelf_id
    form.name = shelf.name
    form.section = shelf.section
    form.description = shelf.description || ''
  } else {
    form.shelf_id = null
    form.name = ''
    form.section = selectedSection.value as SectionLocation || 'seccion_1'
    form.description = ''
  }
  showModal.value = true
}

const saveShelf = async () => {
  saving.value = true
  try {
    const data = {
      name: form.name,
      section: form.section,
      description: form.description || undefined
    }

    if (form.shelf_id) {
      await shelfService.updateShelf(form.shelf_id, data)
    } else {
      await shelfService.createShelf(data)
    }

    showModal.value = false
    await loadShelves()
  } catch (error: any) {
    console.error('Error guardando estante:', error)
    alert(error.message || 'Error al guardar')
  } finally {
    saving.value = false
  }
}

const confirmDelete = async (shelf: Shelf) => {
  if (confirm(`¿Estás seguro de eliminar el estante "${shelf.name}"?`)) {
    try {
      await shelfService.deleteShelf(shelf.shelf_id)
      await loadShelves()
    } catch (error: any) {
      console.error('Error eliminando estante:', error)
      alert(error.message || 'Error al eliminar')
    }
  }
}

onMounted(() => {
  loadShelves()
})
</script>
