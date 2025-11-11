import { computed, ref } from 'vue'

// Definición de todos los módulos del sistema
const ALL_MODULES = [
  { name: 'Dashboard', route: '/dashboard', key: 'dashboard' },
  { name: 'Ventas', route: '/ventas', key: 'ventas' },
  { name: 'Inventario', route: '/inventario', key: 'inventario' },
  { name: 'Clientes', route: '/clientes', key: 'clientes' },
  { name: 'Reportes', route: '/reportes', key: 'reportes' },
  { name: 'Usuarios', route: '/usuarios', key: 'usuarios' }
]

// Permisos por ROL (tiene prioridad sobre departamento)
const ROLE_PERMISSIONS = {
  'administrador': {
    modules: ['dashboard', 'ventas', 'inventario', 'clientes', 'reportes', 'usuarios'],
    canCreate: true,
    canEdit: true,
    canDelete: true
  },
  'gerencia': {
    modules: ['dashboard', 'ventas', 'clientes', 'reportes', 'usuarios'], // Todo MENOS inventario
    canCreate: true,
    canEdit: true,
    canDelete: false
  },
  'usuario': {
    modules: [], // Se define por departamento
    canCreate: false,
    canEdit: false,
    canDelete: false
  }
}

// Permisos por DEPARTAMENTO (aplica solo a usuarios normales)
const DEPARTMENT_PERMISSIONS = {
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
  // Obtener información del usuario desde localStorage
  const getCurrentUser = () => {
    try {
      const userStr = localStorage.getItem('user')
      return userStr ? JSON.parse(userStr) : null
    } catch (error) {
      console.error('Error al obtener usuario:', error)
      return null
    }
  }

  const user = ref(getCurrentUser())

  // Función para actualizar el usuario
  const setUser = (userData) => {
    user.value = userData
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('user')
    }
  }

  // Obtener módulos accesibles según rol y departamento
  const getAccessibleModules = computed(() => {
    if (!user.value) return []

    const rol = user.value.rol?.toLowerCase()
    const department = user.value.department?.toLowerCase()

    // Si es admin o gerencia, usa permisos de ROL
    if (rol === 'administrador' || rol === 'gerencia') {
      const rolePerms = ROLE_PERMISSIONS[rol]
      return ALL_MODULES.filter(module => 
        rolePerms.modules.includes(module.key)
      )
    }

    // Si es usuario normal, usa permisos de DEPARTAMENTO
    if (rol === 'usuario' && department) {
      const deptPerms = DEPARTMENT_PERMISSIONS[department]
      if (deptPerms) {
        return ALL_MODULES.filter(module => 
          deptPerms.modules.includes(module.key)
        )
      }
    }

    return []
  })

  // Verificar si puede acceder a un módulo específico
  const canAccessModule = (moduleKey) => {
    if (!user.value) return false
    
    const accessibleModules = getAccessibleModules.value
    return accessibleModules.some(module => module.key === moduleKey)
  }

  // Verificar si puede acceder a una ruta específica
  const canAccessRoute = (route) => {
    if (!user.value) return false
    
    // Rutas siempre accesibles
    if (['/dashboard', '/perfil', '/'].includes(route)) return true
    
    const accessibleModules = getAccessibleModules.value
    return accessibleModules.some(module => module.route === route)
  }

  // Permisos de acciones (crear, editar, eliminar)
  const canCreate = computed(() => {
    if (!user.value) return false
    const rol = user.value.rol?.toLowerCase()
    return ROLE_PERMISSIONS[rol]?.canCreate || false
  })

  const canEdit = computed(() => {
    if (!user.value) return false
    const rol = user.value.rol?.toLowerCase()
    return ROLE_PERMISSIONS[rol]?.canEdit || false
  })

  const canDelete = computed(() => {
    if (!user.value) return false
    const rol = user.value.rol?.toLowerCase()
    return ROLE_PERMISSIONS[rol]?.canDelete || false
  })

  // Información del usuario
  const userInfo = computed(() => ({
    name: user.value?.full_name || 'Usuario',
    email: user.value?.email || '',
    rol: user.value?.rol || '',
    department: user.value?.department || '',
    initials: user.value?.full_name
      ?.split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase() || 'U'
  }))

  // Verificar si es admin
  const isAdmin = computed(() => {
    return user.value?.rol?.toLowerCase() === 'administrador'
  })

  // Verificar si es gerencia
  const isManager = computed(() => {
    return user.value?.rol?.toLowerCase() === 'gerencia'
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
