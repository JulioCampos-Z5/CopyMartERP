<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Gestión de Usuarios</h1>
          <p class="text-gray-600 mt-2">Administra los usuarios del sistema CopyMart ERP</p>
        </div>
        <button @click="showCreateModal = true" class="btn-primary">
          <svg class="h-5 w-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          Nuevo Usuario
        </button>
      </div>

      <!-- Estadísticas -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card hover:shadow-lg transition-shadow duration-200">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100">
              <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Usuarios</p>
              <p class="text-2xl font-bold text-gray-900">{{ totalUsers }}</p>
            </div>
          </div>
        </div>
        
        <div class="card hover:shadow-lg transition-shadow duration-200">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100">
              <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Usuarios Activos</p>
              <p class="text-2xl font-bold text-gray-900">{{ activeUsers }}</p>
            </div>
          </div>
        </div>
        
        <div class="card hover:shadow-lg transition-shadow duration-200">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-yellow-100">
              <svg class="h-8 w-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Usuarios Inactivos</p>
              <p class="text-2xl font-bold text-gray-900">{{ inactiveUsers }}</p>
            </div>
          </div>
        </div>
        
        <div class="card hover:shadow-lg transition-shadow duration-200">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-purple-100">
              <svg class="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Administradores</p>
              <p class="text-2xl font-bold text-gray-900">{{ adminUsers }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros y búsqueda -->
      <div class="card mb-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 md:space-x-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700 mb-2">Buscar usuario</label>
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar por nombre, email o teléfono..."
                class="input-field pl-10"
              >
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
            </div>
          </div>
          
          <div class="flex space-x-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Rol</label>
              <select v-model="selectedRole" class="input-field">
                <option value="">Todos los roles</option>
                <option value="ADMINISTRADOR">Administrador</option>
                <option value="GERENCIA">Gerente</option>
                <option value="USUARIO">Usuario</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Estado</label>
              <select v-model="selectedStatus" class="input-field">
                <option value="">Todos los estados</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabla de usuarios -->
      <div class="card">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuario
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rol
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Creado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  Cargando usuarios...
                </td>
              </tr>
              <tr v-else-if="filteredUsers.length === 0">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  No se encontraron usuarios
                </td>
              </tr>
              <tr v-for="user in filteredUsers" :key="user.user_id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-10 w-10 flex-shrink-0">
                      <div class="h-10 w-10 bg-primary-600 rounded-full flex items-center justify-center">
                        <span class="text-sm font-medium text-white">{{ getUserInitials(user.full_name) }}</span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ user.full_name }}</div>
                      <div class="text-sm text-gray-500">{{ user.email }}</div>
                      <div class="text-xs text-gray-400">@{{ user.username }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    user.rol === 'ADMINISTRADOR' ? 'bg-red-100 text-red-800' :
                    user.rol === 'GERENCIA' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ getRoleDisplayName(user.rol) }}
                  </span>
                  <div v-if="user.department" class="text-xs text-gray-500 mt-1">
                    {{ getDepartmentDisplayName(user.department) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  ]">
                    {{ user.is_active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(user.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex space-x-2">
                    <button 
                      @click="editUser(user)"
                      class="text-primary-600 hover:text-primary-900 p-1 rounded hover:bg-primary-50"
                    >
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                    <button 
                      @click="toggleUserStatus(user)"
                      :class="[
                        'p-1 rounded',
                        user.is_active 
                          ? 'text-red-600 hover:text-red-900 hover:bg-red-50' 
                          : 'text-green-600 hover:text-green-900 hover:bg-green-50'
                      ]"
                    >
                      <svg v-if="user.is_active" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18.364 5.636M5.636 18.364l12.728-12.728"></path>
                      </svg>
                      <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </button>
                    <button 
                      @click="deleteUser(user)"
                      class="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50"
                    >
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Anterior
            </button>
            <button class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Siguiente
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando <span class="font-medium">1</span> a <span class="font-medium">10</span> de <span class="font-medium">{{ filteredUsers.length }}</span> resultados
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                </button>
                <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">1</button>
                <button class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para crear/editar usuario -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ showCreateModal ? 'Crear Nuevo Usuario' : 'Editar Usuario' }}
          </h3>
          
          <form @submit.prevent="showCreateModal ? createUser() : updateUser()">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de usuario</label>
                <input
                  v-model="userForm.username"
                  type="text"
                  required
                  class="input-field"
                  placeholder="Ej: jperez"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre completo</label>
                <input
                  v-model="userForm.full_name"
                  type="text"
                  required
                  class="input-field"
                  placeholder="Ej: Juan Pérez García"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  v-model="userForm.email"
                  type="email"
                  required
                  class="input-field"
                  placeholder="usuario@correo.com"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Rol</label>
                <select v-model="userForm.rol" required class="input-field">
                  <option value="">Seleccionar rol</option>
                  <option value="ADMINISTRADOR">Administrador</option>
                  <option value="GERENCIA">Gerente</option>
                  <option value="USUARIO">Usuario</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Departamento</label>
                <select v-model="userForm.department" class="input-field">
                  <option value="">Sin departamento</option>
                  <option value="RH">Recursos Humanos</option>
                  <option value="ADMINISTRACION">Administración</option>
                  <option value="COMERCIAL">Comercial</option>
                  <option value="OPERACIONES">Operaciones</option>
                </select>
              </div>
              
              <div v-if="showCreateModal">
                <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
                <input
                  v-model="userForm.password"
                  type="password"
                  required
                  class="input-field"
                  placeholder="Contraseña segura"
                  minlength="6"
                >
              </div>
              
              <div>
                <label class="flex items-center">
                  <input type="checkbox" v-model="userForm.is_active" class="mr-2">
                  <span class="text-sm font-medium text-gray-700">Usuario activo</span>
                </label>
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">
                Cancelar
              </button>
              <button type="submit" class="btn-primary">
                {{ showCreateModal ? 'Crear Usuario' : 'Actualizar Usuario' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '../components/AppNavigation.vue'
import userService from '../services/userService'

export default {
  name: 'UsuariosView',
  components: {
    AppNavigation
  },
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedStatus: '',
      showCreateModal: false,
      showEditModal: false,
      editingUser: null,
      isLoading: false,
      userForm: {
        username: '',
        full_name: '',
        email: '',
        rol: '',
        department: '',
        password: '',
        is_active: true
      },
      users: []
    }
  },
  computed: {
    totalUsers() {
      return this.users.length
    },
    activeUsers() {
      return this.users.filter(user => user.is_active).length
    },
    inactiveUsers() {
      return this.users.filter(user => !user.is_active).length
    },
    adminUsers() {
      return this.users.filter(user => user.rol === 'ADMINISTRADOR').length
    },
    filteredUsers() {
      return this.users.filter(user => {
        const matchesSearch = !this.searchQuery || 
          user.full_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (user.username && user.username.toLowerCase().includes(this.searchQuery.toLowerCase()))
        
        const matchesRole = !this.selectedRole || user.rol === this.selectedRole
        const matchesStatus = !this.selectedStatus || 
          (this.selectedStatus === 'active' && user.is_active) ||
          (this.selectedStatus === 'inactive' && !user.is_active)
        
        return matchesSearch && matchesRole && matchesStatus
      })
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.isLoading = true
      try {
        const response = await userService.getUsers()
        this.users = response || []
      } catch (error) {
        console.error('Error cargando usuarios:', error)
        this.showErrorMessage('Error al cargar los usuarios')
      } finally {
        this.isLoading = false
      }
    },

    getUserInitials(name) {
      if (!name) return '??'
      return name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
    },
    
    getRoleDisplayName(role) {
      const roles = {
        'ADMINISTRADOR': 'Administrador',
        'GERENCIA': 'Gerente',
        'USUARIO': 'Usuario'
      }
      return roles[role] || role
    },

    getDepartmentDisplayName(department) {
      const departments = {
        'RH': 'Recursos Humanos',
        'ADMINISTRACION': 'Administración',
        'COMERCIAL': 'Comercial',
        'OPERACIONES': 'Operaciones'
      }
      return departments[department] || department
    },
    
    formatDate(date) {
      if (!date) return 'Nunca'
      const d = new Date(date)
      return d.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    editUser(user) {
      this.editingUser = user
      this.userForm = {
        username: user.username || '',
        full_name: user.full_name,
        email: user.email,
        rol: user.rol,
        department: user.department || '',
        is_active: user.is_active,
        password: ''
      }
      this.showEditModal = true
    },
    
    async createUser() {
      this.isLoading = true
      try {
        const userData = {
          username: this.userForm.username,
          full_name: this.userForm.full_name,
          email: this.userForm.email,
          password: this.userForm.password,
          rol: this.userForm.rol,
          department: this.userForm.department || null,
          is_active: this.userForm.is_active
        }
        
        await userService.createUser(userData)
        await this.loadUsers()
        this.closeModal()
        this.showSuccessMessage('Usuario creado exitosamente')
      } catch (error) {
        console.error('Error creando usuario:', error)
        this.showErrorMessage('Error al crear el usuario: ' + error.message)
      } finally {
        this.isLoading = false
      }
    },
    
    async updateUser() {
      if (!this.editingUser) return
      
      this.isLoading = true
      try {
        const userData = {
          username: this.userForm.username,
          full_name: this.userForm.full_name,
          email: this.userForm.email,
          rol: this.userForm.rol,
          department: this.userForm.department || null,
          is_active: this.userForm.is_active
        }
        
        await userService.updateUser(this.editingUser.user_id, userData)
        await this.loadUsers()
        this.closeModal()
        this.showSuccessMessage('Usuario actualizado exitosamente')
      } catch (error) {
        console.error('Error actualizando usuario:', error)
        this.showErrorMessage('Error al actualizar el usuario: ' + error.message)
      } finally {
        this.isLoading = false
      }
    },
    
    async toggleUserStatus(user) {
      try {
        await userService.toggleUserStatus(user.user_id)
        await this.loadUsers()
        const action = !user.is_active ? 'activado' : 'desactivado'
        this.showSuccessMessage(`Usuario ${action} exitosamente`)
      } catch (error) {
        console.error('Error cambiando estado:', error)
        this.showErrorMessage('Error al cambiar el estado del usuario')
      }
    },
    
    async deleteUser(user) {
      if (confirm(`¿Estás seguro que deseas eliminar el usuario "${user.full_name}"?`)) {
        try {
          await userService.deleteUser(user.user_id)
          await this.loadUsers()
          this.showSuccessMessage('Usuario eliminado exitosamente')
        } catch (error) {
          console.error('Error eliminando usuario:', error)
          this.showErrorMessage('Error al eliminar el usuario')
        }
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingUser = null
      this.userForm = {
        username: '',
        full_name: '',
        email: '',
        rol: '',
        department: '',
        password: '',
        is_active: true
      }
    },
    
    showSuccessMessage(message) {
      alert(message)
    },

    showErrorMessage(message) {
      alert('Error: ' + message)
    }
  }
}
</script>