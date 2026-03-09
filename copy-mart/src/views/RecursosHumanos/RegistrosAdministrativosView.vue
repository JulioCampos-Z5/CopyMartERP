<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Registros Administrativos</h1>
          <p class="text-gray-600 mt-1">Retroalimentaciones, amonestaciones, actas administrativas y entrevistas de ausentismo</p>
        </div>
        <button @click="openCreateModal" class="btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Registro
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Retroalimentaciones</p>
          <p class="text-2xl font-bold text-blue-600">{{ statsByType.retroalimentacion_escrita }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Amonestaciones</p>
          <p class="text-2xl font-bold text-yellow-600">{{ statsByType.amonestacion }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Actas Administrativas</p>
          <p class="text-2xl font-bold text-red-600">{{ statsByType.acta_administrativa }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Entrevistas Ausentismo</p>
          <p class="text-2xl font-bold text-purple-600">{{ statsByType.entrevista_ausentismo }}</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <select v-model="filters.employeeId" class="input-field" @change="loadRecords">
            <option value="">Todos los empleados</option>
            <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
              ID: {{ emp.employee_id }} - {{ emp.rfc }}
            </option>
          </select>

          <select v-model="filters.type" class="input-field" @change="loadRecords">
            <option value="">Todos los tipos</option>
            <option value="retroalimentacion_escrita">Retroalimentación Escrita</option>
            <option value="amonestacion">Amonestación</option>
            <option value="acta_administrativa">Acta Administrativa</option>
            <option value="entrevista_ausentismo">Entrevista Ausentismo</option>
          </select>

          <button @click="loadRecords" class="btn-secondary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Recargar
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="text-gray-500 mt-4">Cargando registros...</p>
      </div>

      <!-- Table -->
      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empleado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descripción</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Días Susp.</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="filteredRecords.length === 0">
              <td colspan="7" class="px-6 py-8 text-center text-gray-500">No hay registros administrativos</td>
            </tr>
            <tr v-for="record in filteredRecords" :key="record.record_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm text-gray-900">{{ record.record_id }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">{{ getEmployeeName(record.employee_id) }}</td>
              <td class="px-6 py-4">
                <span :class="getTypeClass(record.type_administrative)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ getTypeLabel(record.type_administrative) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-700 max-w-xs truncate">{{ record.description }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">{{ record.suspended_days || 0 }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ formatDate(record.created_at) }}</td>
              <td class="px-6 py-4 text-sm">
                <button @click="editRecord(record)" class="text-blue-600 hover:text-blue-800 mr-3" title="Editar">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <h2 class="text-xl font-bold mb-4">{{ editingRecord ? 'Editar Registro' : 'Nuevo Registro Administrativo' }}</h2>

          <form @submit.prevent="saveRecord">
            <div class="space-y-4">
              <!-- Empleado -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Empleado *</label>
                <select v-model="form.employee_id" class="input-field" required :disabled="!!editingRecord">
                  <option value="">Seleccionar empleado</option>
                  <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
                    ID: {{ emp.employee_id }} - {{ emp.rfc }}
                  </option>
                </select>
              </div>

              <!-- Tipo -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Registro *</label>
                <select v-model="form.type_administrative" class="input-field" required>
                  <option value="">Seleccionar tipo</option>
                  <option value="retroalimentacion_escrita">Retroalimentación Escrita</option>
                  <option value="amonestacion">Amonestación</option>
                  <option value="acta_administrativa">Acta Administrativa</option>
                  <option value="entrevista_ausentismo">Entrevista de Ausentismo</option>
                </select>
              </div>

              <!-- Descripción -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descripción *</label>
                <textarea v-model="form.description" class="input-field" rows="4" required placeholder="Describa el incidente o motivo..."></textarea>
              </div>

              <!-- Días suspendidos -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Días de Suspensión</label>
                <input v-model.number="form.suspended_days" type="number" min="0" class="input-field" placeholder="0" />
              </div>

              <!-- Fechas de suspensión -->
              <div class="grid grid-cols-2 gap-4" v-if="form.suspended_days > 0">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Inicio Suspensión</label>
                  <input v-model="form.start_date" type="date" class="input-field" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Fin Suspensión</label>
                  <input v-model="form.end_date" type="date" class="input-field" />
                </div>
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Guardando...' : (editingRecord ? 'Actualizar' : 'Crear') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import rhService from '@/services/rhService';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const loading = ref(false);
const saving = ref(false);
const showModal = ref(false);
const editingRecord = ref(null);
const employees = ref([]);
const records = ref([]);

const filters = reactive({
  employeeId: '',
  type: ''
});

const form = reactive({
  employee_id: '',
  type_administrative: '',
  description: '',
  suspended_days: 0,
  start_date: '',
  end_date: ''
});

const statsByType = computed(() => {
  const stats = {
    retroalimentacion_escrita: 0,
    amonestacion: 0,
    acta_administrativa: 0,
    entrevista_ausentismo: 0
  };
  records.value.forEach(r => {
    if (stats[r.type_administrative] !== undefined) {
      stats[r.type_administrative]++;
    }
  });
  return stats;
});

const filteredRecords = computed(() => {
  return records.value.filter(r => {
    if (filters.type && r.type_administrative !== filters.type) return false;
    return true;
  });
});

function getTypeLabel(type) {
  const labels = {
    retroalimentacion_escrita: 'Retroalimentación Escrita',
    amonestacion: 'Amonestación',
    acta_administrativa: 'Acta Administrativa',
    entrevista_ausentismo: 'Entrevista Ausentismo'
  };
  return labels[type] || type;
}

function getTypeClass(type) {
  const classes = {
    retroalimentacion_escrita: 'bg-blue-100 text-blue-800',
    amonestacion: 'bg-yellow-100 text-yellow-800',
    acta_administrativa: 'bg-red-100 text-red-800',
    entrevista_ausentismo: 'bg-purple-100 text-purple-800'
  };
  return classes[type] || 'bg-gray-100 text-gray-800';
}

function getEmployeeName(empId) {
  const emp = employees.value.find(e => e.employee_id === empId);
  return emp ? `${emp.employee_id} - ${emp.rfc}` : `ID: ${empId}`;
}

function formatDate(dateStr) {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('es-MX');
}

function openCreateModal() {
  editingRecord.value = null;
  Object.assign(form, {
    employee_id: '',
    type_administrative: '',
    description: '',
    suspended_days: 0,
    start_date: '',
    end_date: ''
  });
  showModal.value = true;
}

function editRecord(record) {
  editingRecord.value = record;
  Object.assign(form, {
    employee_id: record.employee_id,
    type_administrative: record.type_administrative,
    description: record.description,
    suspended_days: record.suspended_days || 0,
    start_date: record.start_date || '',
    end_date: record.end_date || ''
  });
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  editingRecord.value = null;
}

async function loadEmployees() {
  try {
    employees.value = await rhService.employees.getAll({ is_active: true });
  } catch (e) {
    console.error('Error cargando empleados:', e);
  }
}

async function loadRecords() {
  loading.value = true;
  try {
    if (filters.employeeId) {
      records.value = await rhService.administrativeRecords.getByEmployee(Number(filters.employeeId));
    } else {
      // Load for all employees
      const allRecords = [];
      for (const emp of employees.value) {
        try {
          const empRecords = await rhService.administrativeRecords.getByEmployee(emp.employee_id);
          allRecords.push(...empRecords);
        } catch { /* skip */ }
      }
      records.value = allRecords.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    }
  } catch (e) {
    console.error('Error cargando registros:', e);
  } finally {
    loading.value = false;
  }
}

async function saveRecord() {
  saving.value = true;
  try {
    if (editingRecord.value) {
      await rhService.administrativeRecords.update(editingRecord.value.record_id, {
        type_administrative: form.type_administrative,
        description: form.description,
        suspended_days: form.suspended_days,
        start_date: form.start_date || undefined,
        end_date: form.end_date || undefined
      });
    } else {
      await rhService.administrativeRecords.create({
        employee_id: Number(form.employee_id),
        type_administrative: form.type_administrative,
        description: form.description,
        suspended_days: form.suspended_days,
        start_date: form.start_date || undefined,
        end_date: form.end_date || undefined,
        issued_by: authStore.user?.user_id || 1
      });
    }
    closeModal();
    await loadRecords();
  } catch (e) {
    console.error('Error guardando registro:', e);
    alert('Error al guardar el registro');
  } finally {
    saving.value = false;
  }
}

onMounted(async () => {
  await loadEmployees();
  await loadRecords();
});
</script>
