/**
 * Configuración centralizada de la API
 * ====================================
 * 
 * Este archivo centraliza la configuración de la API y proporciona
 * utilidades para hacer peticiones HTTP al backend.
 */

// URL base del backend
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Endpoints de la API (prefijos de los routers del backend)
export const API_ENDPOINTS = {
  // Autenticación y usuarios - Prefijo: /api/users
  AUTH: '/api/users',
  
  // Clientes y relaciones - Prefijo: /api/clients
  CLIENTS: '/api/clients',
  
  // Equipos - La ruta completa es /api/equipment/equipment/equipment/
  EQUIPMENT: '/api/equipment/equipment/equipment',
  
  // Marcas de equipos - /api/equipment/equipment/brands
  BRANDS: '/api/equipment/equipment/brands',
  
  // Proveedores de equipos - /api/equipment/equipment/suppliers
  SUPPLIERS: '/api/equipment/equipment/suppliers',
  
  // Rentas - Prefijo: /api/rents
  RENTS: '/api/rents',
  
  // Ventas - Prefijo: /api/sales
  SALES: '/api/sales',
  
  // Facturación - Prefijo: /api/billings
  BILLINGS: '/api/billings',
  
  // Contactos - Prefijo: /api/contacts
  CONTACTS: '/api/contacts'
}

/**
 * Realiza una petición HTTP al backend con autenticación automática
 * @param {string} endpoint - Ruta del endpoint (puede usar API_ENDPOINTS)
 * @param {Object} options - Opciones de fetch (method, body, headers, etc.)
 * @param {boolean} skipAuth - Si es true, no incluye el token de autenticación
 * @returns {Promise<any>} - Respuesta JSON del servidor
 */
export async function apiRequest(endpoint, options = {}, skipAuth = false) {
  const token = localStorage.getItem('token')
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  }
  
  // Añadir token de autenticación si está disponible y no se omite
  if (token && !skipAuth) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  try {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, config)
    
    // Manejar errores HTTP
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ 
        detail: `Error ${response.status}: ${response.statusText}` 
      }))
      
      // Lanzar error con el mensaje del servidor o mensaje por defecto
      throw new Error(errorData.detail || errorData.message || `Error ${response.status}`)
    }
    
    // Si la respuesta es 204 No Content, no hay body que parsear
    if (response.status === 204) {
      return null
    }
    
    return await response.json()
  } catch (error) {
    // Log del error para debugging
    console.error('API Request Error:', {
      endpoint,
      error: error.message,
      options
    })
    
    // Re-lanzar el error para que el llamador lo maneje
    throw error
  }
}

/**
 * Construye una URL con query parameters
 * @param {string} baseUrl - URL base
 * @param {Object} params - Objeto con los parámetros
 * @returns {string} - URL con query string
 */
export function buildUrlWithParams(baseUrl, params = {}) {
  const filteredParams = Object.entries(params)
    .filter(([_, value]) => value !== null && value !== undefined && value !== '')
    .reduce((acc, [key, value]) => {
      acc[key] = value
      return acc
    }, {})
  
  const queryString = new URLSearchParams(filteredParams).toString()
  return queryString ? `${baseUrl}?${queryString}` : baseUrl
}

/**
 * Manejo de tokens
 */
export const authStorage = {
  setToken(token) {
    localStorage.setItem('token', token)
  },
  
  getToken() {
    return localStorage.getItem('token')
  },
  
  removeToken() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  },
  
  isAuthenticated() {
    return !!this.getToken()
  }
}

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  apiRequest,
  buildUrlWithParams,
  authStorage
}
