/**
 * Store de Autenticación con Pinia
 * =================================
 * Centraliza el estado de autenticación y permisos del usuario
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginCredentials, AuthResponse } from '@/types'
import { apiRequest, API_ENDPOINTS } from '@/config/api'

export const useAuthStore = defineStore('auth', () => {
  // ============================================
  // STATE
  // ============================================
  
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref<boolean>(false)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)

  // ============================================
  // GETTERS
  // ============================================
  
  const userRole = computed(() => user.value?.role || '')
  const userPermissions = computed(() => user.value?.permissions || [])
  const userName = computed(() => user.value?.full_name || user.value?.username || '')
  const userEmail = computed(() => user.value?.email || '')

  // ============================================
  // ACTIONS
  // ============================================
  
  /**
   * Inicializa el store desde localStorage
   */
  function initializeAuth() {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    const storedIsAuthenticated = localStorage.getItem('isAuthenticated')

    if (storedToken && storedUser && storedIsAuthenticated === 'true') {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
      isAuthenticated.value = true
    }
  }

  /**
   * Login del usuario
   */
  async function login(credentials: LoginCredentials): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const formData = new URLSearchParams()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await apiRequest<AuthResponse>(
        `${API_ENDPOINTS.AUTH}/login`,
        {
          method: 'POST',
          data: formData,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        },
        true // skipAuth
      )

      // Guardar en estado
      token.value = response.access_token
      user.value = response.user
      isAuthenticated.value = true

      // Persistir en localStorage
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      localStorage.setItem('isAuthenticated', 'true')
    } catch (err: any) {
      error.value = err.message || 'Error al iniciar sesión'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout del usuario
   */
  function logout(): void {
    // Limpiar estado
    user.value = null
    token.value = null
    isAuthenticated.value = false
    error.value = null

    // Limpiar localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  }

  /**
   * Verifica si el usuario tiene un permiso específico
   */
  function hasPermission(permission: string): boolean {
    return userPermissions.value.includes(permission)
  }

  /**
   * Verifica si el usuario tiene alguno de los permisos
   */
  function hasAnyPermission(permissions: string[]): boolean {
    return permissions.some(p => userPermissions.value.includes(p))
  }

  /**
   * Verifica si el usuario tiene todos los permisos
   */
  function hasAllPermissions(permissions: string[]): boolean {
    return permissions.every(p => userPermissions.value.includes(p))
  }

  /**
   * Actualiza la información del usuario
   */
  async function refreshUser(): Promise<void> {
    if (!isAuthenticated.value) return

    try {
      const response = await apiRequest<{ user: User }>(
        `${API_ENDPOINTS.AUTH}/me`,
        { method: 'GET' }
      )
      
      user.value = response.user
      localStorage.setItem('user', JSON.stringify(response.user))
    } catch (err: any) {
      console.error('Error refreshing user:', err)
      // Si falla, hacer logout
      logout()
    }
  }

  // ============================================
  // INITIALIZATION
  // ============================================
  
  // Inicializar al crear el store
  initializeAuth()

  return {
    // State
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    
    // Getters
    userRole,
    userPermissions,
    userName,
    userEmail,
    
    // Actions
    login,
    logout,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    refreshUser
  }
})
