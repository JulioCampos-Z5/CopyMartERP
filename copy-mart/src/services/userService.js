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

// Servicio de usuarios y autenticación
export const userService = {
  // Autenticación
  async login(credentials) {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    
    const response = await fetch(`${API_BASE_URL}/token`, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('Credenciales incorrectas')
    }
    
    const data = await response.json()
    localStorage.setItem('auth_token', data.access_token)
    localStorage.setItem('user_data', JSON.stringify(data.user))
    return data
  },

  async logout() {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
  },

  async getCurrentUser() {
    return apiRequest('/users/me')
  },

  // CRUD de usuarios
  async getUsers(page = 1, limit = 10) {
    return apiRequest(`/users?page=${page}&limit=${limit}`)
  },

  async getUserById(id) {
    return apiRequest(`/users/${id}`)
  },

  async createUser(userData) {
    return apiRequest('/users', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  },

  async updateUser(id, userData) {
    return apiRequest(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData)
    })
  },

  async deleteUser(id) {
    return apiRequest(`/users/${id}`, {
      method: 'DELETE'
    })
  },

  async changePassword(currentPassword, newPassword) {
    return apiRequest('/users/change-password', {
      method: 'POST',
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    })
  },

  // Utilidades de autenticación
  isAuthenticated() {
    return !!localStorage.getItem('auth_token')
  },

  getUserData() {
    const userData = localStorage.getItem('user_data')
    return userData ? JSON.parse(userData) : null
  },

  hasRole(requiredRole) {
    const user = this.getUserData()
    if (!user) return false
    
    const roleHierarchy = {
      'EMPLEADO': 1,
      'GERENTE': 2,
      'ADMIN': 3
    }
    
    return roleHierarchy[user.role] >= roleHierarchy[requiredRole]
  }
}

export default userService