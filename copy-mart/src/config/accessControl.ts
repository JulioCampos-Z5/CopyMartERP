import type { User } from '@/types'

type AccessUser = Partial<User> & {
  role?: string
  permissions?: string[]
}

const MODULE_PATTERNS: Record<string, string[]> = {
  dashboard: ['/dashboard', '/perfil'],
  ventas: ['/ventas', '/comercial/ventas'],
  rentas: ['/rentas', '/comercial/rentas'],
  clientes: ['/clientes', '/comercial/clientes', '/atencion-clientes'],
  produccion: ['/produccion'],
  compras: ['/compras', '/administracion/compras'],
  almacen: ['/almacen'],
  cobranza: ['/cobranza'],
  facturacion: ['/facturacion', '/administracion/facturacion'],
  inventario: ['/inventario', '/administracion/equipos', '/administracion/refacciones'],
  usuarios: ['/administracion/usuarios'],
  rh: ['/recursos-humanos'],
  operaciones: ['/rutas', '/ordenes-servicio'],
  ti: ['/ti']
}

const DEPARTMENT_MODULES: Record<string, string[]> = {
  rh: ['dashboard', 'usuarios', 'rh'],
  administracion: ['dashboard', 'ventas', 'rentas', 'compras', 'almacen', 'cobranza', 'facturacion', 'inventario'],
  comercial: ['dashboard', 'ventas', 'rentas', 'clientes', 'produccion', 'cobranza', 'facturacion'],
  operaciones: ['dashboard', 'inventario', 'operaciones']
}

const ALL_MODULE_KEYS = Object.keys(MODULE_PATTERNS)

export function getStoredUser(): AccessUser | null {
  try {
    const raw = localStorage.getItem('user')
    if (!raw) return null
    return JSON.parse(raw)
  } catch {
    return null
  }
}

export function getUserRole(user: AccessUser | null): string {
  return String(user?.role || user?.rol || '').toLowerCase()
}

export function getUserDepartment(user: AccessUser | null): string {
  return String(user?.department || '').toLowerCase()
}

function routeToModule(path: string): string | null {
  const cleanPath = String(path || '').toLowerCase()
  for (const [moduleKey, patterns] of Object.entries(MODULE_PATTERNS)) {
    if (patterns.some(pattern => cleanPath === pattern || cleanPath.startsWith(`${pattern}/`))) {
      return moduleKey
    }
  }
  return null
}

export function getAllowedModules(user: AccessUser | null): string[] {
  const role = getUserRole(user)
  const department = getUserDepartment(user)

  if (role === 'administrador' || role === 'admin') {
    return ALL_MODULE_KEYS
  }

  if (role === 'gerencia' || role === 'manager') {
    return ALL_MODULE_KEYS.filter(moduleKey => moduleKey !== 'inventario')
  }

  if (role === 'usuario') {
    return DEPARTMENT_MODULES[department] || ['dashboard']
  }

  return []
}

export function canAccessPath(user: AccessUser | null, path: string): boolean {
  if (!path || path === '/' || path === '/login') return true

  const moduleKey = routeToModule(path)
  if (!moduleKey) {
    return true
  }

  const allowedModules = getAllowedModules(user)
  return allowedModules.includes(moduleKey)
}

export function hasDeleteAccess(user: AccessUser | null): boolean {
  const role = getUserRole(user)
  const explicitPermissions = Array.isArray(user?.permissions) ? user?.permissions : []

  if (explicitPermissions.length > 0) {
    return explicitPermissions.some(permission => {
      const normalized = String(permission || '').toLowerCase()
      return normalized === 'delete' || normalized.startsWith('delete_') || normalized === 'admin'
    })
  }

  return role === 'administrador' || role === 'admin'
}
