<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <button @click="$router.back()" class="text-orange-600 hover:text-orange-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Clientes
        </button>
      </div>

      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
      </div>

      <div v-else-if="client" class="space-y-6">
        <!-- Header -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ client.name }}</h1>
              <p v-if="client.comercial_name" class="text-lg text-gray-600">{{ client.comercial_name }}</p>
              <span :class="client.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" class="mt-2 inline-block px-3 py-1 text-sm font-semibold rounded-full">
                {{ client.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
            <button @click="editClient" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Editar
            </button>
          </div>
        </div>

        <!-- Información General -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Información General</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <dt class="text-sm font-medium text-gray-500">RFC</dt>
              <dd class="text-base text-gray-900 mt-1">{{ client.rfc || '-' }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Dirección</dt>
              <dd class="text-base text-gray-900 mt-1">{{ formatAddress(client) }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Ciudad</dt>
              <dd class="text-base text-gray-900 mt-1">{{ client.city || '-' }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Código Postal</dt>
              <dd class="text-base text-gray-900 mt-1">{{ client.zip_code || '-' }}</dd>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="bg-white rounded-lg shadow-md">
          <div class="border-b border-gray-200">
            <nav class="flex -mb-px">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id 
                    ? 'border-orange-500 text-orange-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm'
                ]"
              >
                {{ tab.label }}
                <span v-if="tab.count !== undefined" class="ml-2 px-2 py-1 text-xs rounded-full bg-gray-100">
                  {{ tab.count }}
                </span>
              </button>
            </nav>
          </div>

          <!-- Tab: Contacto Principal -->
          <div v-if="activeTab === 'contact'" class="p-6">
            <div v-if="client.contact" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Nombre</dt>
                  <dd class="text-base text-gray-900 mt-1">{{ client.contact.name }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Rol/Puesto</dt>
                  <dd class="text-base text-gray-900 mt-1">{{ client.contact.rol || '-' }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Teléfono</dt>
                  <dd class="text-base text-gray-900 mt-1">{{ client.contact.phone || '-' }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Email</dt>
                  <dd class="text-base text-gray-900 mt-1">{{ client.contact.email || '-' }}</dd>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              No hay contacto principal registrado
            </div>
          </div>

          <!-- Tab: Sucursales -->
          <div v-if="activeTab === 'branches'" class="p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold text-gray-900">Sucursales</h3>
              <button @click="openBranchModal()" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 text-sm">
                + Nueva Sucursal
              </button>
            </div>
            <div v-if="branches.length > 0" class="space-y-4">
              <div v-for="branch in branches" :key="branch.branch_id" class="border rounded-lg p-4 hover:bg-gray-50">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="flex items-center gap-2">
                      <h4 class="font-semibold text-gray-900">{{ branch.name }}</h4>
                      <span v-if="branch.is_main" class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">Principal</span>
                    </div>
                    <p class="text-sm text-gray-600 mt-1">{{ formatAddress(branch) }}</p>
                    <p v-if="branch.areas && branch.areas.length > 0" class="text-sm text-gray-500 mt-2">
                      {{ branch.areas.length }} área(s): {{ branch.areas.map(a => a.name).join(', ') }}
                    </p>
                  </div>
                  <div class="flex gap-2">
                    <button @click="manageBranchAreas(branch)" class="text-blue-600 hover:text-blue-800" title="Gestionar Áreas">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                    </button>
                    <button @click="openBranchModal(branch)" class="text-green-600 hover:text-green-800" title="Editar">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="deleteBranch(branch.branch_id)" class="text-red-600 hover:text-red-800" title="Eliminar">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              No hay sucursales registradas
            </div>
          </div>

          <!-- Tab: Contactos -->
          <div v-if="activeTab === 'contacts'" class="p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold text-gray-900">Contactos</h3>
              <button @click="openContactModal()" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 text-sm">
                + Nuevo Contacto
              </button>
            </div>
            <div v-if="contacts.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="contact in contacts" :key="contact.contact_id" class="border rounded-lg p-4 hover:bg-gray-50">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <h4 class="font-semibold text-gray-900">{{ contact.name }}</h4>
                    <p v-if="contact.position" class="text-sm text-gray-600">{{ contact.position }}</p>
                    <p v-if="contact.phone" class="text-sm text-gray-600 mt-1">📞 {{ contact.phone }}</p>
                    <p v-if="contact.email" class="text-sm text-gray-600">✉️ {{ contact.email }}</p>
                  </div>
                  <div class="flex gap-2">
                    <button @click="openContactModal(contact)" class="text-green-600 hover:text-green-800">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="deleteContact(contact.contact_id)" class="text-red-600 hover:text-red-800">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              No hay contactos adicionales registrados
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Sucursal -->
      <div v-if="showBranchModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showBranchModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-2xl">
          <h3 class="text-xl font-semibold mb-4">{{ branchForm.branch_id ? 'Editar' : 'Nueva' }} Sucursal</h3>
          <form @submit.prevent="saveBranch" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
                <input v-model="branchForm.name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div class="md:col-span-2">
                <label class="flex items-center gap-2">
                  <input v-model="branchForm.is_main" type="checkbox" class="rounded" />
                  <span class="text-sm text-gray-700">Sucursal principal</span>
                </label>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
                <input v-model="branchForm.address" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Colonia</label>
                <input v-model="branchForm.colonia" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
                <input v-model="branchForm.zip_code" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
                <input v-model="branchForm.city" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showBranchModal = false" class="px-4 py-2 border rounded-lg">Cancelar</button>
              <button type="submit" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal Contacto -->
      <div v-if="showContactModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showContactModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-2xl">
          <h3 class="text-xl font-semibold mb-4">{{ contactForm.contact_id ? 'Editar' : 'Nuevo' }} Contacto</h3>
          <form @submit.prevent="saveContact" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
                <input v-model="contactForm.name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Puesto</label>
                <input v-model="contactForm.position" type="text" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                <input v-model="contactForm.phone" type="tel" class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input v-model="contactForm.email" type="email" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showContactModal = false" class="px-4 py-2 border rounded-lg">Cancelar</button>
              <button type="submit" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal Áreas -->
      <div v-if="showAreasModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showAreasModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg">
          <h3 class="text-xl font-semibold mb-4">Áreas de {{ selectedBranch?.name }}</h3>
          <div class="mb-4">
            <form @submit.prevent="addArea" class="flex gap-2">
              <input v-model="newAreaName" type="text" placeholder="Nombre del área" class="flex-1 px-3 py-2 border rounded-lg" />
              <button type="submit" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700">Agregar</button>
            </form>
          </div>
          <div v-if="areas.length > 0" class="space-y-2">
            <div v-for="area in areas" :key="area.area_id" class="flex justify-between items-center p-2 border rounded">
              <span>{{ area.name }}</span>
              <button @click="deleteArea(area.area_id)" class="text-red-600 hover:text-red-800">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500">No hay áreas registradas</div>
          <div class="flex justify-end mt-4">
            <button @click="showAreasModal = false" class="px-4 py-2 border rounded-lg">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import { clientService } from '@/services/clientService'
import { contactService } from '@/services/contactService'
import type { Client, Branch, Contact, Area } from '@/types'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const client = ref<Client | null>(null)
const branches = ref<Branch[]>([])
const contacts = ref<Contact[]>([])
const areas = ref<Area[]>([])
const activeTab = ref('contact')

const showBranchModal = ref(false)
const showContactModal = ref(false)
const showAreasModal = ref(false)
const selectedBranch = ref<Branch | null>(null)
const newAreaName = ref('')

const branchForm = ref({
  branch_id: 0,
  name: '',
  is_main: false,
  address: '',
  colonia: '',
  zip_code: '',
  city: ''
})

const contactForm = ref({
  contact_id: 0,
  name: '',
  position: '',
  phone: '',
  email: '',
  client_id: 0
})

const tabs = computed(() => [
  { id: 'contact', label: 'Contacto Principal', count: client.value?.contact ? 1 : 0 },
  { id: 'branches', label: 'Sucursales', count: branches.value.length },
  { id: 'contacts', label: 'Contactos Adicionales', count: contacts.value.length }
])

const loadClient = async () => {
  loading.value = true
  try {
    const clientId = Number(route.params.id)
    client.value = await clientService.getClientById(clientId)
    await Promise.all([loadBranches(), loadContacts()])
  } catch (error) {
    console.error('Error loading client:', error)
    alert('Error al cargar el cliente')
  } finally {
    loading.value = false
  }
}

const loadBranches = async () => {
  try {
    branches.value = await clientService.getClientBranches(Number(route.params.id))
  } catch (error) {
    console.error('Error loading branches:', error)
  }
}

const loadContacts = async () => {
  try {
    const result = await contactService.getContacts({ client_id: Number(route.params.id) })
    contacts.value = result.items || []
  } catch (error) {
    console.error('Error loading contacts:', error)
  }
}

const editClient = () => {
  router.push({ name: 'ClienteEditar', params: { id: route.params.id } })
}

const formatAddress = (obj: any) => {
  const parts = []
  if (obj.address) parts.push(obj.address)
  if (obj.colonia) parts.push(obj.colonia)
  return parts.join(', ') || '-'
}

// Sucursales
const openBranchModal = (branch?: Branch) => {
  if (branch) {
    branchForm.value = { ...branch }
  } else {
    branchForm.value = {
      branch_id: 0,
      name: '',
      is_main: false,
      address: '',
      colonia: '',
      zip_code: '',
      city: ''
    }
  }
  showBranchModal.value = true
}

const saveBranch = async () => {
  try {
    const clientId = Number(route.params.id)
    if (branchForm.value.branch_id) {
      await clientService.updateBranch(branchForm.value.branch_id, branchForm.value)
    } else {
      await clientService.createBranch(clientId, { ...branchForm.value, client_id: clientId })
    }
    showBranchModal.value = false
    await loadBranches()
  } catch (error: any) {
    console.error('Error saving branch:', error)
    alert(`Error al guardar sucursal: ${error.message || error}`)
  }
}

const deleteBranch = async (branchId: number) => {
  if (!confirm('¿Estás seguro de eliminar esta sucursal?')) return
  try {
    await clientService.deleteBranch(branchId)
    await loadBranches()
  } catch (error: any) {
    console.error('Error deleting branch:', error)
    alert(`Error al eliminar sucursal: ${error.message || error}`)
  }
}

// Contactos
const openContactModal = (contact?: Contact) => {
  if (contact) {
    contactForm.value = { ...contact, client_id: Number(route.params.id) }
  } else {
    contactForm.value = {
      contact_id: 0,
      name: '',
      position: '',
      phone: '',
      email: '',
      client_id: Number(route.params.id)
    }
  }
  showContactModal.value = true
}

const saveContact = async () => {
  try {
    if (contactForm.value.contact_id) {
      await contactService.updateContact(contactForm.value.contact_id, contactForm.value)
    } else {
      await contactService.createContact(contactForm.value)
    }
    showContactModal.value = false
    await loadContacts()
  } catch (error: any) {
    console.error('Error saving contact:', error)
    alert(`Error al guardar contacto: ${error.message || error}`)
  }
}

const deleteContact = async (contactId: number) => {
  if (!confirm('¿Estás seguro de eliminar este contacto?')) return
  try {
    await contactService.deleteContact(contactId)
    await loadContacts()
  } catch (error: any) {
    console.error('Error deleting contact:', error)
    alert(`Error al eliminar contacto: ${error.message || error}`)
  }
}

// Áreas
const manageBranchAreas = async (branch: Branch) => {
  selectedBranch.value = branch
  showAreasModal.value = true
  try {
    areas.value = await clientService.getBranchAreas(branch.branch_id)
  } catch (error) {
    console.error('Error loading areas:', error)
  }
}

const addArea = async () => {
  if (!newAreaName.value || !selectedBranch.value) return
  try {
    await clientService.createArea(selectedBranch.value.branch_id, {
      branch_id: selectedBranch.value.branch_id,
      name: newAreaName.value
    })
    newAreaName.value = ''
    areas.value = await clientService.getBranchAreas(selectedBranch.value.branch_id)
    await loadBranches()
  } catch (error: any) {
    console.error('Error adding area:', error)
    alert(`Error al agregar área: ${error.message || error}`)
  }
}

const deleteArea = async (areaId: number) => {
  if (!confirm('¿Estás seguro de eliminar esta área?')) return
  try {
    await clientService.deleteArea(areaId)
    if (selectedBranch.value) {
      areas.value = await clientService.getBranchAreas(selectedBranch.value.branch_id)
      await loadBranches()
    }
  } catch (error: any) {
    console.error('Error deleting area:', error)
    alert(`Error al eliminar área: ${error.message || error}`)
  }
}

onMounted(() => {
  loadClient()
})
</script>
