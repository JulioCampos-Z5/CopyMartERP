<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Taller de Reparaciones</h1>
          <p class="text-gray-600 mt-1">Gestión de reparaciones de equipos</p>
        </div>
        <button @click="openCreateModal" class="btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Reparación
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Pendientes</p>
          <p class="text-2xl font-bold text-yellow-600">{{ stats.pendiente }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Pausados</p>
          <p class="text-2xl font-bold text-orange-600">{{ stats.pausado }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Listos</p>
          <p class="text-2xl font-bold text-green-600">{{ stats.listo }}</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow">
          <p class="text-sm text-gray-500">Total</p>
          <p class="text-2xl font-bold text-blue-600">{{ repairs.length }}</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input v-model="filters.search" type="text" class="input-field" placeholder="Buscar por modelo, serie..." @input="loadRepairs" />

          <select v-model="filters.estado_taller" class="input-field" @change="loadRepairs">
            <option value="">Todos los estados</option>
            <option value="pendiente">Pendiente</option>
            <option value="pausado">Pausado</option>
            <option value="listo">Listo</option>
          </select>

          <select v-model="filters.estatus" class="input-field" @change="loadRepairs">
            <option value="">Todos los estatus</option>
            <option value="en_espera_autorizacion">Espera Autorización</option>
            <option value="en_espera_pieza">Espera Pieza</option>
            <option value="pausado">Pausado</option>
            <option value="listo">Listo</option>
          </select>

          <select v-model="filters.ubicacion" class="input-field" @change="loadRepairs">
            <option value="">Todas las ubicaciones</option>
            <option value="zona_1">Zona 1</option>
            <option value="zona_2">Zona 2</option>
            <option value="zona_3">Zona 3</option>
            <option value="zona_4">Zona 4</option>
            <option value="basura">Basura</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="text-gray-500 mt-4">Cargando reparaciones...</p>
      </div>

      <!-- Table -->
      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Equipo</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serie</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Procedencia</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estatus</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ubicación</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Alta</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="repairs.length === 0">
                <td colspan="9" class="px-4 py-8 text-center text-gray-500">No hay reparaciones registradas</td>
              </tr>
              <tr v-for="repair in repairs" :key="repair.repair_id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm text-gray-900">{{ repair.repair_id }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 font-medium">{{ repair.model }}</td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ repair.serie }}</td>
                <td class="px-4 py-3">
                  <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getProcedenciaClass(repair.procedencia)">
                    {{ getProcedenciaLabel(repair.procedencia) }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getEstadoClass(repair.estado_taller)">
                    {{ getEstadoLabel(repair.estado_taller) }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getEstatusClass(repair.estatus)">
                    {{ getEstatusLabel(repair.estatus) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ getUbicacionLabel(repair.ubicacion) }}</td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(repair.fecha_alta) }}</td>
                <td class="px-4 py-3 text-sm flex gap-1">
                  <button @click="editRepair(repair)" class="text-blue-600 hover:text-blue-800" title="Editar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button v-if="repair.estado_taller === 'listo'" @click="returnToBodega(repair)" class="text-green-600 hover:text-green-800" title="Regresar a Bodega">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <h2 class="text-xl font-bold mb-4">{{ editingRepair ? 'Editar Reparación' : 'Nueva Reparación' }}</h2>

          <form @submit.prevent="saveRepair">
            <div class="space-y-4">
              <!-- Equipo (solo en creación) -->
              <div v-if="!editingRepair">
                <label class="block text-sm font-medium text-gray-700 mb-1">ID del Equipo *</label>
                <input v-model.number="form.item_id" type="number" class="input-field" required placeholder="Ingrese ID del equipo" />
              </div>

              <!-- Procedencia -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Procedencia *</label>
                <select v-model="form.procedencia" class="input-field" required :disabled="!!editingRepair">
                  <option value="">Seleccionar procedencia</option>
                  <option value="bodega">Bodega</option>
                  <option value="asignado">Asignado</option>
                  <option value="vendido">Vendido</option>
                  <option value="desconocido">Desconocido</option>
                </select>
              </div>

              <!-- Estado -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Estado Taller</label>
                <select v-model="form.estado_taller" class="input-field">
                  <option value="pendiente">Pendiente</option>
                  <option value="pausado">Pausado</option>
                  <option value="listo">Listo</option>
                </select>
              </div>

              <!-- Estatus -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Estatus</label>
                <select v-model="form.estatus" class="input-field">
                  <option value="en_espera_autorizacion">En Espera de Autorización</option>
                  <option value="en_espera_pieza">En Espera de Pieza</option>
                  <option value="pausado">Pausado</option>
                  <option value="listo">Listo</option>
                </select>
              </div>

              <!-- Ubicación -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ubicación</label>
                <select v-model="form.ubicacion" class="input-field">
                  <option value="">Sin asignar</option>
                  <option value="zona_1">Zona 1</option>
                  <option value="zona_2">Zona 2</option>
                  <option value="zona_3">Zona 3</option>
                  <option value="zona_4">Zona 4</option>
                  <option value="basura">Basura</option>
                </select>
              </div>

              <!-- Proceso -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Proceso</label>
                <select v-model="form.proceso" class="input-field">
                  <option value="desconocido">Desconocido</option>
                  <option value="proceso_1">Proceso 1</option>
                  <option value="proceso_2">Proceso 2</option>
                  <option value="proceso_3">Proceso 3</option>
                </select>
              </div>

              <!-- Diagnóstico -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Diagnóstico Inicial</label>
                <textarea v-model="form.diagnostico_inicial" class="input-field" rows="3" placeholder="Diagnóstico del equipo..."></textarea>
              </div>

              <!-- Comentarios -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
                <textarea v-model="form.comments" class="input-field" rows="2" placeholder="Comentarios adicionales..."></textarea>
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Guardando...' : (editingRepair ? 'Actualizar' : 'Crear') }}
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
import repairService from '@/services/repairService';

const loading = ref(false);
const saving = ref(false);
const showModal = ref(false);
const editingRepair = ref(null);
const repairs = ref([]);

const filters = reactive({
  search: '',
  estado_taller: '',
  estatus: '',
  ubicacion: ''
});

const form = reactive({
  item_id: null,
  procedencia: '',
  estado_taller: 'pendiente',
  estatus: 'en_espera_autorizacion',
  ubicacion: '',
  proceso: 'desconocido',
  diagnostico_inicial: '',
  comments: ''
});

const stats = computed(() => {
  const s = { pendiente: 0, pausado: 0, listo: 0 };
  repairs.value.forEach(r => {
    if (s[r.estado_taller] !== undefined) s[r.estado_taller]++;
  });
  return s;
});

function getEstadoLabel(estado) {
  const labels = { pendiente: 'Pendiente', pausado: 'Pausado', listo: 'Listo' };
  return labels[estado] || estado;
}

function getEstadoClass(estado) {
  const classes = {
    pendiente: 'bg-yellow-100 text-yellow-800',
    pausado: 'bg-orange-100 text-orange-800',
    listo: 'bg-green-100 text-green-800'
  };
  return classes[estado] || 'bg-gray-100 text-gray-800';
}

function getEstatusLabel(estatus) {
  const labels = {
    en_espera_autorizacion: 'Espera Autorización',
    en_espera_pieza: 'Espera Pieza',
    pausado: 'Pausado',
    listo: 'Listo'
  };
  return labels[estatus] || estatus || '-';
}

function getEstatusClass(estatus) {
  const classes = {
    en_espera_autorizacion: 'bg-blue-100 text-blue-800',
    en_espera_pieza: 'bg-purple-100 text-purple-800',
    pausado: 'bg-orange-100 text-orange-800',
    listo: 'bg-green-100 text-green-800'
  };
  return classes[estatus] || 'bg-gray-100 text-gray-800';
}

function getProcedenciaLabel(proc) {
  const labels = { bodega: 'Bodega', asignado: 'Asignado', vendido: 'Vendido', desconocido: 'Desconocido' };
  return labels[proc] || proc;
}

function getProcedenciaClass(proc) {
  const classes = {
    bodega: 'bg-blue-100 text-blue-800',
    asignado: 'bg-green-100 text-green-800',
    vendido: 'bg-indigo-100 text-indigo-800',
    desconocido: 'bg-gray-100 text-gray-800'
  };
  return classes[proc] || 'bg-gray-100 text-gray-800';
}

function getUbicacionLabel(ubi) {
  const labels = { zona_1: 'Zona 1', zona_2: 'Zona 2', zona_3: 'Zona 3', zona_4: 'Zona 4', basura: 'Basura' };
  return labels[ubi] || ubi || '-';
}

function formatDate(dateStr) {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('es-MX');
}

function openCreateModal() {
  editingRepair.value = null;
  Object.assign(form, {
    item_id: null,
    procedencia: '',
    estado_taller: 'pendiente',
    estatus: 'en_espera_autorizacion',
    ubicacion: '',
    proceso: 'desconocido',
    diagnostico_inicial: '',
    comments: ''
  });
  showModal.value = true;
}

function editRepair(repair) {
  editingRepair.value = repair;
  Object.assign(form, {
    item_id: repair.item_id,
    procedencia: repair.procedencia,
    estado_taller: repair.estado_taller,
    estatus: repair.estatus || 'en_espera_autorizacion',
    ubicacion: repair.ubicacion || '',
    proceso: repair.proceso || 'desconocido',
    diagnostico_inicial: repair.diagnostico_inicial || '',
    comments: repair.comments || ''
  });
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  editingRepair.value = null;
}

async function loadRepairs() {
  loading.value = true;
  try {
    const params = {};
    if (filters.search) params.search = filters.search;
    if (filters.estado_taller) params.estado_taller = filters.estado_taller;
    if (filters.estatus) params.estatus = filters.estatus;
    if (filters.ubicacion) params.ubicacion = filters.ubicacion;

    const data = await repairService.getRepairs(params);
    repairs.value = Array.isArray(data) ? data : (data.repairs || []);
  } catch (e) {
    console.error('Error cargando reparaciones:', e);
  } finally {
    loading.value = false;
  }
}

async function returnToBodega(repair) {
  if (!confirm(`¿Regresar equipo ${repair.model} (${repair.serie}) a bodega?`)) return;
  try {
    await repairService.returnToBodega(repair.repair_id);
    await loadRepairs();
  } catch (e) {
    console.error('Error al regresar a bodega:', e);
    alert('Error al regresar el equipo a bodega');
  }
}

async function saveRepair() {
  saving.value = true;
  try {
    if (editingRepair.value) {
      await repairService.updateRepair(editingRepair.value.repair_id, {
        estado_taller: form.estado_taller,
        estatus: form.estatus,
        ubicacion: form.ubicacion || undefined,
        proceso: form.proceso,
        diagnostico_inicial: form.diagnostico_inicial || undefined,
        comments: form.comments || undefined
      });
    } else {
      await repairService.createRepair({
        item_id: form.item_id,
        procedencia: form.procedencia,
        estado_taller: form.estado_taller,
        estatus: form.estatus,
        ubicacion: form.ubicacion || undefined,
        proceso: form.proceso,
        diagnostico_inicial: form.diagnostico_inicial || undefined,
        comments: form.comments || undefined
      });
    }
    closeModal();
    await loadRepairs();
  } catch (e) {
    console.error('Error guardando reparación:', e);
    alert('Error al guardar la reparación');
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  loadRepairs();
});
</script>
