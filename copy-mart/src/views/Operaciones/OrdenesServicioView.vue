<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-cyan-50 dark:bg-cyan-900/30 p-6 rounded-lg border border-cyan-200 dark:border-cyan-700">
        <h1 class="text-3xl font-bold text-cyan-800 dark:text-cyan-200 mb-2">Órdenes de Servicio</h1>
        <p class="text-cyan-600 dark:text-cyan-400">Gestión y seguimiento de órdenes de trabajo y mantenimiento</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-cyan-100 dark:bg-cyan-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Tickets Pendientes</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ tickets.filter(t => t.report_status === 'pendiente').length }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">En Proceso</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ tickets.filter(t => ['urgente', 'programado', 'atencion'].includes(t.report_status)).length }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Completados Hoy</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ ticketsCompletedToday }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Tickets</h3>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ tickets.length }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border dark:border-gray-700">
        <div class="flex flex-wrap gap-4">
          <button @click="openTicketModal()" class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nuevo Ticket
          </button>
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filtrar
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow border dark:border-gray-700">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Tickets de Servicio</h2>
        </div>

        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-600"></div>
        </div>

        <div v-else-if="tickets.length > 0" class="p-6">
          <div class="overflow-x-auto">
            <table class="min-w-full table-auto">
              <thead>
                <tr class="bg-gray-50 dark:bg-gray-700">
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">ID</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Cliente</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Tipo</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Descripción</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Estado</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Fecha</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="ticket in tickets" :key="ticket.ticket_id">
                  <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">#{{ ticket.ticket_id }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ getClientName(ticket.client_id) }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ getTypeBadge(ticket.report_type) }}</td>
                  <td class="px-4 py-4 text-sm text-gray-900 dark:text-gray-200 max-w-xs truncate">{{ ticket.description }}</td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <span :class="getStatusClass(ticket.report_status)" class="px-2 py-1 text-xs font-medium rounded-full">
                      {{ getStatusLabel(ticket.report_status) }}
                    </span>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">{{ formatDate(ticket.created_at) }}</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm">
                    <div class="flex gap-2">
                      <button @click="viewTicket(ticket.ticket_id)" class="text-blue-600 hover:text-blue-800" title="Ver detalle">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </button>
                      <button @click="editTicket(ticket)" class="text-cyan-600 hover:text-cyan-800" title="Editar">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button v-if="canDelete" @click="deleteTicket(ticket.ticket_id)" class="text-red-600 hover:text-red-800" title="Eliminar">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else class="p-6 text-center text-gray-500 dark:text-gray-400">
          No hay tickets registrados
        </div>
      </div>

      <!-- Modal Ticket -->
      <div v-if="showTicketModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showTicketModal = false">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-semibold mb-4 dark:text-white">{{ ticketForm.ticket_id ? 'Editar' : 'Nuevo' }} Ticket</h3>
          <form @submit.prevent="saveTicket" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
                <select v-model.number="ticketForm.client_id" required 
                        @change="onClientChange"
                        :disabled="!!ticketForm.ticket_id"
                        class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                  <option value="0">Seleccionar cliente...</option>
                  <option v-for="client in clients" :key="client.client_id" :value="client.client_id">
                    {{ client.comercial_name || client.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Sucursal *</label>
                <select v-model.number="ticketForm.branch_id" required 
                        :disabled="!ticketForm.client_id || branches.length === 0"
                        class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                  <option value="0">{{ ticketForm.client_id ? (branches.length ? 'Seleccionar sucursal...' : 'Sin sucursales') : 'Primero seleccione un cliente' }}</option>
                  <option v-for="branch in branches" :key="branch.branch_id" :value="branch.branch_id">
                    {{ branch.name }} {{ branch.city ? `- ${branch.city}` : '' }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Reporte *</label>
                <select v-model="ticketForm.report_type" required class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                  <option value="conectividad">Conectividad</option>
                  <option value="atasco">Atasco</option>
                  <option value="toner">Tóner</option>
                  <option value="quejas">Quejas</option>
                  <option value="copia">Copia</option>
                  <option value="ruidos">Ruidos</option>
                  <option value="impresion">Impresión</option>
                  <option value="otros">Otros</option>
                </select>
              </div>
              <div v-if="ticketForm.ticket_id">
                <label class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
                <select v-model="ticketForm.report_status" required class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                  <option value="pendiente">Pendiente</option>
                  <option value="listo">Listo</option>
                  <option value="urgente">Urgente</option>
                  <option value="programado">Programado</option>
                  <option value="informativo">Informativo</option>
                  <option value="no_quedo_en_la_visita">No quedó en la visita</option>
                  <option value="atencion">Atención</option>
                </select>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Descripción *</label>
                <textarea v-model="ticketForm.description" required rows="3" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"></textarea>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Evidencia</label>
                <input
                  type="file"
                  @change="onEvidenceFileChange"
                  accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.txt"
                  class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                />
                <p v-if="selectedEvidenceFile" class="text-xs text-gray-600 mt-1">
                  Archivo seleccionado: {{ selectedEvidenceFile.name }}
                </p>
                <a
                  v-if="!selectedEvidenceFile && ticketForm.evidence"
                  :href="ticketService.getEvidenceUrl(ticketForm.evidence)"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-xs text-blue-600 hover:text-blue-800 mt-1 inline-block"
                >
                  Ver evidencia actual
                </a>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Acción Correctiva</label>
                <textarea v-model="ticketForm.corrective_action" rows="2" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"></textarea>
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="showTicketModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
              <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded-lg hover:bg-cyan-700">Guardar</button>
            </div>
          </form>
        </div>
      </div>

    </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import ticketService, { type Ticket, type TicketCreate, type TicketUpdate } from '@/services/ticketService'
import { clientService } from '@/services/clientService'
import type { Client, Branch } from '@/types'
import { getStoredUser, hasDeleteAccess } from '@/config/accessControl'

const router = useRouter()
const loading = ref(false)
const tickets = ref<Ticket[]>([])
const showTicketModal = ref(false)
const selectedEvidenceFile = ref<File | null>(null)
const canDelete = computed(() => hasDeleteAccess(getStoredUser()))

// Datos para selects
const clients = ref<Client[]>([])
const branches = ref<Branch[]>([])
const loadingClients = ref(false)

const ticketForm = ref<any>({
  ticket_id: 0,
  client_id: 0,
  branch_id: 0,
  area_id: undefined,
  report_type: 'otros',
  report_status: 'pendiente',
  description: '',
  evidence: '',
  corrective_action: ''
})

const ticketsCompletedToday = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return tickets.value.filter(t => 
    t.report_status === 'listo' && 
    t.completed_at?.startsWith(today)
  ).length
})

const loadTickets = async () => {
  loading.value = true
  try {
    tickets.value = await ticketService.getAll()
  } catch (error) {
    console.error('Error loading tickets:', error)
  } finally {
    loading.value = false
  }
}

const loadClients = async () => {
  loadingClients.value = true
  try {
    const response = await clientService.getClients({ pageSize: 500 })
    clients.value = response.items || []
  } catch (error) {
    console.error('Error loading clients:', error)
  } finally {
    loadingClients.value = false
  }
}

const viewTicket = (ticketId: number) => {
  router.push({ name: 'TicketDetail', params: { id: ticketId } })
}

const editTicket = async (ticket: Ticket) => {
  // Cargar clientes si no están cargados
  if (clients.value.length === 0) {
    await loadClients()
  }
  
  ticketForm.value = { ...ticket }
  selectedEvidenceFile.value = null
  // Cargar sucursales del cliente
  if (ticket.client_id) {
    try {
      branches.value = await clientService.getClientBranches(ticket.client_id)
    } catch (error) {
      console.error('Error loading branches:', error)
    }
  }
  showTicketModal.value = true
}

const onClientChange = async () => {
  branches.value = []
  ticketForm.value.branch_id = 0
  
  if (ticketForm.value.client_id) {
    try {
      branches.value = await clientService.getClientBranches(ticketForm.value.client_id)
      // Si solo hay una sucursal, seleccionarla automáticamente
      if (branches.value.length === 1) {
        ticketForm.value.branch_id = branches.value[0].branch_id
      }
    } catch (error) {
      console.error('Error loading branches:', error)
    }
  }
}

const openTicketModal = async (ticket?: Ticket) => {
  // Cargar clientes si no están cargados
  if (clients.value.length === 0) {
    await loadClients()
  }
  
  if (ticket) {
    ticketForm.value = { ...ticket }
    selectedEvidenceFile.value = null
    // Cargar sucursales del cliente
    if (ticket.client_id) {
      try {
        branches.value = await clientService.getClientBranches(ticket.client_id)
      } catch (error) {
        console.error('Error loading branches:', error)
      }
    }
  } else {
    ticketForm.value = {
      ticket_id: 0,
      client_id: 0,
      branch_id: 0,
      area_id: undefined,
        report_type: 'otros',
        report_status: 'pendiente',
      description: '',
      evidence: '',
      corrective_action: ''
    }
    selectedEvidenceFile.value = null
    branches.value = []
  }
  showTicketModal.value = true
}

const onEvidenceFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  selectedEvidenceFile.value = target.files?.[0] || null
}

