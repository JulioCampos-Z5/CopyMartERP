import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

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
    const url = `${API_ENDPOINTS.EQUIPMENT}/`
    return apiRequest(url)
  },

  async getEquipmentById(id) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}`)
  },

  async createEquipment(equipmentData) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/`, {
      method: 'POST',
      body: JSON.stringify(equipmentData)
    })
  },

  async updateEquipment(id, equipmentData) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(equipmentData)
    })
  },

  async deleteEquipment(id) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}/`, {
      method: 'DELETE'
    })
  },

  async toggleEquipmentStatus(id) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}/toggle-status`, {
      method: 'PATCH'
    })
  },

  async updateEquipmentStatus(id, status) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ location_status: status })
    })
  },

  // Métodos de filtrado y búsqueda
  async searchEquipment(query) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/search?q=${encodeURIComponent(query)}`)
  },

  async getEquipmentByType(type) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/by-type/${type}`)
  },

  async getEquipmentByStatus(status) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/by-status/${status}`)
  },

  async getEquipmentByBrand(brandId) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/by-brand/${brandId}`)
  },

  async getEquipmentByClient(clientName) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/by-client?client=${encodeURIComponent(clientName)}`)
  },

  // Mantenimiento
  async scheduleMaintenanceMaintenance(id, maintenanceData) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}/maintenance`, {
      method: 'POST',
      body: JSON.stringify(maintenanceData)
    })
  },

  async getMaintenanceHistory(id) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/${id}/maintenance-history`)
  },

  async getEquipmentDueMaintenance() {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/maintenance-due`)
  },

  // CRUD de marcas
  async getBrands() {
    return apiRequest(`${API_ENDPOINTS.BRANDS}/`)
  },

  async getBrandById(id) {
    return apiRequest(`${API_ENDPOINTS.BRANDS}/${id}/`)
  },

  async createBrand(brandData) {
    return apiRequest(`${API_ENDPOINTS.BRANDS}/`, {
      method: 'POST',
      body: JSON.stringify(brandData)
    })
  },

  async updateBrand(id, brandData) {
    return apiRequest(`${API_ENDPOINTS.BRANDS}/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(brandData)
    })
  },

  async deleteBrand(id) {
    return apiRequest(`${API_ENDPOINTS.BRANDS}/${id}/`, {
      method: 'DELETE'
    })
  },

  // CRUD de proveedores
  async getSuppliers() {
    return apiRequest(`${API_ENDPOINTS.SUPPLIERS}/`)
  },

  async getSupplierById(id) {
    return apiRequest(`${API_ENDPOINTS.SUPPLIERS}/${id}/`)
  },

  async createSupplier(supplierData) {
    return apiRequest(`${API_ENDPOINTS.SUPPLIERS}/`, {
      method: 'POST',
      body: JSON.stringify(supplierData)
    })
  },

  async updateSupplier(id, supplierData) {
    return apiRequest(`${API_ENDPOINTS.SUPPLIERS}/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(supplierData)
    })
  },

  async deleteSupplier(id) {
    return apiRequest(`${API_ENDPOINTS.SUPPLIERS}/${id}/`, {
      method: 'DELETE'
    })
  },

  // Estadísticas y reportes
  async getEquipmentStats() {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/stats`)
  },

  async getEquipmentByLocation() {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/by-location`)
  },

  async getWarrantyExpiring(days = 30) {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/warranty-expiring?days=${days}`)
  },

  async getRentalEquipment() {
    return apiRequest(`${API_ENDPOINTS.EQUIPMENT}/rentals`)
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