<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-indigo-50 dark:bg-indigo-900/30 p-6 rounded-lg border border-indigo-200 dark:border-indigo-700">
          <h1 class="text-3xl font-bold text-indigo-800 dark:text-indigo-200 mb-2">Mi Perfil</h1>
          <p class="text-indigo-600 dark:text-indigo-400">Administra tu información personal y preferencias</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Profile Card -->
          <div class="lg:col-span-1">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 p-6">
              <div class="text-center">
                <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-indigo-100 dark:bg-indigo-900/50 mb-4">
                  <svg class="w-12 h-12 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">{{ user.name }}</h2>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</p>
                <p class="text-sm text-indigo-600 dark:text-indigo-400 mt-2">{{ user.role }}</p>
              </div>

              <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <h3 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Información de Usuario</h3>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Usuario desde:</span>
                    <span class="text-gray-900 dark:text-white">{{ formatDate(user.created_at) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Rol:</span>
                    <span class="text-gray-900 dark:text-white">{{ user.role }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Estado:</span>
                    <span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300 rounded-full">Activo</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Profile Form -->
          <div class="lg:col-span-2">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
              <div class="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Información Personal</h2>
              </div>
              
              <form @submit.prevent="updateProfile" class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Nombre Completo</label>
                    <input 
                      v-model="formData.name" 
                      type="text" 
                      class="input-field w-full"
                      placeholder="Tu nombre completo"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Correo Electrónico</label>
                    <input 
                      v-model="formData.email" 
                      type="email" 
                      class="input-field w-full"
                      placeholder="tu@email.com"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Departamento</label>
                    <input 
                      v-model="formData.department" 
                      type="text" 
                      class="input-field w-full"
                      disabled
                      placeholder="Departamento"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Rol</label>
                    <input 
                      v-model="formData.role" 
                      type="text" 
                      class="input-field w-full"
                      disabled
                      placeholder="Rol"
                    >
                  </div>
                </div>

                <div class="mt-6 flex justify-end gap-3">
                  <button type="submit" class="btn-primary" :disabled="saving">
                    {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Security Section -->
            <div class="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
              <div class="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Seguridad</h2>
              </div>
              
              <form @submit.prevent="changePassword" class="p-6">
                <div class="space-y-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Contraseña Actual</label>
                    <input 
                      v-model="passwordData.current_password" 
                      type="password" 
                      class="input-field w-full"
                      placeholder="Tu contraseña actual"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Nueva Contraseña</label>
                    <input 
                      v-model="passwordData.new_password" 
                      type="password" 
                      class="input-field w-full"
                      placeholder="Mínimo 8 caracteres"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Confirmar Nueva Contraseña</label>
                    <input 
                      v-model="passwordData.confirm_password" 
                      type="password" 
                      class="input-field w-full"
                      placeholder="Repite la nueva contraseña"
                    >
                  </div>
                </div>

                <div class="mt-6 flex justify-end">
                  <button type="submit" class="btn-primary" :disabled="changingPassword">
                    {{ changingPassword ? 'Cambiando...' : 'Cambiar Contraseña' }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Preferences Section -->
            <div class="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
              <div class="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Preferencias</h2>
              </div>
              
              <div class="p-6">
                <div class="space-y-4">
                  <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900 dark:text-white">Modo Oscuro</h3>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Cambia el tema de la interfaz</p>
                    </div>
                    <button @click="toggleDarkMode" type="button" :class="['relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 dark:focus:ring-offset-gray-800', isDarkMode ? 'bg-indigo-600' : 'bg-gray-200 dark:bg-gray-600']">
                      <span :class="['pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out', isDarkMode ? 'translate-x-5' : 'translate-x-0']"></span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast de notificación -->
    <div v-if="toast.show" :class="['fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg text-white transition-all duration-300 z-50', toast.type === 'success' ? 'bg-green-600' : 'bg-red-600']">
      {{ toast.message }}
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { userService } from '@/services/userService'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'PerfilView',
  components: {
    AppNavigation
  },
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') !== 'false',
      saving: false,
      changingPassword: false,
      toast: { show: false, message: '', type: 'success' },
      user: {
        id: null,
        name: '',
        email: '',
        role: '',
        created_at: ''
      },
      formData: {
        name: '',
        email: '',
        department: '',
        role: ''
      },
      passwordData: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
  },
  mounted() {
    this.loadUserData()
  },
  methods: {
    loadUserData() {
      try {
        const stored = localStorage.getItem('user')
        if (stored) {
          const userData = JSON.parse(stored)
          this.user = {
            id: userData.user_id,
            name: userData.full_name || userData.username || '',
            email: userData.email || '',
            role: userData.rol || userData.role || '',
            created_at: userData.created_at || ''
          }
          this.formData = {
            name: userData.full_name || '',
            email: userData.email || '',
            department: userData.department || '',
            role: userData.rol || userData.role || ''
          }
        }
      } catch (e) {
        console.error('Error loading user data:', e)
      }
    },

    showToast(message, type = 'success') {
      this.toast = { show: true, message, type }
      setTimeout(() => { this.toast.show = false }, 3000)
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('darkMode', this.isDarkMode)
      window.dispatchEvent(new CustomEvent('darkModeChange', { 
        detail: { isDarkMode: this.isDarkMode }
      }))
    },

    formatDate(dateStr) {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('es-MX')
    },
    
    async updateProfile() {
      if (!this.user.id) return
      this.saving = true
      try {
        const payload = {}
        if (this.formData.name) payload.full_name = this.formData.name
        if (this.formData.email) payload.email = this.formData.email

        await userService.updateUser(this.user.id, payload)
        
        // Actualizar localStorage y store
        const stored = JSON.parse(localStorage.getItem('user') || '{}')
        if (this.formData.name) stored.full_name = this.formData.name
        if (this.formData.email) stored.email = this.formData.email
        localStorage.setItem('user', JSON.stringify(stored))
        
        try {
          const authStore = useAuthStore()
          authStore.user = stored
        } catch (e) { /* store no disponible */ }

        this.loadUserData()
        this.showToast('Perfil actualizado exitosamente')
      } catch (err) {
        this.showToast('Error al actualizar perfil: ' + (err.message || err), 'error')
      } finally {
        this.saving = false
      }
    },

    async changePassword() {
      if (this.passwordData.new_password !== this.passwordData.confirm_password) {
        this.showToast('Las contraseñas no coinciden', 'error')
        return
      }
      
      if (this.passwordData.new_password.length < 8) {
        this.showToast('La contraseña debe tener al menos 8 caracteres', 'error')
        return
      }

      if (!this.user.id) return
      this.changingPassword = true
      try {
        await userService.changePassword(this.passwordData.current_password, this.passwordData.new_password)
        this.showToast('Contraseña cambiada exitosamente')
        this.passwordData = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
      } catch (err) {
        this.showToast('Error al cambiar contraseña: ' + (err.message || err), 'error')
      } finally {
        this.changingPassword = false
      }
    }
  }
}
</script>
