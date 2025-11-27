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

// Servicio de clientes
export const clientService = {
  // CRUD de clientes principales
  async getClients(skip = 0, limit = 100, isActive = null) {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString()
    })
    
    if (isActive !== null) {
      params.append('is_active', isActive.toString())
    }
    
    return apiRequest(`/api/clients?${params}`)
  },

  async getClientById(id) {
    return apiRequest(`/api/clients/${id}`)
  },

  async createClient(clientData) {
    return apiRequest('/api/clients', {
      method: 'POST',
      body: JSON.stringify(clientData)
    })
  },

  async updateClient(id, clientData) {
    return apiRequest(`/api/clients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clientData)
    })
  },

  async deleteClient(id) {
    return apiRequest(`/api/clients/${id}`, {
      method: 'DELETE'
    })
  },

  async toggleClientStatus(id) {
    return apiRequest(`/api/clients/${id}/toggle-status`, {
      method: 'PATCH'
    })
  },

  // CRUD de sucursales
  async getBranches(clientId) {
    return apiRequest(`/api/clients/${clientId}/branches`)
  },

  async getBranchById(clientId, branchId) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}`)
  },

  async createBranch(clientId, branchData) {
    return apiRequest(`/api/clients/${clientId}/branches`, {
      method: 'POST',
      body: JSON.stringify(branchData)
    })
  },

  async updateBranch(clientId, branchId, branchData) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}`, {
      method: 'PUT',
      body: JSON.stringify(branchData)
    })
  },

  async deleteBranch(clientId, branchId) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}`, {
      method: 'DELETE'
    })
  },

  async setMainBranch(clientId, branchId) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}/set-main`, {
      method: 'PATCH'
    })
  },

  // CRUD de áreas
  async getAreas(clientId, branchId) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}/areas`)
  },

  async getAreaById(clientId, branchId, areaId) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}/areas/${areaId}`)
  },

  async createArea(clientId, branchId, areaData) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}/areas`, {
      method: 'POST',
      body: JSON.stringify(areaData)
    })
  },

  async updateArea(clientId, branchId, areaId, areaData) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}/areas/${areaId}`, {
      method: 'PUT',
      body: JSON.stringify(areaData)
    })
  },

  async deleteArea(clientId, branchId, areaId) {
    return apiRequest(`/api/clients/${clientId}/branches/${branchId}/areas/${areaId}`, {
      method: 'DELETE'
    })
  },

  // CRUD de contactos
  async getContacts(clientId) {
    return apiRequest(`/api/clients/${clientId}/contacts`)
  },

  async getContactById(clientId, contactId) {
    return apiRequest(`/api/clients/${clientId}/contacts/${contactId}`)
  },

  async createContact(clientId, contactData) {
    return apiRequest(`/api/clients/${clientId}/contacts`, {
      method: 'POST',
      body: JSON.stringify(contactData)
    })
  },

  async updateContact(clientId, contactId, contactData) {
    return apiRequest(`/api/clients/${clientId}/contacts/${contactId}`, {
      method: 'PUT',
      body: JSON.stringify(contactData)
    })
  },

  async deleteContact(clientId, contactId) {
    return apiRequest(`/api/clients/${clientId}/contacts/${contactId}`, {
      method: 'DELETE'
    })
  },

  async setPrimaryContact(clientId, contactId) {
    return apiRequest(`/api/clients/${clientId}/contacts/${contactId}/set-primary`, {
      method: 'PATCH'
    })
  },

  // Métodos de búsqueda y filtros
  async searchClients(query) {
    return apiRequest(`/api/clients/search?q=${encodeURIComponent(query)}`)
  },

  async getClientsByIndustry(industry) {
    return apiRequest(`/api/clients/by-industry/${encodeURIComponent(industry)}`)
  },

  async getActiveClients() {
    return apiRequest('/api/clients?active=true')
  },

  // Métodos para dashboard/estadísticas
  async getClientStats() {
    return apiRequest('/api/clients/stats')
  },

  async getClientSummary(id) {
    return apiRequest(`/api/clients/${id}/summary`)
  }
}

export default clientService