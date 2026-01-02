<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-indigo-50 p-6 rounded-lg border border-indigo-200">
          <h1 class="text-3xl font-bold text-indigo-800 mb-2">Mi Perfil</h1>
          <p class="text-indigo-600">Administra tu información personal y preferencias</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Profile Card -->
          <div class="lg:col-span-1">
            <div class="bg-white rounded-lg shadow border p-6">
              <div class="text-center">
                <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-indigo-100 mb-4">
                  <svg class="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h2 class="text-xl font-semibold text-gray-900">{{ user.name }}</h2>
                <p class="text-sm text-gray-500">{{ user.email }}</p>
                <p class="text-sm text-indigo-600 mt-2">{{ user.role }}</p>
                
                <button class="mt-4 btn-secondary w-full">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Cambiar Foto
                </button>
              </div>

              <div class="mt-6 pt-6 border-t border-gray-200">
                <h3 class="text-sm font-medium text-gray-900 mb-3">Información de Usuario</h3>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500">Usuario desde:</span>
                    <span class="text-gray-900">{{ formatDate(user.created_at) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Último acceso:</span>
                    <span class="text-gray-900">Hoy 09:45 AM</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Estado:</span>
                    <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Activo</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Profile Form -->
          <div class="lg:col-span-2">
            <div class="bg-white rounded-lg shadow border">
              <div class="p-6 border-b border-gray-200">
                <h2 class="text-xl font-semibold text-gray-900">Información Personal</h2>
              </div>
              
              <form @submit.prevent="updateProfile" class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Nombre Completo</label>
                    <input 
                      v-model="formData.name" 
                      type="text" 
                      class="input-field w-full"
                      placeholder="Tu nombre completo"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Correo Electrónico</label>
                    <input 
                      v-model="formData.email" 
                      type="email" 
                      class="input-field w-full"
                      placeholder="tu@email.com"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
                    <input 
                      v-model="formData.phone" 
                      type="tel" 
                      class="input-field w-full"
                      placeholder="555-1234-5678"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Puesto</label>
                    <input 
                      v-model="formData.position" 
                      type="text" 
                      class="input-field w-full"
                      placeholder="Tu puesto"
                    >
                  </div>

                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
                    <textarea 
                      v-model="formData.address" 
                      rows="3" 
                      class="input-field w-full"
                      placeholder="Tu dirección completa"
                    ></textarea>
                  </div>
                </div>

                <div class="mt-6 flex justify-end gap-3">
                  <button type="button" class="btn-secondary">Cancelar</button>
                  <button type="submit" class="btn-primary">Guardar Cambios</button>
                </div>
              </form>
            </div>

            <!-- Security Section -->
            <div class="mt-6 bg-white rounded-lg shadow border">
              <div class="p-6 border-b border-gray-200">
                <h2 class="text-xl font-semibold text-gray-900">Seguridad</h2>
              </div>
              
              <form @submit.prevent="changePassword" class="p-6">
                <div class="space-y-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña Actual</label>
                    <input 
                      v-model="passwordData.current_password" 
                      type="password" 
                      class="input-field w-full"
                      placeholder="Tu contraseña actual"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Nueva Contraseña</label>
                    <input 
                      v-model="passwordData.new_password" 
                      type="password" 
                      class="input-field w-full"
                      placeholder="Mínimo 8 caracteres"
                    >
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar Nueva Contraseña</label>
                    <input 
                      v-model="passwordData.confirm_password" 
                      type="password" 
                      class="input-field w-full"
                      placeholder="Repite la nueva contraseña"
                    >
                  </div>
                </div>

                <div class="mt-6 flex justify-end">
                  <button type="submit" class="btn-primary">Cambiar Contraseña</button>
                </div>
              </form>
            </div>

            <!-- Preferences Section -->
            <div class="mt-6 bg-white rounded-lg shadow border">
              <div class="p-6 border-b border-gray-200">
                <h2 class="text-xl font-semibold text-gray-900">Preferencias</h2>
              </div>
              
              <div class="p-6">
                <div class="space-y-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">Notificaciones por Email</h3>
                      <p class="text-sm text-gray-500">Recibe notificaciones importantes por correo</p>
                    </div>
                    <button type="button" class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-gray-200 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2">
                      <span class="translate-x-0 pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"></span>
                    </button>
                  </div>

                  <div class="flex items-center justify-between pt-4 border-t border-gray-200">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">Notificaciones de Sistema</h3>
                      <p class="text-sm text-gray-500">Alertas y actualizaciones del sistema</p>
                    </div>
                    <button type="button" class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-indigo-600 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2">
                      <span class="translate-x-5 pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"></span>
                    </button>
                  </div>

                  <div class="flex items-center justify-between pt-4 border-t border-gray-200">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">Modo Oscuro</h3>
                      <p class="text-sm text-gray-500">Cambia el tema de la interfaz</p>
                    </div>
                    <button @click="toggleDarkMode" type="button" :class="['relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2', isDarkMode ? 'bg-indigo-600' : 'bg-gray-200']">
                      <span :class="['translate-x-0 pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out', isDarkMode ? 'translate-x-5' : 'translate-x-0']"></span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'

export default {
  name: 'PerfilView',
  components: {
    AppNavigation
  },
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') !== 'false',
      user: {
        name: '',
        email: '',
        role: '',
        created_at: ''
      },
      formData: {
        name: '',
        email: '',
        phone: '',
        position: '',
        address: ''
      },
      passwordData: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
  },
  methods: {
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
      try {
        // TODO: Implementar actualización de perfil con el API
        alert('Perfil actualizado exitosamente')
      } catch (err) {
        alert('Error al actualizar perfil: ' + err.message)
      }
    },

    async changePassword() {
      if (this.passwordData.new_password !== this.passwordData.confirm_password) {
        alert('Las contraseñas no coinciden')
        return
      }
      
      if (this.passwordData.new_password.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres')
        return
      }

      try {
        // TODO: Implementar cambio de contraseña con el API
        alert('Contraseña cambiada exitosamente')
        this.passwordData = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
      } catch (err) {
        alert('Error al cambiar contraseña: ' + err.message)
      }
    }
  }
}
</script>
