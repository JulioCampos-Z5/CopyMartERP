import type { User } from '@/types'

type AccessUser = Partial<User> & {
  role?: string
}

const MODULE_PATTERNS: Record<string, string[]> = {
  dashboard: ['/dashboard', '/perfil'],
  ventas: ['/ventas', '/comercial/ventas'],
  rentas: ['/rentas', '/comercial/rentas'],
  clientes: ['/clientes', '/comercial/clientes'],
  produccion: ['/produccion'],
  compras: ['/compras', '/administracion/compras'],
  almacen: ['/almacen'],
  cobranza: ['/cobranza'],
  facturacion: ['/facturacion', '/administracion/facturacion'],
  inventario: ['/inventario', '/administracion/equipos', '/administracion/refacciones'],
  usuarios: ['/administracion/usuarios'],
  recursos_humanos: ['/recursos-humanos'],
  rutas: ['/rutas'],
  ordenes_servicio: ['/ordenes-servicio'],
  taller: ['/taller'],
  ti: ['/ti']
}

const DEPARTMENT_MODULES: Record<string, string[]> = {
  rh: ['dashboard', 'usuarios', 'recursos_humanos'],
  administracion: ['dashboard', 'ventas', 'rentas', 'compras', 'almacen', 'cobranza', 'facturacion', 'inventario'],
  comercial: ['dashboard', 'ventas', 'rentas', 'clientes', 'produccion', 'cobranza', 'facturacion'],
  operaciones: ['dashboard', 'inventario', 'rutas', 'ordenes_servicio', 'taller']
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
  const allowedModules = new Set<string>(['dashboard'])

  const perms = (user as any)?.permissions
  if (perms && typeof perms === 'object' && !Array.isArray(perms)) {
    for (const [area, actions] of Object.entries(perms)) {
      if (actions && typeof actions === 'object' && (actions as any).view) {
        allowedModules.add(area)
      }
    }
  }

  return Array.from(allowedModules)
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
  const perms = user?.permissions
  if (perms && typeof perms === 'object' && !Array.isArray(perms)) {
    return Object.values(perms).some(actions => 
      actions && typeof actions === 'object' && (actions as any).delete
    )
  }
  return false
}
