/**
 * Configuración centralizada de la API
 * ====================================
 * 
 * Este archivo centraliza la configuración de la API y proporciona
 * utilidades para hacer peticiones HTTP al backend.
 */

import axios from 'axios'

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
  CONTACTS: '/api/contacts'
}

// Cliente Axios con manejo de token y errores
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar Authorization automáticamente
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token && !config.skipAuth) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor de respuesta para normalizar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail || error.message
    const formattedError = new Error(detail || `Error ${status || ''}`.trim())
    formattedError.status = status
    throw formattedError
  }
)

/**
 * Realiza una petición HTTP al backend con axios
 * @param {string} endpoint - Ruta del endpoint (puede usar API_ENDPOINTS)
 * @param {Object} options - Opciones de axios (method, data/body, params, headers)
 * @param {boolean} skipAuth - Si es true, no incluye el token de autenticación
 * @returns {Promise<any>} - Datos de la respuesta
 */
export async function apiRequest(endpoint, options = {}, skipAuth = false) {
  const { body, data, ...rest } = options
  const payload = data ?? (typeof body === 'string' ? JSON.parse(body) : body)

  const response = await apiClient.request({
    url: endpoint,
    method: options.method || 'GET',
    data: payload,
    params: options.params,
    headers: options.headers,
    skipAuth
  })

  return response.data
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
