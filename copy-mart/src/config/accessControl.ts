import type { User } from '@/types'

type AccessUser = Partial<User> & {
  role?: string
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
  operaciones: ['/rutas', '/ordenes-servicio', '/taller'],
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

  // Base modules from department
  let baseModules: string[]

  if (role === 'gerencia' || role === 'manager') {
    baseModules = ALL_MODULE_KEYS.filter(moduleKey => moduleKey !== 'inventario')
  } else if (role === 'usuario') {
    baseModules = DEPARTMENT_MODULES[department] || ['dashboard']
  } else {
    return []
  }

  // If user has granular permissions, further restrict to only areas with view=true
  const perms = (user as any)?.permissions
  if (perms && typeof perms === 'object' && !Array.isArray(perms) && Object.keys(perms).length > 0) {
    const allowedAreas = new Set<string>(['dashboard'])
    for (const [area, actions] of Object.entries(perms)) {
      if (actions && typeof actions === 'object' && (actions as any).view) {
        allowedAreas.add(area)
      }
    }
    // Map permission areas to module keys (most are 1:1 except some)
    const AREA_TO_MODULE: Record<string, string> = {
      ventas: 'ventas',
      rentas: 'rentas',
      clientes: 'clientes',
      compras: 'compras',
      almacen: 'almacen',
      cobranza: 'cobranza',
      facturacion: 'facturacion',
      inventario: 'inventario',
      produccion: 'produccion',
      ordenes_servicio: 'operaciones',
      recursos_humanos: 'rh',
      usuarios: 'usuarios'
    }
    const allowedModules = new Set<string>(['dashboard'])
    for (const area of allowedAreas) {
      const moduleKey = AREA_TO_MODULE[area] || area
      allowedModules.add(moduleKey)
    }
    return baseModules.filter(m => allowedModules.has(m))
  }

  return baseModules
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

  if (role === 'administrador' || role === 'admin') {
    return true
  }

  // Check if any area has delete=true in granular permissions
  const perms = user?.permissions
  if (perms && typeof perms === 'object' && !Array.isArray(perms)) {
    return Object.values(perms).some(actions => 
      actions && typeof actions === 'object' && (actions as any).delete
    )
  }

  return false
}
