<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-purple-800 mb-2">Gestión de Usuarios</h1>
              <p class="text-purple-600">Administración de usuarios del sistema</p>
            </div>
            <button
              @click="openCreateModal"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Usuario
            </button>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Usuarios</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ users.length }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Usuarios Activos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ activeUsersCount }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Administradores</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ adminCount }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Usuarios Inactivos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ inactiveUsersCount }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <input
                v-model="searchTerm"
                type="text"
                placeholder="Buscar por nombre o email..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            <div>
              <select
                v-model="filterRole"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Todos los roles</option>
                <option value="administrador">Administrador</option>
                <option value="gerencia">Gerencia</option>
                <option value="usuario">Usuario</option>
              </select>
            </div>
            <div>
              <select
                v-model="filterStatus"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Todos los estados</option>
                <option value="active">Activos</option>
                <option value="inactive">Inactivos</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Users Table -->
        <div class="bg-white rounded-lg shadow border overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Usuario
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rol
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Departamento
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha Creación
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="loadingUsers">
                  <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                    Cargando usuarios...
                  </td>
                </tr>
                <tr v-else-if="filteredUsers.length === 0">
                  <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                    No se encontraron usuarios
                  </td>
                </tr>
                <tr v-else v-for="user in filteredUsers" :key="user.user_id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10">
                        <div class="h-10 w-10 rounded-full bg-purple-100 flex items-center justify-center">
                          <span class="text-purple-600 font-semibold text-sm">
                            {{ getInitials(user.full_name) }}
                          </span>
                        </div>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">
                          {{ user.full_name }}
                        </div>
                        <div class="text-sm text-gray-500">
                          {{ user.email }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ user.email }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getRoleBadgeClass(user.rol)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ getRoleLabel(user.rol) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span v-if="user.department" class="text-sm text-gray-900">
                      {{ getDepartmentLabel(user.department) }}
                    </span>
                    <span v-else class="text-sm text-gray-400">-</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      :class="user.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'"
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    >
                      {{ user.is_active ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(user.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      @click="editUser(user)"
                      class="text-purple-600 hover:text-purple-900 mr-3"
                      title="Editar"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      @click="openResetPassword(user)"
                      class="text-blue-600 hover:text-blue-900 mr-3"
                      title="Restablecer Contraseña"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                      </svg>
                    </button>
                    <button
                      @click="toggleUserStatus(user)"
                      :class="user.is_active ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'"
                      :title="user.is_active ? 'Desactivar' : 'Activar'"
                    >
                      <svg v-if="user.is_active" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                      </svg>
                      <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">
            {{ editingUser ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </h3>
          <form @submit.prevent="saveUser" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Nombre Completo *
                </label>
                <input
                  v-model="formData.full_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
                <input
                  v-model="formData.email"
                  type="email"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Rol *
                </label>
                <select
                  v-model="formData.rol"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">Seleccionar...</option>
                  <option value="administrador">Administrador</option>
                  <option value="gerencia">Gerencia</option>
                  <option value="usuario">Usuario</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Departamento
                </label>
                <select
                  v-model="formData.department"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">Seleccionar...</option>
                  <option value="rh">Recursos Humanos</option>
                  <option value="administracion">Administración</option>
                  <option value="comercial">Comercial</option>
                  <option value="operaciones">Operaciones</option>
                </select>
              </div>
              <div v-if="!editingUser">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Contraseña *
                </label>
                <input
                  v-model="formData.password"
                  type="password"
                  :required="!editingUser"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              <div class="flex items-center">
                <input
                  v-model="formData.is_active"
                  type="checkbox"
                  class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                />
                <label class="ml-2 block text-sm text-gray-900">
                  Usuario Activo
                </label>
              </div>
            </div>

            <!-- Permisos Granulares -->
            <div class="mt-6 border-t pt-4">
              <h4 class="text-md font-semibold text-gray-900 mb-3">Permisos por Área</h4>
              <p class="text-sm text-gray-600 mb-3">Selecciona las áreas a las que este usuario tendrá acceso:</p>
              <div class="space-y-2">
                <div v-for="area in availableAreas" :key="area.id" class="border border-gray-200 rounded-lg">
                  <!-- Checkbox del área -->
                  <div class="bg-gray-50 p-3 hover:bg-gray-100 transition-colors">
                    <label class="flex items-center cursor-pointer">
                      <input
                        v-model="selectedAreas[area.id]"
                        type="checkbox"
                        @change="toggleArea(area.id)"
                        class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                      />
                      <span class="ml-2 font-medium text-gray-900">{{ area.label }}</span>
                    </label>
                  </div>
                  
                  <!-- Permisos específicos (solo si el área está seleccionada) -->
                  <div v-if="selectedAreas[area.id]" class="bg-white p-4 border-t border-gray-200">
                    <p class="text-xs text-gray-600 mb-2">Permisos para {{ area.label }}:</p>
                    <div class="grid grid-cols-2 gap-3">
                      <label class="flex items-center text-sm">
                        <input
                          v-model="formData.permissions[area.id].view"
                          type="checkbox"
                          class="mr-2 h-4 w-4 text-purple-600 rounded"
                        />
                        <span class="text-gray-700">👁️ Ver</span>
                      </label>
                      <label class="flex items-center text-sm">
                        <input
                          v-model="formData.permissions[area.id].create"
                          type="checkbox"
                          class="mr-2 h-4 w-4 text-green-600 rounded"
                        />
                        <span class="text-gray-700">➕ Crear</span>
                      </label>
                      <label class="flex items-center text-sm">
                        <input
                          v-model="formData.permissions[area.id].edit"
                          type="checkbox"
                          class="mr-2 h-4 w-4 text-blue-600 rounded"
                        />
                        <span class="text-gray-700">✏️ Editar</span>
                      </label>
                      <label class="flex items-center text-sm">
                        <input
                          v-model="formData.permissions[area.id].delete"
                          type="checkbox"
                          class="mr-2 h-4 w-4 text-red-600 rounded"
                        />
                        <span class="text-gray-700">🗑️ Eliminar</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
              >
                {{ saving ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Reset Password Modal -->
    <div v-if="showResetPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Restablecer Contraseña</h3>
        <p class="text-sm text-gray-600 mb-4">Usuario: <strong>{{ resetPasswordUser?.full_name }}</strong></p>
        <form @submit.prevent="submitResetPassword">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Nueva Contraseña *</label>
            <input v-model="resetPasswordForm.new_password" type="password" required minlength="6" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" placeholder="Mínimo 6 caracteres">
          </div>
          <div class="flex justify-end gap-3">
            <button type="button" @click="showResetPasswordModal = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="saving" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">Restablecer</button>
          </div>
        </form>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { userService } from '@/services/userService'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'UsuariosView',
  components: {
    BaseLayout
  },
  data() {
    return {
      users: [],
      loadingUsers: false,
      searchTerm: '',
      filterRole: '',
      filterStatus: '',
      showModal: false,
      editingUser: null,
      saving: false,
      showResetPasswordModal: false,
      resetPasswordUser: null,
      resetPasswordForm: { new_password: '' },
      formData: {
        full_name: '',
        email: '',
        rol: '',
        department: '',
        password: '',
        is_active: true,
        permissions: {}
      },
      selectedAreas: {},
      availableAreas: [
        { id: 'ventas', label: 'Ventas' },
        { id: 'rentas', label: 'Rentas' },
        { id: 'clientes', label: 'Clientes' },
        { id: 'produccion', label: 'Producción' },
        { id: 'compras', label: 'Compras' },
        { id: 'almacen', label: 'Almacén' },
        { id: 'cobranza', label: 'Cobranza' },
        { id: 'facturacion', label: 'Facturación' },
        { id: 'inventario', label: 'Inventario' },
        { id: 'rutas', label: 'Rutas' },
        { id: 'ordenes_servicio', label: 'Órdenes de Servicio' },
        { id: 'taller', label: 'Taller' },
        { id: 'recursos_humanos', label: 'Recursos Humanos' },
        { id: 'ti', label: 'Tecnologías de la Información' },
        { id: 'usuarios', label: 'Usuarios' },
      ]
    }
  },
  computed: {
    activeUsersCount() {
      return this.users.filter(u => u.is_active).length
    },
    inactiveUsersCount() {
      return this.users.filter(u => !u.is_active).length
    },
    adminCount() {
      return this.users.filter(u => u.rol === 'administrador').length
    },
    filteredUsers() {
      return this.users.filter(user => {
        const matchesSearch = !this.searchTerm ||
          user.full_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchTerm.toLowerCase())

        const matchesRole = !this.filterRole || user.rol === this.filterRole

        const matchesStatus = !this.filterStatus ||
          (this.filterStatus === 'active' && user.is_active) ||
          (this.filterStatus === 'inactive' && !user.is_active)

        return matchesSearch && matchesRole && matchesStatus
      })
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loadingUsers = true
      try {
        this.users = await userService.getAll()
      } catch (error) {
        console.error('Error loading users:', error)
        alert('Error al cargar los usuarios')
      } finally {
        this.loadingUsers = false
      }
    },
    toggleArea(areaId) {
      if (this.selectedAreas[areaId]) {
        // Área seleccionada: activar todos los permisos
        this.formData.permissions[areaId] = {
          view: true,
          create: true,
          edit: true,
          delete: true
        }
      } else {
        // Área deseleccionada: limpiar permisos
        delete this.formData.permissions[areaId]
      }
    },
    openCreateModal() {
      this.editingUser = null
      // Inicializar permisos vacíos y áreas no seleccionadas
      const permissions = {}
      const selectedAreas = {}
      this.availableAreas.forEach(area => {
        permissions[area.id] = { view: false, create: false, edit: false, delete: false }
        selectedAreas[area.id] = false
      })
      this.selectedAreas = selectedAreas
      this.formData = {
        full_name: '',
        email: '',
        rol: '',
        department: '',
        password: '',
        is_active: true,
        permissions
      }
      this.showModal = true
    },
    editUser(user) {
      this.editingUser = user
      // Inicializar permisos con valores del usuario o vacíos
      const permissions = {}
      const selectedAreas = {}
      this.availableAreas.forEach(area => {
        const hasPermissions = user.permissions?.[area.id]
        // Marcar área como seleccionada si tiene algún permiso
        if (hasPermissions) {
          selectedAreas[area.id] = true
          permissions[area.id] = { ...user.permissions[area.id] }
        } else {
          selectedAreas[area.id] = false
          permissions[area.id] = { view: false, create: false, edit: false, delete: false }
        }
      })
      this.selectedAreas = selectedAreas
      this.formData = {
        full_name: user.full_name,
        email: user.email,
        rol: user.rol,
        department: user.department || '',
        password: '',
        is_active: user.is_active,
        permissions
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.editingUser = null
    },
    async saveUser() {
      this.saving = true
      try {
        // Filtrar solo los permisos de áreas seleccionadas
        const filteredPermissions = {}
        this.availableAreas.forEach(area => {
          if (this.selectedAreas[area.id]) {
            filteredPermissions[area.id] = this.formData.permissions[area.id]
          }
        })

        if (this.editingUser) {
          // Update existing user
          const updateData = {
            full_name: this.formData.full_name,
            email: this.formData.email,
            rol: this.formData.rol,
            department: this.formData.department || null,
            is_active: this.formData.is_active,
            permissions: filteredPermissions
          }
          await userService.updateUser(this.editingUser.user_id, updateData)

          // If editing the current logged-in user, update localStorage and store
          const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
          if (storedUser.user_id === this.editingUser.user_id) {
            storedUser.permissions = filteredPermissions
            storedUser.full_name = updateData.full_name
            storedUser.email = updateData.email
            storedUser.rol = updateData.rol
            storedUser.department = updateData.department
            localStorage.setItem('user', JSON.stringify(storedUser))
            try {
              const authStore = useAuthStore()
              authStore.user = storedUser
            } catch (e) { /* ignore */ }
          }
        } else {
          // Create new user
          await userService.createUser({
            ...this.formData,
            permissions: filteredPermissions
          })
        }
        await this.loadUsers()
        this.closeModal()
      } catch (error) {
        console.error('Error saving user:', error)
        alert('Error al guardar el usuario: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    },
    async toggleUserStatus(user) {
      const action = user.is_active ? 'desactivar' : 'activar'
      if (!confirm(`¿Estás seguro de ${action} este usuario?`)) {
        return
      }

      try {
        await userService.updateUser(user.user_id, {
          is_active: !user.is_active
        })
        await this.loadUsers()
      } catch (error) {
        console.error('Error updating user status:', error)
        alert('Error al actualizar el estado del usuario')
      }
    },
    openResetPassword(user) {
      this.resetPasswordUser = user
      this.resetPasswordForm.new_password = ''
      this.showResetPasswordModal = true
    },
    async submitResetPassword() {
      if (!this.resetPasswordForm.new_password || this.resetPasswordForm.new_password.length < 6) {
        alert('La contraseña debe tener al menos 6 caracteres')
        return
      }
      this.saving = true
      try {
        await userService.adminResetPassword(this.resetPasswordUser.user_id, this.resetPasswordForm.new_password)
        alert('Contraseña restablecida exitosamente')
        this.showResetPasswordModal = false
      } catch (error) {
        alert('Error al restablecer contraseña: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    },
    getInitials(name) {
      if (!name) return '??'
      const parts = name.split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    },
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('es-MX', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    getRoleLabel(rol) {
      const labels = {
        'administrador': 'Administrador',
        'gerencia': 'Gerencia',
        'usuario': 'Usuario'
      }
      return labels[rol] || rol
    },
    getRoleBadgeClass(rol) {
      const classes = {
        'administrador': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
        'gerencia': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'usuario': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
      }
      return classes[rol] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    },
    getDepartmentLabel(dept) {
      const labels = {
        'rh': 'Recursos Humanos',
        'administracion': 'Administración',
        'comercial': 'Comercial',
        'operaciones': 'Operaciones'
      }
      return labels[dept] || dept
    }
  }
}
</script>
