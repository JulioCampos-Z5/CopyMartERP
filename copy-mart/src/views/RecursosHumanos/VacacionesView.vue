<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Vacaciones</h1>
          <p class="text-gray-600 mt-1">Solicitudes y control de vacaciones</p>
        </div>
        <button @click="showCreateModal = true" class="btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Solicitud
        </button>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <select v-model="filters.employeeId" class="input-field">
            <option value="">Todos los empleados</option>
            <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
              ID: {{ emp.employee_id }} - {{ emp.rfc }}
            </option>
          </select>
          
          <select v-model="filters.status" class="input-field">
            <option value="">Todos los estados</option>
            <option value="PENDIENTE">Pendiente</option>
            <option value="APROBADO">Aprobado</option>
            <option value="RECHAZADO">Rechazado</option>
          </select>
          
          <button @click="loadVacations" class="btn-secondary">
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
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empleado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Días</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Inicio</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Fin</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Notas</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="vacation in filteredVacations" :key="vacation.vacation_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ vacation.vacation_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ getEmployeeName(vacation.employee_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-semibold">
                {{ vacation.vacation_days }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(vacation.start_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(vacation.end_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusClass(vacation.status)">
                  {{ vacation.status }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                {{ vacation.notes || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button v-if="vacation.status === 'PENDIENTE'" @click="updateStatus(vacation.vacation_id, 'APROBADO')" class="text-green-600 hover:text-green-900">
                  Aprobar
                </button>
                <button v-if="vacation.status === 'PENDIENTE'" @click="updateStatus(vacation.vacation_id, 'RECHAZADO')" class="text-red-600 hover:text-red-900">
                  Rechazar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-2/3 lg:w-1/2 shadow-lg rounded-md bg-white">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium">Nueva Solicitud de Vacaciones</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="saveVacation" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Empleado</label>
              <select v-model="form.employee_id" @change="loadVacationDays" required class="input-field">
                <option value="">Seleccionar empleado</option>
                <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
                  ID: {{ emp.employee_id }} - {{ emp.rfc }}
                </option>
              </select>
              <p v-if="availableDays !== null" class="mt-1 text-sm text-gray-500">
                Días disponibles: <span class="font-semibold">{{ availableDays }}</span>
              </p>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Fecha Inicio</label>
                <input v-model="form.start_date" type="date" required class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Fecha Fin</label>
                <input v-model="form.end_date" type="date" required class="input-field" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Días Solicitados</label>
              <input v-model.number="form.vacation_days" type="number" min="1" required class="input-field" />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Notas (Opcional)</label>
              <textarea v-model="form.notes" rows="3" class="input-field"></textarea>
            </div>
            
            <div class="flex justify-end space-x-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
              <button type="submit" class="btn-primary">Crear Solicitud</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import rhService from '@/services/rhService';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const vacations = ref([]);
const employees = ref([]);
const showCreateModal = ref(false);
const availableDays = ref(null);

const filters = ref({
  employeeId: '',
  status: ''
});

const form = ref({
  employee_id: '',
  vacation_days: 1,
  start_date: '',
  end_date: '',
  notes: '',
  requested_by: authStore.user?.user_id || 1
});

const filteredVacations = computed(() => {
  let result = vacations.value;
  
  if (filters.value.employeeId) {
    result = result.filter(v => v.employee_id === parseInt(filters.value.employeeId));
  }
  
  if (filters.value.status) {
    result = result.filter(v => v.status === filters.value.status);
  }
  
  return result;
});

const loadVacations = async () => {
  try {
    const allVacations = [];
    for (const emp of employees.value) {
      const empVacations = await rhService.vacations.getByEmployee(emp.employee_id);
      allVacations.push(...empVacations);
    }
    vacations.value = allVacations;
  } catch (error) {
    console.error('Error loading vacations:', error);
  }
};

const loadEmployees = async () => {
  try {
    employees.value = await rhService.employees.getAll({ is_active: true });
  } catch (error) {
    console.error('Error loading employees:', error);
  }
};

const loadVacationDays = async () => {
  if (!form.value.employee_id) {
    availableDays.value = null;
    return;
  }
  
  try {
    const data = await rhService.vacations.getVacationDays(form.value.employee_id);
    availableDays.value = data.available_days || 0;
  } catch (error) {
    console.error('Error loading vacation days:', error);
    availableDays.value = 0;
  }
};

const getEmployeeName = (employeeId) => {
  const emp = employees.value.find(e => e.employee_id === employeeId);
  return emp ? `${emp.rfc} (ID: ${employeeId})` : `ID: ${employeeId}`;
};

const getStatusClass = (status) => {
  const classes = {
    'PENDIENTE': 'px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800',
    'APROBADO': 'px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800',
    'RECHAZADO': 'px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800'
  };
  return classes[status] || 'px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800';
};

const updateStatus = async (vacationId, newStatus) => {
  try {
    await rhService.vacations.update(vacationId, { status: newStatus });
    loadVacations();
  } catch (error) {
    console.error('Error updating status:', error);
    alert('Error al actualizar el estado');
  }
};

const saveVacation = async () => {
  try {
    await rhService.vacations.create(form.value);
    closeModal();
    loadVacations();
  } catch (error) {
    console.error('Error saving vacation:', error);
    alert('Error al guardar la solicitud de vacaciones');
  }
};

const closeModal = () => {
  showCreateModal.value = false;
  availableDays.value = null;
  form.value = {
    employee_id: '',
    vacation_days: 1,
    start_date: '',
    end_date: '',
    notes: '',
    requested_by: authStore.user?.user_id || 1
  };
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('es-MX');
};

onMounted(async () => {
  await loadEmployees();
  await loadVacations();
});
</script>
