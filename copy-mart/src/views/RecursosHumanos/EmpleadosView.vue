<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Empleados</h1>
          <p class="text-gray-600 mt-1">Gestión de empleados y expedientes</p>
        </div>
        <button @click="showCreateModal = true" class="btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Empleado
        </button>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            v-model="filters.search"
            type="text"
            placeholder="Buscar por nombre, RFC, NSS..."
            class="input-field"
          />
          <select v-model="filters.isActive" class="input-field">
            <option value="">Todos los estados</option>
            <option value="true">Activos</option>
            <option value="false">Inactivos</option>
          </select>
          <button @click="loadEmployees" class="btn-secondary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Buscar
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">NSS</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RFC</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha Contratación</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="employee in filteredEmployees" :key="employee.employee_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ getEmployeeName(employee) }}</div>
                <div v-if="!employee.user_id" class="text-xs text-gray-400">Sin cuenta de usuario</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ employee.nss }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ employee.rfc }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(employee.hire_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                  employee.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                ]">
                  {{ employee.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button @click="viewEmployee(employee)" class="text-blue-600 hover:text-blue-900">
                  Ver
                </button>
                <button @click="editEmployee(employee)" class="text-indigo-600 hover:text-indigo-900">
                  Editar
                </button>
                <button @click="viewPayrolls(employee)" class="text-green-600 hover:text-green-900">
                  Nóminas
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-2/3 lg:w-1/2 shadow-lg rounded-md bg-white">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium">{{ editingEmployee ? 'Editar Empleado' : 'Nuevo Empleado' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="saveEmployee" class="space-y-4">
            <!-- Tipo de vinculación -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Vinculación</label>
              <div class="flex gap-4">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="radio" v-model="form.linkType" value="user" class="text-orange-600" />
                  <span class="text-sm">Usuario del sistema</span>
                </label>
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="radio" v-model="form.linkType" value="nombre" class="text-orange-600" />
                  <span class="text-sm">Sin cuenta (solo nombre)</span>
                </label>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-if="form.linkType === 'user'">
                <label class="block text-sm font-medium text-gray-700">Usuario</label>
                <select v-model.number="form.user_id" :required="form.linkType === 'user'" class="input-field">
                  <option value="">Seleccionar usuario</option>
                  <option v-for="user in users" :key="user.user_id" :value="user.user_id">
                    {{ user.full_name }}
                  </option>
                </select>
              </div>
              <div v-else>
                <label class="block text-sm font-medium text-gray-700">Nombre del Empleado</label>
                <input v-model="form.nombre" type="text" :required="form.linkType === 'nombre'" class="input-field" placeholder="Nombre completo" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">NSS</label>
                <input v-model="form.nss" type="text" required maxlength="11" class="input-field" placeholder="12345678901" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">RFC</label>
                <input v-model="form.rfc" type="text" required maxlength="13" class="input-field" placeholder="AAAA000000AAA" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">CURP</label>
                <input v-model="form.curp" type="text" required maxlength="18" class="input-field" placeholder="AAAA000000AAAAAA00" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Fecha de Nacimiento</label>
                <input v-model="form.birthday" type="date" required class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Fecha de Contratación</label>
                <input v-model="form.hire_date" type="date" required class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Teléfono de Emergencia</label>
                <input v-model="form.phone_emergency" type="tel" required class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Contacto de Emergencia</label>
                <input v-model="form.contact_emergency" type="text" required class="input-field" />
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
              <button type="submit" class="btn-primary">{{ editingEmployee ? 'Actualizar' : 'Crear' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseLayout from '@/components/BaseLayout.vue';
import rhService from '@/services/rhService';
import userService from '@/services/userService';

const router = useRouter();
const employees = ref([]);
const users = ref([]);
const showCreateModal = ref(false);
const editingEmployee = ref(null);

const filters = ref({
  search: '',
  isActive: ''
});

const form = ref({
  linkType: 'user',
  user_id: '',
  nombre: '',
  nss: '',
  rfc: '',
  curp: '',
  birthday: '',
  hire_date: '',
  phone_emergency: '',
  contact_emergency: ''
});

const getEmployeeName = (employee) => {
  return employee.user?.full_name || employee.nombre || employee.rfc;
};

const filteredEmployees = computed(() => {
  let result = employees.value;

  if (filters.value.search) {
    const search = filters.value.search.toLowerCase();
    result = result.filter(emp =>
      (emp.user?.full_name || '').toLowerCase().includes(search) ||
      (emp.nombre || '').toLowerCase().includes(search) ||
      emp.nss.toLowerCase().includes(search) ||
      emp.rfc.toLowerCase().includes(search) ||
      emp.curp.toLowerCase().includes(search)
    );
  }
  
  if (filters.value.isActive !== '') {
    const isActive = filters.value.isActive === 'true';
    result = result.filter(emp => emp.is_active === isActive);
  }
  
  return result;
});

const loadEmployees = async () => {
  try {
    const params = {};
    if (filters.value.isActive !== '') {
      params.is_active = filters.value.isActive === 'true';
    }
    employees.value = await rhService.employees.getAll(params);
  } catch (error) {
    console.error('Error loading employees:', error);
  }
};

const loadUsers = async () => {
  try {
    users.value = await userService.getAll();
  } catch (error) {
    console.error('Error loading users:', error);
  }
};

const viewEmployee = async (employee) => {
  router.push(`/recursos-humanos/empleados/${employee.employee_id}`);
};

const editEmployee = (employee) => {
  editingEmployee.value = employee;
  form.value = {
    linkType: employee.user_id ? 'user' : 'nombre',
    user_id: employee.user_id || '',
    nombre: employee.nombre || '',
    nss: employee.nss,
    rfc: employee.rfc,
    curp: employee.curp,
    birthday: employee.birthday,
    hire_date: employee.hire_date,
    phone_emergency: employee.phone_emergency,
    contact_emergency: employee.contact_emergency
  };
  showCreateModal.value = true;
};

const viewPayrolls = (employee) => {
  router.push(`/recursos-humanos/empleados/${employee.employee_id}/nominas`);
};

const saveEmployee = async () => {
  try {
    const payload = {
      nss: String(form.value.nss || '').replace(/\D/g, ''),
      rfc: String(form.value.rfc || '').trim().toUpperCase(),
      curp: String(form.value.curp || '').trim().toUpperCase(),
      birthday: form.value.birthday,
      hire_date: form.value.hire_date,
      phone_emergency: String(form.value.phone_emergency || '').trim(),
      contact_emergency: String(form.value.contact_emergency || '').trim(),
      user_id: form.value.linkType === 'user' && form.value.user_id ? Number(form.value.user_id) : null,
      nombre: form.value.linkType === 'nombre' ? String(form.value.nombre || '').trim() : null
    };

    if (editingEmployee.value) {
      await rhService.employees.update(editingEmployee.value.employee_id, payload);
    } else {
      await rhService.employees.create(payload);
    }
    closeModal();
    loadEmployees();
  } catch (error) {
    console.error('Error saving employee:', error);
    alert(`Error al guardar el empleado: ${error?.response?.data?.detail || error?.message || 'Error desconocido'}`);
  }
};

const closeModal = () => {
  showCreateModal.value = false;
  editingEmployee.value = null;
  form.value = {
    linkType: 'user',
    user_id: '',
    nombre: '',
    nss: '',
    rfc: '',
    curp: '',
    birthday: '',
    hire_date: '',
    phone_emergency: '',
    contact_emergency: ''
  };
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('es-MX');
};

onMounted(() => {
  loadEmployees();
  loadUsers();
});
</script>
