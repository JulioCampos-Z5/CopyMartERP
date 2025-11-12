<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header del Perfil -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Mi Perfil</h1>
        <p class="text-gray-600 mt-2">Gestiona tu información personal y configuración de cuenta</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Información Personal -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Datos Básicos -->
          <div class="card">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-900">Información Personal</h3>
              <button 
                @click="editingPersonal = !editingPersonal"
                class="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                {{ editingPersonal ? 'Cancelar' : 'Editar' }}
              </button>
            </div>

            <form @submit.prevent="updatePersonalInfo" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Nombre</label>
                  <input 
                    v-model="userInfo.firstName"
                    type="text" 
                    class="input-field"
                    :disabled="!editingPersonal"
                    required
                  >
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Apellido</label>
                  <input 
                    v-model="userInfo.lastName"
                    type="text" 
                    class="input-field"
                    :disabled="!editingPersonal"
                    required
                  >
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input 
                  v-model="userInfo.email"
                  type="email" 
                  class="input-field"
                  :disabled="!editingPersonal"
                  required
                >
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
                  <input 
                    v-model="userInfo.phone"
                    type="tel" 
                    class="input-field"
                    :disabled="!editingPersonal"
                  >
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Cargo</label>
                  <input 
                    v-model="userInfo.position"
                    type="text" 
                    class="input-field"
                    :disabled="!editingPersonal"
                  >
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
                <textarea 
                  v-model="userInfo.address"
                  class="input-field"
                  rows="2"
                  :disabled="!editingPersonal"
                ></textarea>
              </div>

              <div v-if="editingPersonal" class="flex justify-end space-x-3 pt-4">
                <button type="button" @click="cancelPersonalEdit" class="btn-secondary">
                  Cancelar
                </button>
                <button type="submit" class="btn-primary">
                  Guardar Cambios
                </button>
              </div>
            </form>
          </div>

          <!-- Cambiar Contraseña -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-6">Cambiar Contraseña</h3>
            
            <form @submit.prevent="changePassword" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña Actual</label>
                <input 
                  v-model="passwordForm.currentPassword"
                  type="password" 
                  class="input-field"
                  required
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nueva Contraseña</label>
                <input 
                  v-model="passwordForm.newPassword"
                  type="password" 
                  class="input-field"
                  required
                  minlength="6"
                >
                <p class="text-xs text-gray-500 mt-1">Mínimo 6 caracteres</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar Nueva Contraseña</label>
                <input 
                  v-model="passwordForm.confirmPassword"
                  type="password" 
                  class="input-field"
                  required
                  minlength="6"
                >
                <div v-if="passwordForm.newPassword && passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword" 
                     class="text-red-500 text-xs mt-1">
                  Las contraseñas no coinciden
                </div>
              </div>
              
              <div class="flex justify-end pt-4">
                <button type="submit" class="btn-primary" :disabled="!isPasswordFormValid">
                  Cambiar Contraseña
                </button>
              </div>
            </form>
          </div>

          <!-- Preferencias -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-6">Preferencias</h3>
            
            <div class="space-y-6">
              <!-- Notificaciones -->
              <div>
                <h4 class="text-md font-medium text-gray-900 mb-4">Notificaciones</h4>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm font-medium text-gray-700">Notificaciones por email</p>
                      <p class="text-xs text-gray-500">Recibir notificaciones de ventas y eventos importantes</p>
                    </div>
                    <label class="relative inline-flex items-center cursor-pointer">
                      <input v-model="preferences.emailNotifications" type="checkbox" class="sr-only peer">
                      <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                    </label>
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm font-medium text-gray-700">Alertas de inventario bajo</p>
                      <p class="text-xs text-gray-500">Notificar cuando el stock esté por debajo del mínimo</p>
                    </div>
                    <label class="relative inline-flex items-center cursor-pointer">
                      <input v-model="preferences.inventoryAlerts" type="checkbox" class="sr-only peer">
                      <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Idioma y Región -->
              <div>
                <h4 class="text-md font-medium text-gray-900 mb-4">Idioma y Región</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Idioma</label>
                    <select v-model="preferences.language" class="input-field">
                      <option value="es">Español</option>
                      <option value="en">English</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Zona Horaria</label>
                    <select v-model="preferences.timezone" class="input-field">
                      <option value="America/Mexico_City">Ciudad de México (GMT-6)</option>
                      <option value="America/Bogota">Bogotá (GMT-5)</option>
                      <option value="America/Lima">Lima (GMT-5)</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="flex justify-end pt-4">
                <button @click="savePreferences" class="btn-primary">
                  Guardar Preferencias
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar con foto y estadísticas -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Foto de Perfil -->
          <div class="card text-center">
            <div class="mb-4">
              <div class="w-32 h-32 mx-auto bg-gray-200 rounded-full flex items-center justify-center mb-4">
                <svg class="w-20 h-20 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ fullName }}</h3>
              <p class="text-gray-600">{{ userInfo.position }}</p>
            </div>
            
            <button class="btn-secondary w-full mb-4">
              <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2V7"></path>
              </svg>
              Cambiar Foto
            </button>
          </div>

          <!-- Estadísticas Rápidas -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Estadísticas</h3>
            <div class="space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Ventas realizadas</span>
                <span class="font-semibold text-primary-600">{{ userStats.salesCount }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Clientes atendidos</span>
                <span class="font-semibold text-primary-600">{{ userStats.customersServed }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Último acceso</span>
                <span class="text-sm text-gray-600">{{ formatLastLogin }}</span>
              </div>
            </div>
          </div>

          <!-- Actividad Reciente -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Actividad Reciente</h3>
            <div class="space-y-3">
              <div v-for="activity in recentActivity" :key="activity.id" 
                   class="flex items-start space-x-3 text-sm">
                <div class="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p class="text-gray-900">{{ activity.description }}</p>
                  <p class="text-gray-500 text-xs">{{ formatActivityDate(activity.date) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Acciones Rápidas -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
            <div class="space-y-3">
              <button @click="exportData" class="w-full text-left p-3 hover:bg-gray-50 rounded-lg transition-colors">
                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <span class="font-medium">Exportar Datos</span>
                </div>
              </button>
              
              <button @click="downloadBackup" class="w-full text-left p-3 hover:bg-gray-50 rounded-lg transition-colors">
                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                  </svg>
                  <span class="font-medium">Respaldar Datos</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación -->
    <div v-if="showConfirmModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">{{ confirmModal.title }}</h3>
        <p class="text-gray-600 mb-6">{{ confirmModal.message }}</p>
        <div class="flex justify-end space-x-3">
          <button @click="closeModal" class="btn-secondary">Cancelar</button>
          <button @click="confirmAction" class="btn-primary">Confirmar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '../components/AppNavigation.vue'

export default {
  name: 'PerfilView',
  components: {
    AppNavigation
  },
  data() {
    return {
      editingPersonal: false,
      userInfo: {
        firstName: 'Juan',
        lastName: 'Pérez',
        email: 'juan.perez@copymart.com',
        phone: '+52 55 1234-5678',
        position: 'Gerente de Ventas',
        address: 'Av. Principal 123, Col. Centro, Ciudad de México'
      },
      originalUserInfo: {},
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      preferences: {
        emailNotifications: true,
        inventoryAlerts: true,
        language: 'es',
        timezone: 'America/Mexico_City'
      },
      userStats: {
        salesCount: 247,
        customersServed: 89,
        lastLogin: new Date('2025-11-05T14:30:00')
      },
      recentActivity: [
        {
          id: 1,
          description: 'Venta realizada a María González',
          date: new Date('2025-11-05T10:30:00')
        },
        {
          id: 2,
          description: 'Producto agregado al inventario',
          date: new Date('2025-11-04T16:45:00')
        },
        {
          id: 3,
          description: 'Cliente registrado: José Ramírez',
          date: new Date('2025-11-04T14:20:00')
        },
        {
          id: 4,
          description: 'Reporte generado: Ventas mensuales',
          date: new Date('2025-11-03T09:15:00')
        }
      ],
      showConfirmModal: false,
      confirmModal: {
        title: '',
        message: '',
        action: null
      }
    }
  },
  computed: {
    fullName() {
      return `${this.userInfo.firstName} ${this.userInfo.lastName}`
    },
    formatLastLogin() {
      return this.userStats.lastLogin.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    },
    isPasswordFormValid() {
      return this.passwordForm.currentPassword && 
             this.passwordForm.newPassword && 
             this.passwordForm.confirmPassword &&
             this.passwordForm.newPassword === this.passwordForm.confirmPassword &&
             this.passwordForm.newPassword.length >= 6
    }
  },
  methods: {
    updatePersonalInfo() {
      this.showConfirmation(
        'Actualizar Información',
        '¿Estás seguro que deseas actualizar tu información personal?',
        () => {
          // Aquí iría la lógica para actualizar en el backend
          console.log('Información personal actualizada:', this.userInfo)
          this.editingPersonal = false
          this.showSuccessMessage('Información actualizada correctamente')
        }
      )
    },
    
    cancelPersonalEdit() {
      this.userInfo = { ...this.originalUserInfo }
      this.editingPersonal = false
    },
    
    changePassword() {
      this.showConfirmation(
        'Cambiar Contraseña',
        '¿Estás seguro que deseas cambiar tu contraseña?',
        () => {
          // Aquí iría la lógica para cambiar la contraseña
          console.log('Contraseña cambiada')
          this.passwordForm = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
          }
          this.showSuccessMessage('Contraseña actualizada correctamente')
        }
      )
    },
    
    savePreferences() {
      // Aquí iría la lógica para guardar las preferencias
      console.log('Preferencias guardadas:', this.preferences)
      this.showSuccessMessage('Preferencias guardadas correctamente')
    },
    
    exportData() {
      this.showConfirmation(
        'Exportar Datos',
        'Se descargará un archivo con todos tus datos. ¿Continuar?',
        () => {
          // Aquí iría la lógica para exportar datos
          console.log('Exportando datos del usuario...')
          this.showSuccessMessage('Los datos se están preparando para descarga')
        }
      )
    },
    
    downloadBackup() {
      this.showConfirmation(
        'Respaldar Datos',
        'Se creará un respaldo de tu información. ¿Continuar?',
        () => {
          // Aquí iría la lógica para crear respaldo
          console.log('Creando respaldo...')
          this.showSuccessMessage('El respaldo se ha iniciado')
        }
      )
    },
    
    formatActivityDate(date) {
      const now = new Date()
      const diff = now - date
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      
      if (days === 0) {
        const hours = Math.floor(diff / (1000 * 60 * 60))
        if (hours === 0) {
          const minutes = Math.floor(diff / (1000 * 60))
          return `Hace ${minutes} min`
        }
        return `Hace ${hours}h`
      } else if (days === 1) {
        return 'Ayer'
      } else if (days < 7) {
        return `Hace ${days} días`
      } else {
        return date.toLocaleDateString('es-ES', {
          day: 'numeric',
          month: 'short'
        })
      }
    },
    
    showConfirmation(title, message, action) {
      this.confirmModal = { title, message, action }
      this.showConfirmModal = true
    },
    
    confirmAction() {
      if (this.confirmModal.action) {
        this.confirmModal.action()
      }
      this.closeModal()
    },
    
    closeModal() {
      this.showConfirmModal = false
      this.confirmModal = { title: '', message: '', action: null }
    },
    
    showSuccessMessage(message) {
      // En una aplicación real, aquí mostrarías un toast o notificación
      alert(message)
    }
  },
  
  mounted() {
    // Guardar una copia de la información original para poder cancelar ediciones
    this.originalUserInfo = { ...this.userInfo }
  }
}
</script>