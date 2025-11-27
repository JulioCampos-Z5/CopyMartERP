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

// Servicio de usuarios y autenticación
export const userService = {
  // Autenticación
  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password
      })
    })
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Credenciales incorrectas' }))
      throw new Error(error.detail || 'Credenciales incorrectas')
    }
    
    const data = await response.json()
    
    // Guardar token
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('isAuthenticated', 'true')
    
    // Obtener datos completos del usuario
    try {
      const userResponse = await fetch(`${API_BASE_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${data.access_token}`
        }
      })
      
      if (userResponse.ok) {
        const userData = await userResponse.json()
        localStorage.setItem('user', JSON.stringify(userData))
      } else {
        // Fallback si no se puede obtener el usuario
        const userData = {
          email: credentials.email,
          full_name: 'Usuario',
          role: 'user'
        }
        localStorage.setItem('user', JSON.stringify(userData))
      }
    } catch (error) {
      console.error('Error getting user data:', error)
      // Fallback
      const userData = {
        email: credentials.email,
        full_name: 'Usuario',
        role: 'user'
      }
      localStorage.setItem('user', JSON.stringify(userData))
    }
    
    return data
  },

  async logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
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

  async changePassword(userId, currentPassword, newPassword) {
    return apiRequest(`/users/${userId}/password`, {
      method: 'PUT',
      body: JSON.stringify({
        old_password: currentPassword,
        new_password: newPassword
      })
    })
  },

  async changeEmail(userId, newEmail) {
    return apiRequest(`/users/${userId}/email`, {
      method: 'PUT',
      body: JSON.stringify({
        new_email: newEmail
      })
    })
  },

  // Utilidades de autenticación
  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  getUserData() {
    const userData = localStorage.getItem('user')
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