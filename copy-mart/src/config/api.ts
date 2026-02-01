/**
 * Configuración centralizada de la API
 * ====================================
 * 
 * Este archivo centraliza la configuración de la API y proporciona
 * utilidades para hacer peticiones HTTP al backend.
 */

import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import type { ApiError } from '@/types'

// URL base del backend
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Endpoints de la API (prefijos de los routers del backend)
export const API_ENDPOINTS = {
  // Autenticación y usuarios - Prefijo: /api/users
  AUTH: '/api/users',
  
  // Clientes y relaciones - Prefijo: /api/clients
  CLIENTS: '/api/clients',
  
  // Equipos - La ruta completa es /api/equipment/equipment/
  EQUIPMENT: '/api/equipment/equipment',
  
  // Marcas de equipos - /api/equipment/brands
  BRANDS: '/api/equipment/brands',
  
  // Proveedores de equipos - /api/equipment/suppliers
  SUPPLIERS: '/api/equipment/suppliers',
  
  // Rentas - Prefijo: /api/rents
  RENTS: '/api/rents',
  
  // Ventas - Prefijo: /api/sales
  SALES: '/api/sales',
  
  // Facturación - Prefijo: /api/billings
  BILLINGS: '/api/billings',
  
  // Contactos - Prefijo: /api/contacts
  CONTACTS: '/api/contacts',
  
  // Compras - Prefijo: /api/purchases
  PURCHASES: '/api/purchases',
  
  // Refacciones - Prefijo: /api/spareparts
  SPAREPARTS: '/api/spareparts',
  
  // Inventario - Catálogo de items
  CATALOG: '/api/catalog',
  
  // Inventario - Instancias de inventario
  INVENTORY: '/api/inventory',
  
  // Inventario - Estantes
  SHELVES: '/api/shelves'
} as const

interface ApiRequestConfig extends AxiosRequestConfig {
  skipAuth?: boolean
}

// Cliente Axios con manejo de token y errores
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar Authorization automáticamente
apiClient.interceptors.request.use((config: any) => {
  const token = localStorage.getItem('token')
  if (token && !config.skipAuth) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor de respuesta para normalizar errores
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: any) => {
    const status = error.response?.status
    let detail = error.response?.data?.detail || error.message
    
    // Si detail es un array u objeto, convertirlo a string legible
    if (typeof detail === 'object') {
      if (Array.isArray(detail)) {
        detail = detail.map(err => err.msg || err.message || JSON.stringify(err)).join(', ')
      } else {
        detail = JSON.stringify(detail, null, 2)
      }
    }
    
    // Si recibimos un 401, redirigir al login
    if (status === 401) {
      // Limpiar autenticación
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
      
      // Redirigir al login si no estamos ya en esa ruta
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    
    const formattedError: ApiError & Error = new Error(detail || `Error ${status || ''}`.trim()) as any
    formattedError.status = status
    formattedError.detail = detail
    throw formattedError
  }
)

/**
 * Realiza una petición HTTP al backend con axios
 * @param endpoint - Ruta del endpoint (puede usar API_ENDPOINTS)
 * @param options - Opciones de axios (method, data/body, params, headers)
 * @param skipAuth - Si es true, no incluye el token de autenticación
 * @returns Datos de la respuesta
 */
export async function apiRequest<T = any>(
  endpoint: string, 
  options: ApiRequestConfig = {}, 
  skipAuth: boolean = false
): Promise<T> {
  try {
    // Normalizar data/body
    const { data, body, ...restOptions } = options
    const payload = data || body

    const config: ApiRequestConfig = {
      url: endpoint,
      method: options.method || 'GET',
      ...(payload && { data: payload }),
      ...restOptions,
      skipAuth
    }

    const response = await apiClient.request<T>(config)
    return response.data
  } catch (error: any) {
    console.error(`API Request Error [${options.method || 'GET'}] ${endpoint}:`, error)
    throw error
  }
}

/**
 * Construye una URL con parámetros de query
 * @param baseUrl - URL base
 * @param params - Objeto con parámetros
 * @returns URL con query string
 */
export function buildUrlWithParams(baseUrl: string, params: Record<string, any> = {}): string {
  const filteredParams = Object.entries(params).reduce((acc, [key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      acc[key] = value
    }
    return acc
  }, {} as Record<string, any>)

  const queryString = new URLSearchParams(
    Object.entries(filteredParams).map(([key, value]) => [key, String(value)])
  ).toString()
  
  return queryString ? `${baseUrl}?${queryString}` : baseUrl
}

/**
 * GET request helper
 */
export async function apiGet<T = any>(endpoint: string, params?: Record<string, any>): Promise<T> {
  const url = params ? buildUrlWithParams(endpoint, params) : endpoint
  return apiRequest<T>(url, { method: 'GET' })
}

/**
 * POST request helper
 */
export async function apiPost<T = any>(endpoint: string, data: any): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'POST', data })
}

/**
 * PUT request helper
 */
export async function apiPut<T = any>(endpoint: string, data: any): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PUT', data })
}

/**
 * PATCH request helper
 */
export async function apiPatch<T = any>(endpoint: string, data: any): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PATCH', data })
}

/**
 * DELETE request helper
 */
export async function apiDelete<T = any>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'DELETE' })
}

/**
 * Utilidades para manejo de autenticación en localStorage
 */
export const authStorage = {
  setToken(token: string): void {
    localStorage.setItem('token', token)
  },
  
  getToken(): string | null {
    return localStorage.getItem('token')
  },
  
  removeToken(): void {
    localStorage.removeItem('token')
  },
  
  isAuthenticated(): boolean {
    return !!this.getToken()
  },
  
  setUser(user: any): void {
    localStorage.setItem('user', JSON.stringify(user))
  },
  
  getUser(): any {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },
  
  removeUser(): void {
    localStorage.removeItem('user')
  },
  
  clearAuth(): void {
    this.removeToken()
    this.removeUser()
    localStorage.removeItem('isAuthenticated')
  }
}

export default apiClient
