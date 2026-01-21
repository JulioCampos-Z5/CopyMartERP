<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Nóminas</h1>
          <p class="text-gray-600 mt-1">Control de pagos y nómina del personal</p>
        </div>
        <button @click="showCreateModal = true" class="btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Nómina
        </button>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
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
            <option value="ACTIVO">Activo</option>
            <option value="PAGADO">Pagado</option>
            <option value="RECHAZADO">Rechazado</option>
          </select>
          
          <input v-model="filters.startDate" type="date" class="input-field" placeholder="Fecha inicio" />
          <input v-model="filters.endDate" type="date" class="input-field" placeholder="Fecha fin" />
        </div>
        <button @click="loadPayrolls" class="btn-secondary mt-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Buscar
        </button>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white p-4 rounded-lg shadow border-l-4 border-yellow-500">
          <h3 class="text-sm font-medium text-gray-500">Pendientes</h3>
          <p class="text-2xl font-bold text-gray-900">{{ stats.pending }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow border-l-4 border-green-500">
          <h3 class="text-sm font-medium text-gray-500">Aprobadas</h3>
          <p class="text-2xl font-bold text-gray-900">{{ stats.approved }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow border-l-4 border-blue-500">
          <h3 class="text-sm font-medium text-gray-500">Pagadas</h3>
          <p class="text-2xl font-bold text-gray-900">{{ stats.paid }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow border-l-4 border-indigo-500">
          <h3 class="text-sm font-medium text-gray-500">Total Mes</h3>
          <p class="text-2xl font-bold text-gray-900">${{ stats.totalAmount.toLocaleString() }}</p>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empleado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Salario</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bonos</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Comisiones</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Pago</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="payroll in filteredPayrolls" :key="payroll.payroll_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ payroll.payroll_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ getEmployeeName(payroll.employee_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ payroll.salary.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ payroll.bonus.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ payroll.commission.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                ${{ (payroll.salary + payroll.bonus + payroll.commission).toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(payroll.pay_day) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusClass(payroll.status)">
                  {{ payroll.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button @click="editPayroll(payroll)" class="text-indigo-600 hover:text-indigo-900">
                  Editar
                </button>
                <button v-if="payroll.status === 'PENDIENTE'" @click="updateStatus(payroll.payroll_id, 'APROBADO')" class="text-green-600 hover:text-green-900">
                  Aprobar
                </button>
                <button v-if="payroll.status === 'APROBADO'" @click="updateStatus(payroll.payroll_id, 'PAGADO')" class="text-blue-600 hover:text-blue-900">
                  Pagar
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
            <h3 class="text-lg font-medium">{{ editingPayroll ? 'Editar Nómina' : 'Nueva Nómina' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="savePayroll" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Empleado</label>
              <select v-model="form.employee_id" required class="input-field" :disabled="editingPayroll">
                <option value="">Seleccionar empleado</option>
                <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
                  ID: {{ emp.employee_id }} - {{ emp.rfc }}
                </option>
              </select>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Salario Base</label>
                <input v-model.number="form.salary" type="number" step="0.01" required class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Fecha de Pago</label>
                <input v-model="form.pay_day" type="date" required class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Bonos</label>
                <input v-model.number="form.bonus" type="number" step="0.01" class="input-field" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Comisiones</label>
                <input v-model.number="form.commission" type="number" step="0.01" class="input-field" />
              </div>
            </div>
            
            <div class="bg-gray-50 p-4 rounded">
              <div class="flex justify-between items-center">
                <span class="text-lg font-medium text-gray-700">Total a Pagar:</span>
                <span class="text-2xl font-bold text-indigo-600">
                  ${{ (form.salary + form.bonus + form.commission).toLocaleString() }}
                </span>
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
              <button type="submit" class="btn-primary">{{ editingPayroll ? 'Actualizar' : 'Crear' }}</button>
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

const payrolls = ref([]);
const employees = ref([]);
const showCreateModal = ref(false);
const editingPayroll = ref(null);

const filters = ref({
  employeeId: '',
  status: '',
  startDate: '',
  endDate: ''
});

const form = ref({
  employee_id: '',
  salary: 0,
  pay_day: '',
  bonus: 0,
  commission: 0
});

const stats = computed(() => {
  return {
    pending: payrolls.value.filter(p => p.status === 'PENDIENTE').length,
    approved: payrolls.value.filter(p => p.status === 'APROBADO').length,
    paid: payrolls.value.filter(p => p.status === 'PAGADO').length,
    totalAmount: payrolls.value
      .filter(p => p.status === 'PAGADO')
      .reduce((sum, p) => sum + p.salary + p.bonus + p.commission, 0)
  };
});

const filteredPayrolls = computed(() => {
  let result = payrolls.value;
  
  if (filters.value.employeeId) {
    result = result.filter(p => p.employee_id === parseInt(filters.value.employeeId));
  }
  
  if (filters.value.status) {
    result = result.filter(p => p.status === filters.value.status);
  }
  
  return result;
});

const loadPayrolls = async () => {
  try {
    // Cargar todas las nóminas
    const allPayrolls = [];
    for (const emp of employees.value) {
      const empPayrolls = await rhService.payrolls.getByEmployee(emp.employee_id);
      allPayrolls.push(...empPayrolls);
    }
    payrolls.value = allPayrolls;
  } catch (error) {
    console.error('Error loading payrolls:', error);
  }
};

const loadEmployees = async () => {
  try {
    employees.value = await rhService.employees.getAll({ is_active: true });
  } catch (error) {
    console.error('Error loading employees:', error);
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
    'PAGADO': 'px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800',
    'RECHAZADO': 'px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800',
    'ACTIVO': 'px-2 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800'
  };
  return classes[status] || 'px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800';
};

const editPayroll = (payroll) => {
  editingPayroll.value = payroll;
  form.value = {
    employee_id: payroll.employee_id,
    salary: payroll.salary,
    pay_day: payroll.pay_day,
    bonus: payroll.bonus || 0,
    commission: payroll.commission || 0
  };
  showCreateModal.value = true;
};

const updateStatus = async (payrollId, newStatus) => {
  try {
    await rhService.payrolls.update(payrollId, { status: newStatus });
    loadPayrolls();
  } catch (error) {
    console.error('Error updating status:', error);
    alert('Error al actualizar el estado');
  }
};

const savePayroll = async () => {
  try {
    if (editingPayroll.value) {
      await rhService.payrolls.update(editingPayroll.value.payroll_id, form.value);
    } else {
      await rhService.payrolls.create(form.value);
    }
    closeModal();
    loadPayrolls();
  } catch (error) {
    console.error('Error saving payroll:', error);
    alert('Error al guardar la nómina');
  }
};

const closeModal = () => {
  showCreateModal.value = false;
  editingPayroll.value = null;
  form.value = {
    employee_id: '',
    salary: 0,
    pay_day: '',
    bonus: 0,
    commission: 0
  };
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('es-MX');
};

onMounted(async () => {
  await loadEmployees();
  await loadPayrolls();
});
</script>
