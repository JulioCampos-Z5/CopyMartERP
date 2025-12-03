// Configuración base de la API
const API_BASE_URL = 'http://localhost:8000'

// Interceptor para incluir token en las peticiones
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token')
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  }
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
    
    // Si es 401, limpiar sesión y redirigir al login
    if (response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
      window.location.href = '/login'
      throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.')
    }
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Error desconocido' }))
      throw new Error(errorData.detail || errorData.message || `Error ${response.status}`)
    }
    
    // Para DELETE que no devuelve contenido
    if (response.status === 204) {
      return null
    }
    
    return await response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}

const rentService = {
  // Obtener todas las rentas con filtros opcionales
  async getRents(filters = {}) {
    const params = new URLSearchParams()
    
    if (filters.client_id) params.append('client_id', filters.client_id)
    if (filters.branch_id) params.append('branch_id', filters.branch_id)
    if (filters.area_id) params.append('area_id', filters.area_id)
    if (filters.contract_status) params.append('contract_status', filters.contract_status)
    if (filters.is_foreign !== undefined) params.append('is_foreign', filters.is_foreign)
    if (filters.is_active !== undefined) params.append('is_active', filters.is_active)
    if (filters.skip) params.append('skip', filters.skip)
    if (filters.limit) params.append('limit', filters.limit)
    
    const queryString = params.toString()
    const url = queryString ? `/rents?${queryString}` : '/rents'
    
    return apiRequest(url)
  },

  // Obtener una renta por ID
  async getRent(rentId) {
    return apiRequest(`/rents/${rentId}`)
  },

  // Crear una nueva renta
  async createRent(rentData) {
    return apiRequest('/rents/', {
      method: 'POST',
      body: JSON.stringify(rentData)
    })
  },

  // Actualizar una renta
  async updateRent(rentId, rentData) {
    return apiRequest(`/rents/${rentId}`, {
      method: 'PUT',
      body: JSON.stringify(rentData)
    })
  },

  // Eliminar (desactivar) una renta
  async deleteRent(rentId) {
    return apiRequest(`/rents/${rentId}`, {
      method: 'DELETE'
    })
  },

  // Actualizar estado del contrato
  async updateContractStatus(rentId, newStatus) {
    return apiRequest(`/rents/${rentId}/status?new_status=${newStatus}`, {
      method: 'PATCH'
    })
  },

  // Obtener resumen de rentas por cliente
  async getClientRentSummary(clientId) {
    return apiRequest(`/rents/client/${clientId}/summary`)
  }
}

export default rentService
