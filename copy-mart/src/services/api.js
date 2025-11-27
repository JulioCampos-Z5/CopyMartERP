const API_URL = 'http://localhost:8000'

class ApiService {
  constructor() {
    this.baseURL = API_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const token = localStorage.getItem('token')
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    }

    if (token && !options.skipAuth) {
      config.headers['Authorization'] = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}))
        throw new Error(error.detail || `Error ${response.status}: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API Request Error:', error)
      throw error
    }
  }

  // Auth endpoints
  async login(email, password) {
    const response = await this.request('/users/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      skipAuth: true,
    })
    
    if (response.access_token) {
      localStorage.setItem('token', response.access_token)
    }
    
    return response
  }

  async logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  }

  // User endpoints
  async getCurrentUser() {
    // Decodificar el token para obtener el user_id
    const token = localStorage.getItem('token')
    if (!token) throw new Error('No token found')
    
    const payload = JSON.parse(atob(token.split('.')[1]))
    return await this.request(`/users/${payload.user_id}`)
  }

  async getUsers() {
    return await this.request('/users/')
  }

  async getUser(userId) {
    return await this.request(`/users/${userId}`)
  }

  async createUser(userData) {
    return await this.request('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  async changePassword(userId, oldPassword, newPassword) {
    return await this.request(`/users/${userId}/password`, {
      method: 'PUT',
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
    })
  }

  async changeEmail(userId, newEmail) {
    return await this.request(`/users/${userId}/email`, {
      method: 'PUT',
      body: JSON.stringify({ new_email: newEmail }),
    })
  }

  async getUserPermissions(userId) {
    return await this.request(`/users/${userId}/permissions`)
  }
}

export default new ApiService()
