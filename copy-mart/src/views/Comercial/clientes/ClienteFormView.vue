<template>
  <BaseLayout>
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <button @click="$router.back()" class="text-orange-600 hover:text-orange-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Clientes
        </button>
        <h1 class="text-3xl font-bold text-gray-900">{{ isEditing ? 'Editar' : 'Nuevo' }} Cliente</h1>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Información del Cliente -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Información del Cliente</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre / Razón Social *</label>
              <input v-model="form.name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Comercial</label>
              <input v-model="form.comercial_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">RFC</label>
              <input v-model="form.rfc" type="text" maxlength="13" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
              <input v-model="form.address" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Colonia</label>
              <input v-model="form.colonia" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
              <input v-model="form.zip_code" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
              <input v-model="form.city" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
          </div>
        </div>

        <!-- Contacto Principal -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Contacto Principal</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Contacto</label>
              <input v-model="form.contact_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Rol/Puesto</label>
              <input v-model="form.contact_rol" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
              <input v-model="form.contact_phone" type="tel" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input v-model="form.contact_email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
          </div>
        </div>

        <!-- Sucursal Principal (solo al crear) -->
        <div v-if="!isEditing" class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-gray-900">Sucursal Principal</h2>
            <label class="flex items-center gap-2">
              <input v-model="addBranch" type="checkbox" class="rounded text-orange-600 focus:ring-orange-500" />
              <span class="text-sm text-gray-700">Agregar sucursal</span>
            </label>
          </div>
          <div v-if="addBranch" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de la Sucursal</label>
              <input v-model="branch.name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" placeholder="Ej: Matriz, Sucursal Centro" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
              <input v-model="branch.address" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Colonia</label>
              <input v-model="branch.colonia" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código Postal</label>
              <input v-model="branch.zip_code" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ciudad</label>
              <input v-model="branch.city" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent" />
            </div>
          </div>
        </div>

        <!-- Botones -->
        <div class="flex justify-end gap-3">
          <button type="button" @click="$router.back()" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button type="submit" :disabled="loading" class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50">
            {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear') }} Cliente
          </button>
        </div>
      </form>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import { clientService } from '@/services/clientService'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const addBranch = ref(false)

const form = ref({
  name: '',
  comercial_name: '',
  rfc: '',
  address: '',
  colonia: '',
  zip_code: '',
  city: '',
  contact_name: '',
  contact_phone: '',
  contact_email: '',
  contact_rol: ''
})

const branch = ref({
  name: '',
  address: '',
  colonia: '',
  zip_code: '',
  city: '',
  is_main: true
})

const isEditing = computed(() => !!route.params.id)

const loadClient = async () => {
  if (!isEditing.value) return
  try {
    const client = await clientService.getClientById(Number(route.params.id))
    form.value = {
      name: client.name,
      comercial_name: client.comercial_name || '',
      rfc: client.rfc || '',
      address: client.address || '',
      colonia: client.colonia || '',
      zip_code: client.zip_code || '',
      city: client.city || '',
      contact_name: client.contact?.name || '',
      contact_phone: client.contact?.phone || '',
      contact_email: client.contact?.email || '',
      contact_rol: client.contact?.rol || ''
    }
  } catch (error) {
    console.error('Error loading client:', error)
    alert('Error al cargar el cliente')
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    const payload: any = {
      name: form.value.name,
      comercial_name: form.value.comercial_name || null,
      rfc: form.value.rfc || null,
      address: form.value.address || null,
      colonia: form.value.colonia || null,
      zip_code: form.value.zip_code || null,
      city: form.value.city || null,
      contact_name: form.value.contact_name || null,
      contact_phone: form.value.contact_phone || null,
      contact_email: form.value.contact_email || null,
      contact_rol: form.value.contact_rol || null
    }

    // Agregar sucursal si se marcó el checkbox
    if (!isEditing.value && addBranch.value && branch.value.name) {
      payload.branches = [{
        client_id: 0, // Se asignará en el backend
        name: branch.value.name,
        is_main: true,
        address: branch.value.address || null,
        colonia: branch.value.colonia || null,
        zip_code: branch.value.zip_code || null,
        city: branch.value.city || null
      }]
    }

    if (isEditing.value) {
      await clientService.updateClient(Number(route.params.id), payload)
    } else {
      await clientService.createClient(payload)
    }
    
    router.push({ name: 'Clientes' })
  } catch (error: any) {
    console.error('Error saving client:', error)
    alert(`Error al guardar el cliente: ${error.message || error}`)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadClient()
})
</script>
