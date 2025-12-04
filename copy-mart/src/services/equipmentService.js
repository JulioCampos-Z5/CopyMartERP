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
    
    // Para DELETE que retorna 204
    if (response.status === 204) {
      return true
    }
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Error desconocido' }))
      throw new Error(errorData.detail || errorData.message || `Error ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}

// Enums para equipos (deben coincidir con el backend)
export const TypeColor = {
  MONOCROMO: 'monocromo',
  COLOR: 'color'
}

export const LocationStatus = {
  BODEGA: 'bodega',
  ASIGNADO: 'asignado',
  VENDIDO: 'vendido',
  TALLER: 'taller',
  DESCONOCIDO: 'desconocido'
}

// Servicio de equipos
export const equipmentService = {
  // CRUD de equipos
  async getEquipment() {
    return apiRequest('/api/equipment/')
  },

  async getEquipmentById(id) {
    return apiRequest(`/api/equipment/${id}`)
  },

  async createEquipment(equipmentData) {
    return apiRequest('/api/equipment/', {
      method: 'POST',
      body: JSON.stringify(equipmentData)
    })
  },

  async updateEquipment(id, equipmentData) {
    return apiRequest(`/api/equipment/${id}`, {
      method: 'PUT',
      body: JSON.stringify(equipmentData)
    })
  },

  async updateEquipmentStatus(id, status) {
    return apiRequest(`/api/equipment/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ location_status: status })
    })
  },

  async deleteEquipment(id) {
    return apiRequest(`/api/equipment/${id}`, {
      method: 'DELETE'
    })
  },

  // CRUD de marcas
  async getBrands() {
    return apiRequest('/api/equipment/brands/')
  },

  async createBrand(brandData) {
    return apiRequest('/api/equipment/brands/', {
      method: 'POST',
      body: JSON.stringify(brandData)
    })
  },

  // CRUD de proveedores
  async getSuppliers() {
    return apiRequest('/api/equipment/suppliers/')
  },

  async createSupplier(supplierData) {
    return apiRequest('/api/equipment/suppliers/', {
      method: 'POST',
      body: JSON.stringify(supplierData)
    })
  },

  // Utilidades
  getTypeLabel(type) {
    const labels = {
      [TypeColor.MONOCROMO]: 'Monocromo',
      [TypeColor.COLOR]: 'Color'
    }
    return labels[type] || type
  },

  getLocationStatusLabel(status) {
    const labels = {
      [LocationStatus.BODEGA]: 'En Bodega',
      [LocationStatus.ASIGNADO]: 'Asignado',
      [LocationStatus.VENDIDO]: 'Vendido',
      [LocationStatus.TALLER]: 'En Taller',
      [LocationStatus.DESCONOCIDO]: 'Desconocido'
    }
    return labels[status] || status
  },

  getLocationStatusColor(status) {
    const colors = {
      [LocationStatus.BODEGA]: 'text-blue-600 bg-blue-100',
      [LocationStatus.ASIGNADO]: 'text-green-600 bg-green-100',
      [LocationStatus.VENDIDO]: 'text-purple-600 bg-purple-100',
      [LocationStatus.TALLER]: 'text-yellow-600 bg-yellow-100',
      [LocationStatus.DESCONOCIDO]: 'text-gray-600 bg-gray-100'
    }
    return colors[status] || 'text-gray-600 bg-gray-100'
  }
}

export default equipmentService