const saveTicket = async () => {
  try {
    let evidencePath = ticketForm.value.evidence
    if (selectedEvidenceFile.value) {
      const uploaded = await ticketService.uploadEvidence(selectedEvidenceFile.value)
      evidencePath = uploaded.file_path
    }

    if (ticketForm.value.ticket_id) {
      const updateData: TicketUpdate = {
        branch_id: ticketForm.value.branch_id,
        area_id: ticketForm.value.area_id,
        report_status: ticketForm.value.report_status,
        report_type: ticketForm.value.report_type,
        description: ticketForm.value.description,
        evidence: evidencePath,
        corrective_action: ticketForm.value.corrective_action
      }
      await ticketService.update(ticketForm.value.ticket_id, updateData)
    } else {
      const createData: TicketCreate = {
        client_id: ticketForm.value.client_id,
        branch_id: ticketForm.value.branch_id,
        area_id: ticketForm.value.area_id,
        report_type: ticketForm.value.report_type,
        description: ticketForm.value.description,
        evidence: evidencePath,
        corrective_action: ticketForm.value.corrective_action
      }
      await ticketService.create(createData)
    }
    selectedEvidenceFile.value = null
    showTicketModal.value = false
    await loadTickets()
  } catch (error: any) {
    console.error('Error saving ticket:', error)
    alert(`Error al guardar ticket: ${error.message || error}`)
  }
}

