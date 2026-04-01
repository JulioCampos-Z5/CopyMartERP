<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Ausentismo</h1>
          <p class="text-gray-600 mt-1">Control de inasistencias de empleados</p>
        </div>
        <button @click="openCreateModal" class="btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Registrar Inasistencia
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Enfermedad</p>
          <p class="text-2xl font-bold text-blue-600">{{ statsByType.enfermedad }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Ausentismo</p>
          <p class="text-2xl font-bold text-red-600">{{ statsByType.ausentismo }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Permiso Personal</p>
          <p class="text-2xl font-bold text-yellow-600">{{ statsByType.permiso_personal }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Pendientes</p>
          <p class="text-2xl font-bold text-orange-600">{{ pendingCount }}</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <select v-model="filters.employeeId" class="input-field" @change="loadAbsences">
            <option value="">Todos los empleados</option>
            <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
              {{ emp.user?.full_name || emp.nombre || emp.rfc }}
            </option>
          </select>

          <select v-model="filters.type" class="input-field">
            <option value="">Todos los tipos</option>
            <option value="enfermedad">Enfermedad</option>
            <option value="ausentismo">Ausentismo</option>
            <option value="permiso_personal">Permiso Personal</option>
            <option value="otro">Otro</option>
          </select>

          <select v-model="filters.status" class="input-field">
            <option value="">Todos los estados</option>
            <option value="pendiente">Pendiente</option>
            <option value="aprobado">Aprobado</option>
            <option value="rechazado">Rechazado</option>
          </select>

          <button @click="loadAbsences" class="btn-secondary">
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
        <p class="text-gray-500 mt-4">Cargando inasistencias...</p>
      </div>

      <!-- Table -->
      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empleado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Inicio</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Fin</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Justificada</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="filteredAbsences.length === 0">
              <td colspan="8" class="px-6 py-8 text-center text-gray-500">No hay inasistencias registradas</td>
            </tr>
            <tr v-for="absence in filteredAbsences" :key="absence.absence_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm text-gray-900">{{ absence.absence_id }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">{{ getEmployeeName(absence.employee_id) }}</td>
              <td class="px-6 py-4">
                <span :class="getAbsenceTypeClass(absence.absence_type)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ getAbsenceTypeLabel(absence.absence_type) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ formatDate(absence.start_date) }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ formatDate(absence.end_date) }}</td>
              <td class="px-6 py-4 text-sm">
                <span v-if="absence.is_justified" class="text-green-600 font-medium">Sí</span>
                <span v-else class="text-red-600 font-medium">No</span>
              </td>
              <td class="px-6 py-4">
                <span :class="getStatusClass(absence.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ getStatusLabel(absence.status) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm flex gap-2">
                <button @click="editAbsence(absence)" class="text-blue-600 hover:text-blue-800" title="Editar">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button v-if="absence.status === 'pendiente'" @click="updateStatus(absence, 'aprobado')" class="text-green-600 hover:text-green-800" title="Aprobar">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
                <button v-if="absence.status === 'pendiente'" @click="updateStatus(absence, 'rechazado')" class="text-red-600 hover:text-red-800" title="Rechazar">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
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
          <h2 class="text-xl font-bold mb-4">{{ editingAbsence ? 'Editar Inasistencia' : 'Registrar Inasistencia' }}</h2>

          <form @submit.prevent="saveAbsence">
            <div class="space-y-4">
              <!-- Empleado -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Empleado *</label>
                <select v-model="form.employee_id" class="input-field" required :disabled="!!editingAbsence">
                  <option value="">Seleccionar empleado</option>
                  <option v-for="emp in employees" :key="emp.employee_id" :value="emp.employee_id">
                    {{ emp.user?.full_name || emp.nombre || emp.rfc }}
                  </option>
                </select>
              </div>

              <!-- Tipo -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Inasistencia *</label>
                <select v-model="form.absence_type" class="input-field" required>
                  <option value="">Seleccionar tipo</option>
                  <option value="enfermedad">Enfermedad</option>
                  <option value="ausentismo">Ausentismo</option>
                  <option value="permiso_personal">Permiso Personal</option>
                  <option value="otro">Otro</option>
                </select>
              </div>

              <!-- Fechas -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Inicio *</label>
                  <input v-model="form.start_date" type="date" class="input-field" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Fin *</label>
                  <input v-model="form.end_date" type="date" class="input-field" required />
                </div>
              </div>

              <!-- Justificada -->
              <div class="flex items-center gap-2">
                <input v-model="form.is_justified" type="checkbox" id="justified" class="rounded border-gray-300" />
                <label for="justified" class="text-sm font-medium text-gray-700">Justificada</label>
              </div>

              <!-- Justificación -->
              <div v-if="form.is_justified">
                <label class="block text-sm font-medium text-gray-700 mb-1">Justificación</label>
                <textarea v-model="form.justification" class="input-field" rows="3" placeholder="Describa la justificación..."></textarea>
              </div>

              <!-- Notas -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
                <textarea v-model="form.notes" class="input-field" rows="2" placeholder="Notas adicionales..."></textarea>
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Guardando...' : (editingAbsence ? 'Actualizar' : 'Registrar') }}
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
const editingAbsence = ref(null);
const employees = ref([]);
const absences = ref([]);

const filters = reactive({
  employeeId: '',
  type: '',
  status: ''
});

const form = reactive({
  employee_id: '',
  absence_type: '',
  start_date: '',
  end_date: '',
  is_justified: false,
  justification: '',
  notes: ''
});

const statsByType = computed(() => {
  const stats = { enfermedad: 0, ausentismo: 0, permiso_personal: 0, otro: 0 };
  absences.value.forEach(a => {
    if (stats[a.absence_type] !== undefined) stats[a.absence_type]++;
  });
  return stats;
});

const pendingCount = computed(() => absences.value.filter(a => a.status === 'pendiente').length);

const filteredAbsences = computed(() => {
  return absences.value.filter(a => {
    if (filters.type && a.absence_type !== filters.type) return false;
    if (filters.status && a.status !== filters.status) return false;
    return true;
  });
});

function getAbsenceTypeLabel(type) {
  const labels = {
    enfermedad: 'Enfermedad',
    ausentismo: 'Ausentismo',
    permiso_personal: 'Permiso Personal',
    otro: 'Otro'
  };
  return labels[type] || type;
}

function getAbsenceTypeClass(type) {
  const classes = {
    enfermedad: 'bg-blue-100 text-blue-800',
    ausentismo: 'bg-red-100 text-red-800',
    permiso_personal: 'bg-yellow-100 text-yellow-800',
    otro: 'bg-gray-100 text-gray-800'
  };
  return classes[type] || 'bg-gray-100 text-gray-800';
}

function getStatusLabel(status) {
  const labels = { pendiente: 'Pendiente', aprobado: 'Aprobado', rechazado: 'Rechazado' };
  return labels[status] || status;
}

function getStatusClass(status) {
  const classes = {
    pendiente: 'bg-yellow-100 text-yellow-800',
    aprobado: 'bg-green-100 text-green-800',
    rechazado: 'bg-red-100 text-red-800'
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
}

function getEmployeeName(empId) {
  const emp = employees.value.find(e => e.employee_id === empId);
  if (!emp) return `ID: ${empId}`;
  return emp.user?.full_name || emp.nombre || emp.rfc;
}

function formatDate(dateStr) {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('es-MX');
}

function openCreateModal() {
  editingAbsence.value = null;
  Object.assign(form, {
    employee_id: '',
    absence_type: '',
    start_date: '',
    end_date: '',
    is_justified: false,
    justification: '',
    notes: ''
  });
  showModal.value = true;
}

function editAbsence(absence) {
  editingAbsence.value = absence;
  Object.assign(form, {
    employee_id: absence.employee_id,
    absence_type: absence.absence_type,
    start_date: absence.start_date,
    end_date: absence.end_date,
    is_justified: absence.is_justified,
    justification: absence.justification || '',
    notes: absence.notes || ''
  });
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  editingAbsence.value = null;
}

async function loadEmployees() {
  try {
    employees.value = await rhService.employees.getAll({ is_active: true });
  } catch (e) {
    console.error('Error cargando empleados:', e);
  }
}

async function loadAbsences() {
  loading.value = true;
  try {
    if (filters.employeeId) {
      absences.value = await rhService.absences.getByEmployee(Number(filters.employeeId));
    } else {
      const allAbsences = [];
      for (const emp of employees.value) {
        try {
          const empAbsences = await rhService.absences.getByEmployee(emp.employee_id);
          allAbsences.push(...empAbsences);
        } catch { /* skip */ }
      }
      absences.value = allAbsences.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    }
  } catch (e) {
    console.error('Error cargando inasistencias:', e);
  } finally {
    loading.value = false;
  }
}

async function updateStatus(absence, newStatus) {
  try {
    await rhService.absences.update(absence.absence_id, {
      status: newStatus,
      reviewed_by: authStore.user?.user_id || 1
    });
    await loadAbsences();
  } catch (e) {
    console.error('Error actualizando estado:', e);
    alert('Error al actualizar estado');
  }
}

async function saveAbsence() {
  saving.value = true;
  try {
    if (editingAbsence.value) {
      await rhService.absences.update(editingAbsence.value.absence_id, {
        absence_type: form.absence_type,
        start_date: form.start_date,
        end_date: form.end_date,
        is_justified: form.is_justified,
        justification: form.justification || undefined,
        notes: form.notes || undefined
      });
    } else {
      await rhService.absences.create({
        employee_id: Number(form.employee_id),
        absence_type: form.absence_type,
        start_date: form.start_date,
        end_date: form.end_date,
        is_justified: form.is_justified,
        justification: form.justification || undefined,
        notes: form.notes || undefined
      });
    }
    closeModal();
    await loadAbsences();
  } catch (e) {
    console.error('Error guardando inasistencia:', e);
    alert('Error al guardar la inasistencia');
  } finally {
    saving.value = false;
  }
}

onMounted(async () => {
  await loadEmployees();
  await loadAbsences();
});
</script>
