<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-gradient-to-r from-indigo-50 to-blue-50 p-6 rounded-lg border border-indigo-200 mb-6">
        <h1 class="text-3xl font-bold text-indigo-800 mb-2">Gestión de Áreas</h1>
        <p class="text-indigo-600">Administra las áreas organizacionales de la empresa</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Total Áreas</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Sucursales</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.branches }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500">Clientes</h3>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.clients }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions and Search -->
      <div class="bg-white p-6 rounded-lg shadow border mb-6">
        <div class="flex flex-wrap gap-4">
          <button @click="openCreateModal" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Área
          </button>
          <button @click="loadAreas" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
          <div class="flex-1">
            <input v-model="searchQuery" type="text" placeholder="Buscar áreas..." class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
          </div>
        </div>
      </div>

      <!-- Areas Table -->
      <div class="bg-white rounded-lg shadow border">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Áreas Registradas</h2>
        </div>
        <div class="p-6">
          <div v-if="loading" class="text-center py-8">
            <p class="text-gray-500">Cargando áreas...</p>
          </div>
          <div v-else-if="error" class="text-center py-8">
            <p class="text-red-500">{{ error }}</p>
          </div>
          <div v-else class="overflow-x-auto">
            <table class="min-w-full table-auto">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sucursal</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="filteredAreas.length === 0">
                  <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                    No hay áreas registradas
                  </td>
                </tr>
                <tr v-for="area in filteredAreas" :key="area.area_id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-indigo-600">{{ area.area_id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ area.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ getClientName(area.branch_id) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ getBranchName(area.branch_id) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editArea(area)" class="text-indigo-600 hover:text-indigo-900 mr-3">Editar</button>
                    <button @click="deleteArea(area.area_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Modal Crear/Editar Área -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
          <div class="p-6 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-semibold text-gray-900">{{ editingArea ? 'Editar Área' : 'Nueva Área' }}</h3>
              <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <form @submit.prevent="editingArea ? updateArea() : createArea()" class="p-6">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Área *</label>
                <input v-model="areaForm.name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="Ej: Ventas, Compras, Contabilidad...">
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
                <select v-model="selectedClientId" @change="onClientChange" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                  <option :value="null">Seleccionar cliente...</option>
                  <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                    {{ client.name }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Sucursal *</label>
                <select v-model="areaForm.branch_id" required :disabled="!selectedClientId" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100">
                  <option :value="null">{{ selectedClientId ? 'Seleccionar sucursal...' : 'Seleccione un cliente primero' }}</option>
                  <option v-for="branch in filteredBranches" :key="branch.branch_id" :value="branch.branch_id">
                    {{ branch.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="mt-6 flex justify-end gap-2">
              <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                {{ editingArea ? 'Actualizar' : 'Crear' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import { clientService } from '@/services/clientService'
import type { Area, Client, Branch } from '@/types'

// Estado local
const areas = ref<Area[]>([])
const clients = ref<Client[]>([])
const branches = ref<Branch[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showModal = ref(false)
const editingArea = ref<Area | null>(null)
const searchQuery = ref('')
const selectedClientId = ref<number | null>(null)

const areaForm = ref({
  name: '',
  branch_id: null as number | null
})

const stats = computed(() => ({
  total: areas.value.length,
  branches: new Set(areas.value.map(a => a.branch_id)).size,
  clients: new Set(branches.value.map(b => b.client_id)).size
}))

const filteredBranches = computed(() => {
  if (!selectedClientId.value) return []
  return branches.value.filter(b => b.client_id === selectedClientId.value)
})

const filteredAreas = computed(() => {
  if (!searchQuery.value) return areas.value
  
  const query = searchQuery.value.toLowerCase()
  return areas.value.filter(area => 
    area.name.toLowerCase().includes(query) ||
    getBranchName(area.branch_id).toLowerCase().includes(query) ||
    getClientName(area.branch_id).toLowerCase().includes(query)
  )
})

const loadAreas = async () => {
  loading.value = true
  error.value = null
  try {
    // Cargar todas las áreas de todos los clientes
    const allAreas: Area[] = []
    for (const client of clients.value) {
      if (client.branches) {
        for (const branch of client.branches) {
          const branchAreas = await clientService.getBranchAreas(branch.branch_id)
          allAreas.push(...branchAreas)
        }
      }
    }
    areas.value = allAreas
  } catch (err: any) {
    error.value = 'Error al cargar áreas: ' + err.message
    console.error('Error loading areas:', err)
  } finally {
    loading.value = false
  }
}

const loadClients = async () => {
  try {
    const response = await clientService.getClients({ page: 1, pageSize: 100 })
    clients.value = response.items || []
    
    // Extraer todas las sucursales
    const allBranches: Branch[] = []
    for (const client of clients.value) {
      if (client.client_id) {
        const clientBranches = await clientService.getClientBranches(client.client_id)
        allBranches.push(...clientBranches)
      }
    }
    branches.value = allBranches
  } catch (err: any) {
    console.error('Error loading clients:', err)
  }
}

const getBranchName = (branchId: number): string => {
  const branch = branches.value.find(b => b.branch_id === branchId)
  return branch ? branch.name : '-'
}

const getClientName = (branchId: number): string => {
  const branch = branches.value.find(b => b.branch_id === branchId)
  if (!branch) return '-'
  const client = clients.value.find(c => c.client_id === branch.client_id)
  return client ? client.name : '-'
}

const openCreateModal = () => {
  editingArea.value = null
  areaForm.value = { name: '', branch_id: null }
  selectedClientId.value = null
  showModal.value = true
}

const editArea = (area: Area) => {
  editingArea.value = area
  areaForm.value = { name: area.name, branch_id: area.branch_id }
  
  // Encontrar el cliente de esta sucursal
  const branch = branches.value.find(b => b.branch_id === area.branch_id)
  selectedClientId.value = branch?.client_id || null
  
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingArea.value = null
  areaForm.value = { name: '', branch_id: null }
  selectedClientId.value = null
}

const onClientChange = () => {
  areaForm.value.branch_id = null
}

const createArea = async () => {
  if (!areaForm.value.branch_id) return
  
  try {
    await clientService.createArea(areaForm.value.branch_id, { name: areaForm.value.name })
    await loadAreas()
    closeModal()
    alert('Área creada exitosamente')
  } catch (err: any) {
    alert('Error al crear área: ' + err.message)
  }
}

const updateArea = async () => {
  if (!editingArea.value || !areaForm.value.branch_id) return
  
  try {
    await clientService.updateArea(editingArea.value.area_id, { name: areaForm.value.name })
    await loadAreas()
    closeModal()
    alert('Área actualizada exitosamente')
  } catch (err: any) {
    alert('Error al actualizar área: ' + err.message)
  }
}

const deleteArea = async (areaId: number) => {
  if (!confirm('¿Está seguro de eliminar esta área?')) return
  
  try {
    await clientService.deleteArea(areaId)
    await loadAreas()
    alert('Área eliminada exitosamente')
  } catch (err: any) {
    alert('Error al eliminar área: ' + err.message)
  }
}

onMounted(async () => {
  await loadClients()
  await loadAreas()
})
</script>
