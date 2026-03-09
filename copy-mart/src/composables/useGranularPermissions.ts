// Composable para gestionar permisos granulares del usuario actual
// Sistema actualizado que usa los permisos JSON de la base de datos
// Uso: const { canView, canCreate, canEdit, canDelete, hasArea } = useGranularPermissions('ventas')

import { ref, computed } from 'vue'
import { API_BASE_URL } from '@/config/api'

export interface UserPermissions {
  [area: string]: {
    view: boolean
    create: boolean
    edit: boolean
    delete: boolean
  }
}

export interface PermissionsResponse {
  user_id: number
  rol: string
  areas: string[]
  permissions: UserPermissions
}

// Estado global de permisos (se carga una vez al iniciar sesión)
const userPermissions = ref<PermissionsResponse | null>(null)
const permissionsLoaded = ref(false)
const permissionsLoading = ref(false)

export function useGranularPermissions(area?: string) {
  // Cargar permisos del usuario actual desde el backend
  async function loadPermissions(token: string, forceReload: boolean = false) {
    if ((permissionsLoaded.value && !forceReload) || permissionsLoading.value) return

    permissionsLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/api/users/me/permissions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        userPermissions.value = await response.json()
        permissionsLoaded.value = true
        console.log('✓ Permisos del usuario cargados:', userPermissions.value)
      } else {
        console.error('Error al cargar permisos:', response.status)
      }
    } catch (error) {
      console.error('Error loading permissions:', error)
    } finally {
      permissionsLoading.value = false
    }
  }

  // Verificar si el usuario tiene acceso a un área
  const hasArea = (areaName: string): boolean => {
    if (!userPermissions.value) return false
    
    return userPermissions.value.areas.includes(areaName)
  }

  // Verificar si tiene un permiso específico
  const hasPermission = (areaName: string, action: 'view' | 'create' | 'edit' | 'delete'): boolean => {
    if (!userPermissions.value) return false
    
    const areaPerms = userPermissions.value.permissions[areaName]
    return areaPerms ? areaPerms[action] === true : false
  }

  // Si se especifica un área, retornar permisos específicos de esa área
  if (area) {
    return {
      canView: computed(() => hasPermission(area, 'view')),
      canCreate: computed(() => hasPermission(area, 'create')),
      canEdit: computed(() => hasPermission(area, 'edit')),
      canDelete: computed(() => hasPermission(area, 'delete')),
      hasArea: computed(() => hasArea(area)),
      loadPermissions,
      permissionsLoaded: computed(() => permissionsLoaded.value),
      permissionsLoading: computed(() => permissionsLoading.value)
    }
  }

  // Si no se especifica área, retornar funciones genéricas
  return {
    hasPermission,
    hasArea,
    userPermissions: computed(() => userPermissions.value),
    permissionsLoaded: computed(() => permissionsLoaded.value),
    permissionsLoading: computed(() => permissionsLoading.value),
    loadPermissions,
    isAdmin: computed(() => userPermissions.value?.rol === 'administrador'),
    availableAreas: computed(() => userPermissions.value?.areas || [])
  }
}

// Hook para resetear permisos (usar al cerrar sesión)
export function resetGranularPermissions() {
  userPermissions.value = null
  permissionsLoaded.value = false
  permissionsLoading.value = false
}

// Ejemplo de uso en un componente:
/*
<script setup lang="ts">
import { useGranularPermissions } from '@/composables/useGranularPermissions'
import { onMounted } from 'vue'

const { canView, canCreate, canEdit, canDelete, loadPermissions } = useGranularPermissions('ventas')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    await loadPermissions(token)
  }
})
</script>

<template>
  <div>
    <button v-if="canCreate" @click="createSale">Nueva Venta</button>
    <button v-if="canEdit" @click="editSale">Editar</button>
    <button v-if="canDelete" @click="deleteSale">Eliminar</button>
  </div>
</template>
*/
