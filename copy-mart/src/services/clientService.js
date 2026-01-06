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
      method: 'PATCH',
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

  async getBranchById(branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}`)
  },

  async createBranch(clientId, branchData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches`, {
      method: 'POST',
      body: JSON.stringify({ ...branchData, client_id: clientId })
    })
  },

  async updateBranch(branchId, branchData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}`, {
      method: 'PATCH',
      body: JSON.stringify(branchData)
    })
  },

  async deleteBranch(branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}`, {
      method: 'DELETE'
    })
  },

  // CRUD de áreas
  async getAreas(branchId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}/areas`)
  },

  async getAreaById(areaId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/areas/${areaId}`)
  },

  async createArea(branchId, areaData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}/areas`, {
      method: 'POST',
      body: JSON.stringify({ ...areaData, branch_id: branchId })
    })
  },

  async updateArea(areaId, areaData) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/areas/${areaId}`, {
      method: 'PATCH',
      body: JSON.stringify(areaData)
    })
  },

  async deleteArea(areaId) {
    return apiRequest(`${API_ENDPOINTS.CLIENTS}/areas/${areaId}`, {
      method: 'DELETE'
    })
  }
}

export default clientService