// Configuración base de la API
const API_BASE_URL = 'http://localhost:8000'

// Interceptor para incluir token en las peticiones
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('auth_token')
  
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
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Error desconocido' }))
      throw new Error(errorData.message || `Error ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}

// Enums para equipos
export const EquipmentType = {
  IMPRESORA: 'IMPRESORA',
  COPIADORA: 'COPIADORA',
  MULTIFUNCIONAL: 'MULTIFUNCIONAL',
  ESCANER: 'ESCANER',
  PLOTTER: 'PLOTTER'
}

export const EquipmentStatus = {
  ACTIVO: 'ACTIVO',
  INACTIVO: 'INACTIVO',
  MANTENIMIENTO: 'MANTENIMIENTO',
  FUERA_SERVICIO: 'FUERA_SERVICIO'
}

// Servicio de equipos
export const equipmentService = {
  // CRUD de equipos
  async getEquipment(page = 1, limit = 10, filters = {}) {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    })
    
    // Agregar filtros opcionales
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        params.append(key, filters[key])
      }
    })
    
    return apiRequest(`/api/equipment?${params}`)
  },

  async getEquipmentById(id) {
    return apiRequest(`/api/equipment/${id}`)
  },

  async createEquipment(equipmentData) {
    return apiRequest('/api/equipment', {
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

  async deleteEquipment(id) {
    return apiRequest(`/api/equipment/${id}`, {
      method: 'DELETE'
    })
  },

  async toggleEquipmentStatus(id) {
    return apiRequest(`/api/equipment/${id}/toggle-status`, {
      method: 'PATCH'
    })
  },

  async updateEquipmentStatus(id, status) {
    return apiRequest(`/api/equipment/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    })
  },

  // Métodos de filtrado y búsqueda
  async searchEquipment(query) {
    return apiRequest(`/api/equipment/search?q=${encodeURIComponent(query)}`)
  },

  async getEquipmentByType(type) {
    return apiRequest(`/api/equipment/by-type/${type}`)
  },

  async getEquipmentByStatus(status) {
    return apiRequest(`/api/equipment/by-status/${status}`)
  },

  async getEquipmentByBrand(brandId) {
    return apiRequest(`/api/equipment/by-brand/${brandId}`)
  },

  async getEquipmentByClient(clientName) {
    return apiRequest(`/api/equipment/by-client?client=${encodeURIComponent(clientName)}`)
  },

  // Mantenimiento
  async scheduleMaintenanceMaintenance(id, maintenanceData) {
    return apiRequest(`/api/equipment/${id}/maintenance`, {
      method: 'POST',
      body: JSON.stringify(maintenanceData)
    })
  },

  async getMaintenanceHistory(id) {
    return apiRequest(`/api/equipment/${id}/maintenance-history`)
  },

  async getEquipmentDueMaintenance() {
    return apiRequest('/api/equipment/maintenance-due')
  },

  // CRUD de marcas
  async getBrands() {
    return apiRequest('/api/equipment/brands')
  },

  async getBrandById(id) {
    return apiRequest(`/api/equipment/brands/${id}`)
  },

  async createBrand(brandData) {
    return apiRequest('/api/equipment/brands', {
      method: 'POST',
      body: JSON.stringify(brandData)
    })
  },

  async updateBrand(id, brandData) {
    return apiRequest(`/api/equipment/brands/${id}`, {
      method: 'PUT',
      body: JSON.stringify(brandData)
    })
  },

  async deleteBrand(id) {
    return apiRequest(`/api/equipment/brands/${id}`, {
      method: 'DELETE'
    })
  },

  // CRUD de proveedores
  async getSuppliers() {
    return apiRequest('/api/equipment/suppliers')
  },

  async getSupplierById(id) {
    return apiRequest(`/api/equipment/suppliers/${id}`)
  },

  async createSupplier(supplierData) {
    return apiRequest('/api/equipment/suppliers', {
      method: 'POST',
      body: JSON.stringify(supplierData)
    })
  },

  async updateSupplier(id, supplierData) {
    return apiRequest(`/api/equipment/suppliers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(supplierData)
    })
  },

  async deleteSupplier(id) {
    return apiRequest(`/api/equipment/suppliers/${id}`, {
      method: 'DELETE'
    })
  },

  // Estadísticas y reportes
  async getEquipmentStats() {
    return apiRequest('/api/equipment/stats')
  },

  async getEquipmentByLocation() {
    return apiRequest('/api/equipment/by-location')
  },

  async getWarrantyExpiring(days = 30) {
    return apiRequest(`/api/equipment/warranty-expiring?days=${days}`)
  },

  async getRentalEquipment() {
    return apiRequest('/api/equipment/rentals')
  },

  // Utilidades
  getEquipmentTypeLabel(type) {
    const labels = {
      [EquipmentType.IMPRESORA]: 'Impresora',
      [EquipmentType.COPIADORA]: 'Copiadora',
      [EquipmentType.MULTIFUNCIONAL]: 'Multifuncional',
      [EquipmentType.ESCANER]: 'Escáner',
      [EquipmentType.PLOTTER]: 'Plotter'
    }
    return labels[type] || type
  },

  getEquipmentStatusLabel(status) {
    const labels = {
      [EquipmentStatus.ACTIVO]: 'Activo',
      [EquipmentStatus.INACTIVO]: 'Inactivo',
      [EquipmentStatus.MANTENIMIENTO]: 'En Mantenimiento',
      [EquipmentStatus.FUERA_SERVICIO]: 'Fuera de Servicio'
    }
    return labels[status] || status
  },

  getEquipmentStatusColor(status) {
    const colors = {
      [EquipmentStatus.ACTIVO]: 'text-green-600 bg-green-100',
      [EquipmentStatus.INACTIVO]: 'text-gray-600 bg-gray-100',
      [EquipmentStatus.MANTENIMIENTO]: 'text-yellow-600 bg-yellow-100',
      [EquipmentStatus.FUERA_SERVICIO]: 'text-red-600 bg-red-100'
    }
    return colors[status] || 'text-gray-600 bg-gray-100'
  }
}

export default equipmentService