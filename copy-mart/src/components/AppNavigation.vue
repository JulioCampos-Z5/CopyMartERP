<template>
  <!-- Top Navigation Bar -->
  <nav class="bg-white shadow-md fixed w-full top-0 z-50">
    <div class="max-w-full mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center space-x-3">
          <svg class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="text-xl font-semibold text-gray-800">CopyMart ERP</span>
        </div>

        <!-- Right Side -->
        <div class="flex items-center space-x-4">
          <!-- Apps Menu Button -->
          <button 
            @click="toggleAppsMenu"
            class="p-2 rounded-full hover:bg-gray-100 transition-colors relative"
            title="Aplicaciones"
          >
            <svg class="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6-8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6-8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
            </svg>
          </button>

          <!-- User Profile -->
          <div class="relative">
            <button 
              @click="toggleUserMenu"
              class="flex items-center space-x-2 p-1 rounded-full hover:bg-gray-100 transition-colors"
            >
              <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
                {{ currentUser.name.charAt(0).toUpperCase() }}
              </div>
            </button>

            <!-- User Dropdown -->
            <div 
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 py-2"
              @click.stop
            >
              <div class="px-4 py-3 border-b border-gray-200">
                <p class="text-sm font-semibold text-gray-900">{{ currentUser.name }}</p>
                <p class="text-sm text-gray-500">{{ currentUser.email }}</p>
              </div>
              <router-link 
                to="/perfil" 
                @click="showUserMenu = false"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Mi Perfil
              </router-link>
              <button 
                @click="logout" 
                class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <!-- Apps Menu Modal (Outside nav to avoid z-index conflicts) -->
  <div 
    v-if="showAppsMenu"
    @click="showAppsMenu = false"
    class="fixed inset-0 bg-black bg-opacity-20 z-[60]"
  >
    <div 
      @click.stop
      class="absolute right-4 top-16 w-auto bg-gray-900 rounded-2xl shadow-2xl p-6"
    >
        <!-- General -->
        <div class="mb-6">
          <h3 class="text-xs text-gray-400 uppercase font-semibold mb-3 px-2">General</h3>
          <div class="grid grid-cols-1 gap-3">
            <router-link 
              to="/dashboard"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Dashboard</span>
            </router-link>
          </div>
        </div>

        <!-- Comercial -->
        <div class="mb-6">
          <h3 class="text-xs text-gray-400 uppercase font-semibold mb-3 px-2">Comercial</h3>
          <div class="grid grid-cols-4 gap-3">
            <router-link 
              to="/ventas"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Ventas</span>
            </router-link>

            <router-link 
              to="/rentas"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Rentas</span>
            </router-link>

            <router-link 
              to="/atencion-clientes"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Atención</span>
            </router-link>

            <router-link 
              to="/clientes"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Clientes</span>
            </router-link>

            <router-link 
              to="/produccion"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Producción</span>
            </router-link>
          </div>
        </div>

        <!-- Administración -->
        <div class="mb-6">
          <h3 class="text-xs text-gray-400 uppercase font-semibold mb-3 px-2">Administración</h3>
          <div class="grid grid-cols-4 gap-3">
            <router-link 
              to="/compras"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Compras</span>
            </router-link>

            <router-link 
              to="/almacen"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Almacén</span>
            </router-link>

            <router-link 
              to="/cobranza"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Cobranza</span>
            </router-link>

            <router-link 
              to="/facturacion"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Facturación</span>
            </router-link>

            <router-link 
              to="/inventario"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Inventario</span>
            </router-link>
          </div>
        </div>

        <!-- Operaciones y Más -->
        <div>
          <h3 class="text-xs text-gray-400 uppercase font-semibold mb-3 px-2">Operaciones y Más</h3>
          <div class="grid grid-cols-4 gap-3">
            <router-link 
              to="/rutas"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-lime-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Rutas</span>
            </router-link>

            <router-link 
              to="/ordenes-servicio"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">Órdenes</span>
            </router-link>

            <router-link 
              to="/recursos-humanos"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">RH</span>
            </router-link>

            <router-link 
              to="/ti"
              @click="showAppsMenu = false"
              class="flex flex-col items-center justify-center p-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              <div class="w-12 h-12 mb-2 flex items-center justify-center">
                <svg class="w-10 h-10 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <span class="text-xs text-white text-center">TI</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const showAppsMenu = ref(false)
const showUserMenu = ref(false)
const currentUser = ref({
  name: 'Usuario Demo',
  email: 'usuario@copymart.com'
})

const loadCurrentUser = () => {
  try {
    const userDataStr = localStorage.getItem('user')
    if (userDataStr) {
      const userData = JSON.parse(userDataStr)
      currentUser.value = {
        name: userData.name || userData.full_name || 'Usuario Demo',
        email: userData.email || 'usuario@copymart.com'
      }
    }
  } catch (error) {
    console.error('Error loading user:', error)
  }
}

const toggleAppsMenu = () => {
  showAppsMenu.value = !showAppsMenu.value
  showUserMenu.value = false
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  showAppsMenu.value = false
}

const logout = async () => {
  try {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
    await router.push('/login')
  } catch (error) {
    console.error('Error during logout:', error)
    localStorage.clear()
    await router.push('/login')
  }
}

onMounted(() => {
  loadCurrentUser()
})
</script>