const deleteTicket = async (ticketId: number) => {
  if (!canDelete.value) {
    alert('No tienes permisos para eliminar tickets')
    return
  }
  if (!confirm('¿Estás seguro de eliminar este ticket?')) return
  try {
    await ticketService.delete(ticketId)
    await loadTickets()
  } catch (error: any) {
    console.error('Error deleting ticket:', error)
    alert(`Error al eliminar ticket: ${error.message || error}`)
  }
}

const getClientName = (clientId: number) => {
  const client = clients.value.find(c => c.client_id === clientId)
  return client ? (client.comercial_name || client.name) : `Cliente #${clientId}`
}

const getTypeBadge = (type: string) => {
  const labels: Record<string, string> = {
    'conectividad': 'Conectividad',
    'atasco': 'Atasco',
    'toner': 'Tóner',
    'quejas': 'Quejas',
    'copia': 'Copia',
    'ruidos': 'Ruidos',
    'impresion': 'Impresión',
    'otros': 'Otros'
  }
  return labels[type] || type
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    'pendiente': 'Pendiente',
    'listo': 'Listo',
    'urgente': 'Urgente',
    'programado': 'Programado',
    'informativo': 'Informativo',
    'no_quedo_en_la_visita': 'No quedó en la visita',
    'atencion': 'Atención'
  }
  return labels[status] || status
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'listo': 'bg-green-100 text-green-800',
    'urgente': 'bg-red-100 text-red-800',
    'programado': 'bg-blue-100 text-blue-800',
    'informativo': 'bg-purple-100 text-purple-800',
    'no_quedo_en_la_visita': 'bg-orange-100 text-orange-800',
    'atencion': 'bg-pink-100 text-pink-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadTickets()
  loadClients() // Cargar clientes para mostrar nombres en la tabla
})
</script>