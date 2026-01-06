import { apiRequest, API_ENDPOINTS, authStorage } from '@/config/api'

export const userService = {
  // Autenticación
  async login(credentials) {
    const data = await apiRequest(`${API_ENDPOINTS.AUTH}/login`, {
      method: 'POST',
      data: {
        email: credentials.email,
        password: credentials.password
      }
    }, true)

    authStorage.setToken(data.access_token)
    localStorage.setItem('isAuthenticated', 'true')

    // Obtener datos completos del usuario
    try {
      const userData = await apiRequest(`${API_ENDPOINTS.AUTH}/me`)
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (error) {
      console.error('Error getting user data:', error)
      // Fallback mínimo
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
    authStorage.removeToken()
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  },

  async getCurrentUser() {
    return apiRequest(`${API_ENDPOINTS.AUTH}/me`)
  },

  // CRUD de usuarios
  async getUsers(page = 1, limit = 10) {
    return apiRequest(`${API_ENDPOINTS.AUTH}?page=${page}&limit=${limit}`)
  },

  async getUserById(id) {
    return apiRequest(`${API_ENDPOINTS.AUTH}/${id}`)
  },

  async createUser(userData) {
    return apiRequest(API_ENDPOINTS.AUTH, {
      method: 'POST',
      data: userData
    })
  },

  async updateUser(id, userData) {
    return apiRequest(`${API_ENDPOINTS.AUTH}/${id}`, {
      method: 'PUT',
      data: userData
    })
  },

  async deleteUser(id) {
    return apiRequest(`${API_ENDPOINTS.AUTH}/${id}`, {
      method: 'DELETE'
    })
  },

  async changePassword(userId, currentPassword, newPassword) {
    return apiRequest(`${API_ENDPOINTS.AUTH}/${userId}/password`, {
      method: 'PUT',
      data: {
        old_password: currentPassword,
        new_password: newPassword
      }
    })
  },

  async changeEmail(userId, newEmail) {
    return apiRequest(`${API_ENDPOINTS.AUTH}/${userId}/email`, {
      method: 'PUT',
      data: {
        new_email: newEmail
      }
    })
  },

  // Permisos de usuario
  async getUserPermissions(userId) {
    return apiRequest(`${API_ENDPOINTS.AUTH}/${userId}/permissions`)
  },

  // Utilidades de autenticación
  isAuthenticated() {
    return !!authStorage.getToken()
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
