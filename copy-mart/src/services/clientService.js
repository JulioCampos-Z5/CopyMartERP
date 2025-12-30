import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

// Servicio de clientes
export const clientService = {
  // CRUD de clientes principales
  async getClients(skip = 0, limit = 100, isActive = null) {
    const params = { skip, limit }
    if (isActive !== null) params.is_active = isActive
    
    const url = buildUrlWithParams(API_ENDPOINTS.CLIENTS, params)
    return apiRequest(url)
  },

  async getClientById(id) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${id}`)
  },

  async createClient(clientData) {
    return apiRequest(API_ENDPOINTS.CLIENTS, {
      method: 'POST',
      body: JSON.stringify(clientData)
    })
  },

  async updateClient(id, clientData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clientData)
    })
  },

  async deleteClient(id) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${id}`, {
      method: 'DELETE'
    })
  },

  async toggleClientStatus(id) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${id}/toggle-status`, {
      method: 'PATCH'
    })
  },

  // CRUD de sucursales
  async getBranches(clientId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches`)
  },

  async getBranchById(clientId, branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}`)
  },

  async createBranch(clientId, branchData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches`, {
      method: 'POST',
      body: JSON.stringify(branchData)
    })
  },

  async updateBranch(clientId, branchId, branchData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}`, {
      method: 'PUT',
      body: JSON.stringify(branchData)
    })
  },

  async deleteBranch(clientId, branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}`, {
      method: 'DELETE'
    })
  },

  async setMainBranch(clientId, branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}/set-main`, {
      method: 'PATCH'
    })
  },

  // CRUD de áreas
  async getAreas(clientId, branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}/areas`)
  },

  async getAreaById(clientId, branchId, areaId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}/areas/${areaId}`)
  },

  async createArea(clientId, branchId, areaData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}/areas`, {
      method: 'POST',
      body: JSON.stringify(areaData)
    })
  },

  async updateArea(clientId, branchId, areaId, areaData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}/areas/${areaId}`, {
      method: 'PUT',
      body: JSON.stringify(areaData)
    })
  },

  async deleteArea(clientId, branchId, areaId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches/${branchId}/areas/${areaId}`, {
      method: 'DELETE'
    })
  },

  // CRUD de contactos
  async getContacts(clientId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/contacts`)
  },

  async getContactById(clientId, contactId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/contacts/${contactId}`)
  },

  async createContact(clientId, contactData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/contacts`, {
      method: 'POST',
      body: JSON.stringify(contactData)
    })
  },

  async updateContact(clientId, contactId, contactData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/contacts/${contactId}`, {
      method: 'PUT',
      body: JSON.stringify(contactData)
    })
  },

  async deleteContact(clientId, contactId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/contacts/${contactId}`, {
      method: 'DELETE'
    })
  },

  async setPrimaryContact(clientId, contactId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/contacts/${contactId}/set-primary`, {
      method: 'PATCH'
    })
  },

  // Métodos de búsqueda y filtros
  async searchClients(query) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/search?q=${encodeURIComponent(query)}`)
  },

  async getClientsByIndustry(industry) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/by-industry/${encodeURIComponent(industry)}`)
  },

  async getActiveClients() {
    const url = buildUrlWithParams(API_ENDPOINTS.CLIENTS, { active: true })
    return apiRequest(url)
  },

  // Métodos para dashboard/estadísticas
  async getClientStats() {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/stats`)
  },

  async getClientSummary(id) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${id}/summary`)
  }
}

export default clientService