<template>
  <nav class="bg-white shadow-lg border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo y marca -->
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <svg class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h1 class="ml-2 text-xl font-bold text-gray-900">CopyMart ERP</h1>
          </div>
          
          <!-- Navegación principal (escritorio) -->
          <div class="hidden md:block ml-10">
            <div class="flex items-baseline space-x-4">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.to"
                :class="[
                  isActive(item.to) 
                    ? 'bg-primary-100 text-primary-700 border-primary-500' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'px-3 py-2 rounded-md text-sm font-medium border-b-2 border-transparent hover:border-gray-300 transition-colors duration-200'
                ]"
              >
                <svg class="h-4 w-4 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                </svg>
                {{ item.name }}
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Acciones de usuario -->
        <div class="hidden md:flex items-center space-x-4">
          <!-- Notificaciones -->
          <button class="relative p-2 text-gray-600 hover:text-gray-900 rounded-full hover:bg-gray-100 transition-colors duration-200">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-3.5-3.5a.5.5 0 010-.707L20 9.5V6a2 2 0 00-2-2h-4a2 2 0 00-2 2v3.5l3.5 3.5z" />
            </svg>
            <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
          </button>
          
          <!-- Menú de usuario -->
          <div class="relative" v-click-outside="closeUserMenu">
            <button 
              @click="toggleUserMenu"
              class="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors duration-200"
            >
              <div class="h-8 w-8 bg-primary-600 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-white">{{ userInitials }}</span>
              </div>
              <span class="text-sm font-medium">{{ userName }}</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <!-- Dropdown del usuario -->
            <div 
              v-show="showUserMenu"
              class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
            >
              <div class="py-1">
                <a 
                  v-for="item in userMenuItems"
                  :key="item.name"
                  :href="item.href"
                  @click="item.action && item.action(); closeUserMenu()"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                >
                  <svg class="h-4 w-4 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                  </svg>
                  {{ item.name }}
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Botón de menú móvil -->
        <div class="md:hidden">
          <button 
            @click="toggleMobileMenu"
            class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors duration-200"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Menú móvil -->
      <div v-show="showMobileMenu" class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1 bg-gray-50">
          <router-link
            v-for="item in navigation"
            :key="item.name"
            :to="item.to"
            @click="showMobileMenu = false"
            :class="[
              isActive(item.to) 
                ? 'bg-primary-100 text-primary-700' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
              'block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200'
            ]"
          >
            <svg class="h-5 w-5 inline-block mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
            </svg>
            {{ item.name }}
          </router-link>
        </div>
        
        <!-- Usuario móvil -->
        <div class="pt-4 pb-3 border-t border-gray-200">
          <div class="flex items-center px-4">
            <div class="h-10 w-10 bg-primary-600 rounded-full flex items-center justify-center">
              <span class="text-sm font-medium text-white">{{ userInitials }}</span>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ userName }}</div>
              <div class="text-sm text-gray-500">{{ userEmail }}</div>
            </div>
          </div>
          <div class="mt-3 px-2 space-y-1">
            <a 
              v-for="item in userMenuItems"
              :key="item.name"
              :href="item.href"
              @click="item.action && item.action(); showMobileMenu = false"
              class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors duration-200"
            >
              {{ item.name }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { usePermissions } from '../composables/usePermissions'
import { computed } from 'vue'

export default {
  name: 'AppNavigation',
  setup() {
    const { getAccessibleModules, userInfo, canCreate, canEdit, canDelete } = usePermissions()
    
    // Mapeo de módulos a iconos SVG
    const moduleIcons = {
      'dashboard': 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z',
      'ventas': 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
      'inventario': 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
      'clientes': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
      'reportes': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      'usuarios': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
    }
    
    // Construir navegación con módulos accesibles
    const navigation = computed(() => {
      return getAccessibleModules.value.map(module => ({
        name: module.name,
        to: module.route,
        icon: moduleIcons[module.key] || moduleIcons['dashboard']
      }))
    })
    
    return {
      navigation,
      userInfo,
      canCreate,
      canEdit,
      canDelete
    }
  },
  data() {
    return {
      showUserMenu: false,
      showMobileMenu: false,
      userMenuItems: [
        {
          name: 'Perfil',
          href: '#',
          icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
          action: () => this.$router.push('/perfil')
        },
        {
          name: 'Usuarios',
          href: '#',
          icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z',
          action: () => this.$router.push('/usuarios')
        },
        {
          name: 'Configuración',
          href: '#',
          icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'
        },
        {
          name: 'Cerrar Sesión',
          href: '#',
          icon: 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
          action: () => this.logout()
        }
      ]
    }
  },
  computed: {
    userName() {
      return this.userInfo.name
    },
    userEmail() {
      return this.userInfo.email
    },
    userInitials() {
      return this.userInfo.initials
    }
  },
  methods: {
    isActive(route) {
      return this.$route.path === route
    },
    
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
    },
    
    closeUserMenu() {
      this.showUserMenu = false
    },
    
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu
    },
    
    logout() {
      // Limpiar estado de autenticación
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('user')
      
      // Redirigir al login
      this.$router.push('/login')
    }
  },
  
  // Directiva personalizada para cerrar menús al hacer clic fuera
  directives: {
    'click-outside': {
      mounted(el, binding) {
        el.clickOutsideEvent = function (event) {
          if (!(el == event.target || el.contains(event.target))) {
            binding.value()
          }
        }
        document.addEventListener('click', el.clickOutsideEvent)
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
      }
    }
  }
}
</script>