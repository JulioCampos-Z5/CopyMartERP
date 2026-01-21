/**
 * Composable: Permissions (TypeScript)
 * =====================================
 * Sistema de permisos basado en roles y departamentos
 */

import { computed, ref } from 'vue'
import type { User } from '@/types'

interface Module {
  name: string
  route: string
  key: string
}

interface RolePermissions {
  modules: string[]
  canCreate: boolean
  canEdit: boolean
  canDelete: boolean
}

interface DepartmentPermissions {
  modules: string[]
}

// Definición de todos los módulos del sistema
const ALL_MODULES: Module[] = [
  { name: 'Dashboard', route: '/dashboard', key: 'dashboard' },
  { name: 'Ventas', route: '/ventas', key: 'ventas' },
  { name: 'Inventario', route: '/inventario', key: 'inventario' },
  { name: 'Clientes', route: '/clientes', key: 'clientes' },
  { name: 'Reportes', route: '/reportes', key: 'reportes' },
  { name: 'Usuarios', route: '/usuarios', key: 'usuarios' }
]

// Permisos por ROL (tiene prioridad sobre departamento)
const ROLE_PERMISSIONS: Record<string, RolePermissions> = {
  'administrador': {
    modules: ['dashboard', 'ventas', 'inventario', 'clientes', 'reportes', 'usuarios'],
    canCreate: true,
    canEdit: true,
    canDelete: true
  },
  'gerencia': {
    modules: ['dashboard', 'ventas', 'clientes', 'reportes', 'usuarios'],
    canCreate: true,
    canEdit: true,
    canDelete: false
  },
  'usuario': {
    modules: [],
    canCreate: false,
    canEdit: false,
    canDelete: false
  }
}

// Permisos por DEPARTAMENTO (aplica solo a usuarios normales)
const DEPARTMENT_PERMISSIONS: Record<string, DepartmentPermissions> = {
  'rh': {
    modules: ['dashboard', 'usuarios']
  },
  'administracion': {
    modules: ['dashboard', 'ventas', 'inventario', 'reportes']
  },
  'comercial': {
    modules: ['dashboard', 'ventas', 'clientes', 'reportes']
  },
  'operaciones': {
    modules: ['dashboard', 'inventario']
  }
}

export function usePermissions() {
  const user = ref<User | null>(null)

  // Cargar usuario desde localStorage
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser)
    } catch (error) {
      console.error('Error parsing user from localStorage:', error)
    }
  }

  const setUser = (newUser: User | null) => {
    user.value = newUser
  }

  // Obtener módulos accesibles según rol y departamento
  const getAccessibleModules = computed<Module[]>(() => {
    if (!user.value) return []
    
    const rol = user.value.role?.toLowerCase()
    const department = user.value.department?.toLowerCase()
    
    let allowedModuleKeys: string[] = []
    
    // 1. Primero verificar permisos por rol
    if (rol && ROLE_PERMISSIONS[rol]) {
      allowedModuleKeys = ROLE_PERMISSIONS[rol].modules
    }
    
    // 2. Si es usuario normal, verificar permisos por departamento
    if (rol === 'usuario' && department && DEPARTMENT_PERMISSIONS[department]) {
      allowedModuleKeys = DEPARTMENT_PERMISSIONS[department].modules
    }
    
    // 3. Filtrar módulos permitidos
    return ALL_MODULES.filter(module => allowedModuleKeys.includes(module.key))
  })

  // Verificar si puede acceder a un módulo específico
  const canAccessModule = (moduleKey: string): boolean => {
    if (!user.value) return false
    
    const accessibleModules = getAccessibleModules.value
    return accessibleModules.some(module => module.key === moduleKey)
  }

  // Verificar si puede acceder a una ruta específica
  const canAccessRoute = (route: string): boolean => {
    if (!user.value) return false
    
    // Rutas siempre accesibles
    if (['/dashboard', '/perfil', '/'].includes(route)) return true
    
    const accessibleModules = getAccessibleModules.value
    return accessibleModules.some(module => module.route === route)
  }

  // Permisos de acciones (crear, editar, eliminar)
  const canCreate = computed(() => {
    if (!user.value) return false
    const rol = user.value.role?.toLowerCase()
    return ROLE_PERMISSIONS[rol]?.canCreate || false
  })

  const canEdit = computed(() => {
    if (!user.value) return false
    const rol = user.value.role?.toLowerCase()
    return ROLE_PERMISSIONS[rol]?.canEdit || false
  })

  const canDelete = computed(() => {
    if (!user.value) return false
    const rol = user.value.role?.toLowerCase()
    return ROLE_PERMISSIONS[rol]?.canDelete || false
  })

  // Información del usuario
  const userInfo = computed(() => ({
    name: user.value?.full_name || 'Usuario',
    email: user.value?.email || '',
    role: user.value?.role || '',
    department: user.value?.department || '',
    initials: user.value?.full_name
      ?.split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase() || 'U'
  }))

  // Verificar si es admin
  const isAdmin = computed(() => {
    return user.value?.role?.toLowerCase() === 'administrador'
  })

  // Verificar si es gerencia
  const isManager = computed(() => {
    return user.value?.role?.toLowerCase() === 'gerencia'
  })

  return {
    user,
    setUser,
    getAccessibleModules,
    canAccessModule,
    canAccessRoute,
    canCreate,
    canEdit,
    canDelete,
    userInfo,
    isAdmin,
    isManager
  }
}
