import { defineStore } from 'pinia'
import { apiRequest, API_ENDPOINTS, authStorage } from '@/config/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: authStorage.getToken() || null,
    loading: false,
    error: null
  }),
  actions: {
    async loadSession() {
      this.token = authStorage.getToken()
      if (this.token && !this.user) {
        try {
          this.user = await apiRequest(`${API_ENDPOINTS.AUTH}/me`)
        } catch (err) {
          this.clearSession()
        }
      }
    },
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const data = await apiRequest(`${API_ENDPOINTS.AUTH}/login`, {
          method: 'POST',
          data: { email, password }
        }, true)

        authStorage.setToken(data.access_token)
        this.token = data.access_token

        this.user = await apiRequest(`${API_ENDPOINTS.AUTH}/me`)
        localStorage.setItem('user', JSON.stringify(this.user))

        return data
      } catch (err) {
        this.error = err.message || 'No se pudo iniciar sesión'
        throw err
      } finally {
        this.loading = false
      }
    },
    async logout() {
      this.clearSession()
    },
    clearSession() {
      authStorage.removeToken()
      this.user = null
      this.token = null
    }
  }
})
