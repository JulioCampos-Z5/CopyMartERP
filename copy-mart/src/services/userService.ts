/**
 * Servicio de Usuarios y Autenticación (TypeScript)
 * ==================================================
 */

import { apiRequest, API_ENDPOINTS, authStorage } from '@/config/api'
import type { User, LoginCredentials, AuthResponse } from '@/types'

interface UserListResponse {
  users: User[]
  total: number
  page: number
  limit: number
}

export const userService = {
  // Autenticación
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const data = await apiRequest<AuthResponse>(`${API_ENDPOINTS.AUTH}/login`, {
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
      const userData = await apiRequest<User>(`${API_ENDPOINTS.AUTH}/me`)
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (error) {
      console.error('Error getting user data:', error)
      // Fallback mínimo
      const userData: Partial<User> = {
        email: credentials.email,
        full_name: 'Usuario',
        role: 'user'
      }
      localStorage.setItem('user', JSON.stringify(userData))
    }

    return data
  },

  async logout(): Promise<void> {
    authStorage.removeToken()
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  },

  async getCurrentUser(): Promise<User> {
    return apiRequest<User>(`${API_ENDPOINTS.AUTH}/me`)
  },

  // CRUD de usuarios
  async getUsers(page: number = 1, limit: number = 10): Promise<UserListResponse> {
    return apiRequest<UserListResponse>(`${API_ENDPOINTS.AUTH}?page=${page}&limit=${limit}`)
  },

  async getUserById(id: number): Promise<User> {
    return apiRequest<User>(`${API_ENDPOINTS.AUTH}/${id}`)
  },

  async createUser(userData: Omit<User, 'user_id' | 'created_at'>): Promise<User> {
    return apiRequest<User>(`${API_ENDPOINTS.AUTH}/`, {
      method: 'POST',
      data: userData
    })
  },

  async updateUser(id: number, userData: Partial<User>): Promise<User> {
    return apiRequest<User>(`${API_ENDPOINTS.AUTH}/${id}`, {
      method: 'PUT',
      data: userData
    })
  },

  async deleteUser(id: number): Promise<void> {
    return apiRequest<void>(`${API_ENDPOINTS.AUTH}/${id}`, {
      method: 'DELETE'
    })
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<{ message: string }> {
    return apiRequest<{ message: string }>(`${API_ENDPOINTS.AUTH}/change-password`, {
      method: 'POST',
      data: {
        current_password: currentPassword,
        new_password: newPassword
      }
    })
  },

  async resetPassword(email: string): Promise<{ message: string }> {
    return apiRequest<{ message: string }>(`${API_ENDPOINTS.AUTH}/reset-password`, {
      method: 'POST',
      data: { email }
    })
  },

  // Compatibilidad: método para verificar autenticación
  isAuthenticated(): boolean {
    return authStorage.isAuthenticated()
  }
}
