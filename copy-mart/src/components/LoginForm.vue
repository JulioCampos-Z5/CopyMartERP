<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-700 to-indigo-800 flex items-center justify-center px-4">
    <div class="max-w-md w-full space-y-8">
      <div class="card">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">CopyMart ERP</h2>
          <p class="text-gray-600">Inicia sesión en tu cuenta</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Correo Electrónico
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-field"
              :class="{ 'border-red-500': errors.email }"
              placeholder="usuario@ejemplo.com"
            />
            <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-field pr-12"
                :class="{ 'border-red-500': errors.password }"
                placeholder="Ingresa tu contraseña"
              />
              <button
                type="button"
                @click="togglePassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
          </div>
          
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember"
                v-model="form.remember"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="remember" class="ml-2 block text-sm text-gray-700">
                Recordar sesión
              </label>
            </div>
            
            <a href="#" class="text-sm text-primary-600 hover:text-primary-500">
              ¿Olvidaste tu contraseña?
            </a>
          </div>
          
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Iniciando sesión...
            </span>
            <span v-else>Iniciar Sesión</span>
          </button>
        </form>
        
        <div v-if="loginError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p class="text-red-800 text-sm">{{ loginError }}</p>
        </div>
        
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            ¿No tienes una cuenta? 
            <a href="#" class="text-primary-600 hover:text-primary-500 font-medium">
              Contacta al administrador
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import userService from '@/services/userService.js'

export default {
  name: 'LoginForm',
  data() {
    return {
      form: {
        email: '',
        password: '',
        remember: false
      },
      errors: {},
      isLoading: false,
      loginError: '',
      showPassword: false
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    
    validateForm() {
      this.errors = {}
      
      if (!this.form.email) {
        this.errors.email = 'El correo electrónico es requerido'
      } else if (!this.isValidEmail(this.form.email)) {
        this.errors.email = 'Ingresa un correo electrónico válido'
      }
      
      if (!this.form.password) {
        this.errors.password = 'La contraseña es requerida'
      } else if (this.form.password.length < 6) {
        this.errors.password = 'La contraseña debe tener al menos 6 caracteres'
      }
      
      return Object.keys(this.errors).length === 0
    },
    
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
    },
    
    async handleLogin() {
      if (!this.validateForm()) {
        return
      }
      
      this.isLoading = true
      this.loginError = ''
      
      try {
        // Intentar login real con userService
        const response = await userService.login({
          email: this.form.email,
          password: this.form.password
        })
        
        // Si el login es exitoso, redirigir al dashboard
        console.log('Login successful:', response)
        this.$router.push('/dashboard')
        
      } catch (error) {
        console.log('Login failed, using demo mode')
        
        // Simulación de login para desarrollo
        if (this.form.email === 'admin@copymart.com' && this.form.password === 'admin123') {
          // Simular datos de usuario administrador
          const demoUser = {
            id: 1,
            full_name: 'Administrador Demo',
            email: 'admin@copymart.com',
            role: 'ADMIN',
            is_active: true
          }
          
          // Guardar token y datos (usando las mismas claves que el router guard)
          localStorage.setItem('token', 'demo_token_' + Date.now())
          localStorage.setItem('user', JSON.stringify(demoUser))
          localStorage.setItem('isAuthenticated', 'true')
          
          this.$router.push('/dashboard')
          
        } else if (this.form.email === 'gerente@copymart.com' && this.form.password === 'gerente123') {
          // Simular datos de usuario gerente
          const demoUser = {
            id: 2,
            full_name: 'Gerente Demo',
            email: 'gerente@copymart.com',
            role: 'GERENTE',
            is_active: true
          }
          
          localStorage.setItem('token', 'demo_token_' + Date.now())
          localStorage.setItem('user', JSON.stringify(demoUser))
          localStorage.setItem('isAuthenticated', 'true')
          
          this.$router.push('/dashboard')
          
        } else if (this.form.email === 'empleado@copymart.com' && this.form.password === 'empleado123') {
          // Simular datos de usuario empleado
          const demoUser = {
            id: 3,
            full_name: 'Empleado Demo',
            email: 'empleado@copymart.com',
            role: 'EMPLEADO',
            is_active: true
          }
          
          localStorage.setItem('token', 'demo_token_' + Date.now())
          localStorage.setItem('user', JSON.stringify(demoUser))
          localStorage.setItem('isAuthenticated', 'true')
          
          this.$router.push('/dashboard')
          
        } else {
          this.loginError = 'Credenciales incorrectas. Prueba con:\nadmin@copymart.com / admin123'
        }
      } finally {
        this.isLoading = false
      }
    }
  },
  
  mounted() {
    // Verificar si ya está autenticado
    if (userService.isAuthenticated()) {
      this.$router.push('/dashboard')
    }
  }
}
</script>