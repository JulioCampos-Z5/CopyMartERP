<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-6">
        <button @click="$router.back()" class="text-cyan-600 hover:text-cyan-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Órdenes de Servicio
        </button>
      </div>

      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-600"></div>
      </div>

      <div v-else-if="ticket" class="space-y-6">
        <!-- Header con información principal -->
        <div class="bg-white rounded-lg shadow border p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 mb-2">Ticket #{{ ticket.ticket_id }}</h1>
              <span :class="getStatusClass(ticket.report_status)" class="px-3 py-1 text-sm font-medium rounded-full">
                {{ getStatusLabel(ticket.report_status) }}
              </span>
            </div>
            <div class="flex gap-2">
              <button @click="editTicket" class="bg-cyan-600 text-white px-4 py-2 rounded-lg hover:bg-cyan-700 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar
              </button>
              <button v-if="canDelete" @click="deleteTicket" class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <!-- Grid de información -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Información General -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Información General</h2>
            <dl class="space-y-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">Cliente</dt>
                <dd class="text-base text-gray-900 mt-1">{{ getClientName() }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Sucursal</dt>
                <dd class="text-base text-gray-900 mt-1">{{ getBranchName() }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Área</dt>
                <dd class="text-base text-gray-900 mt-1">{{ ticket.area_id ? getAreaName() : '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Tipo de Reporte</dt>
                <dd class="text-base text-gray-900 mt-1">{{ getTypeLabel(ticket.report_type) }}</dd>
              </div>
            </dl>
          </div>

          <!-- Información de Fechas -->
          <div class="bg-white rounded-lg shadow border p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Fechas</h2>
            <dl class="space-y-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">Creado en</dt>
                <dd class="text-base text-gray-900 mt-1">{{ formatDate(ticket.created_at) }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Completado en</dt>
                <dd class="text-base text-gray-900 mt-1">{{ ticket.completed_at ? formatDate(ticket.completed_at) : '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Creado por</dt>
                <dd class="text-base text-gray-900 mt-1">{{ getCreatorName() }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <!-- Descripción -->
        <div class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Descripción</h2>
          <p class="text-gray-700 whitespace-pre-wrap">{{ ticket.description }}</p>
        </div>

        <!-- Acción Correctiva -->
        <div v-if="ticket.corrective_action" class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Acción Correctiva</h2>
          <p class="text-gray-700 whitespace-pre-wrap">{{ ticket.corrective_action }}</p>
        </div>

        <!-- Evidencia -->
        <div v-if="ticket.evidence" class="bg-white rounded-lg shadow border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Evidencia</h2>
          <div class="flex gap-3 items-center">
            <button 
              @click="openEvidenceModal" 
              class="px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              Ver evidencia
            </button>
            <button 
              @click="downloadEvidenceFromUrl" 
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Descargar
            </button>
          </div>
        </div>

        <div v-else class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p class="text-yellow-800">No hay evidencia adjunta para este ticket</p>
        </div>
      </div>

      <div v-else class="bg-white rounded-lg shadow border p-6 text-center">
        <p class="text-gray-500">No se encontró el ticket</p>
      </div>

      <!-- Modal Evidencia -->
      <div v-if="showEvidenceModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-auto">
          <!-- Header del Modal -->
          <div class="flex justify-between items-center p-6 border-b border-gray-200 sticky top-0 bg-white">
            <h2 class="text-2xl font-semibold text-gray-900">Evidencia - Ticket #{{ ticket?.ticket_id }}</h2>
            <button 
              @click="closeEvidenceModal"
              class="text-gray-500 hover:text-gray-700"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Contenido del Modal -->
          <div class="p-6">
            <!-- Imagen -->
            <img 
              v-if="isImageFile(ticket?.evidence || '')"
              :src="evidenceBlobUrl" 
              :alt="`Evidencia del ticket #${ticket?.ticket_id}`"
              class="w-full rounded-lg border border-gray-200 object-contain"
            />

            <!-- PDF -->
            <iframe 
              v-else-if="isPdfFile(ticket?.evidence || '')"
              :src="evidenceBlobUrl" 
              class="w-full rounded-lg border border-gray-200"
              style="height: 600px"
            ></iframe>

            <!-- Otros archivos -->
            <div v-else class="flex flex-col items-center justify-center py-12 text-center">
              <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="text-gray-600 mb-4">Este tipo de archivo no puede ser mostrado en vista previa</p>
              <button 
                @click="downloadEvidence"
                class="px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700"
              >
                Descargar archivo
              </button>
            </div>
          </div>

          <!-- Footer del Modal -->
          <div class="flex justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50 sticky bottom-0">
            <button 
              @click="closeEvidenceModal"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100"
            >
              Cerrar
            </button>
            <button 
              @click="downloadEvidence"
              class="px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Descargar
            </button>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import ticketService, { type Ticket } from '@/services/ticketService'
import { clientService } from '@/services/clientService'
import type { Client, Branch } from '@/types'
import { getStoredUser, hasDeleteAccess } from '@/config/accessControl'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const ticket = ref<Ticket | null>(null)
const clients = ref<Client[]>([])
const branches = ref<Branch[]>([])
const canDelete = computed(() => hasDeleteAccess(getStoredUser()))
const showEvidenceModal = ref(false)
const evidenceBlobUrl = ref<string>('')

const ticketId = computed(() => Number(route.params.id))

const loadTicket = async () => {
  try {
    loading.value = true
    ticket.value = await ticketService.getById(ticketId.value)
  } catch (error) {
    console.error('Error loading ticket:', error)
  } finally {
    loading.value = false
  }
}

const loadClients = async () => {
  try {
    const response = await clientService.getClients({ pageSize: 500 })
    clients.value = response.items || []
  } catch (error) {
    console.error('Error loading clients:', error)
  }
}

const loadBranches = async () => {
  try {
    if (ticket.value?.client_id) {
      branches.value = await clientService.getClientBranches(ticket.value.client_id)
    }
  } catch (error) {
    console.error('Error loading branches:', error)
  }
}

const getClientName = () => {
  const client = clients.value.find(c => c.client_id === ticket.value?.client_id)
  return client ? (client.comercial_name || client.name) : `Cliente #${ticket.value?.client_id}`
}

const getBranchName = () => {
  const branch = branches.value.find(b => b.branch_id === ticket.value?.branch_id)
  return branch ? branch.name : `Sucursal #${ticket.value?.branch_id}`
}

const getAreaName = () => {
  // Aquí puedes agregar la lógica para obtener el nombre del área si es necesario
  return `Área #${ticket.value?.area_id}`
}

const getCreatorName = () => {
  // Puedes expandir esto si tienes acceso a los datos del usuario creador
  return `Usuario #${ticket.value?.created_by}`
}

const getTypeLabel = (type: string) => {
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
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const isImageFile = (filePath: string) => {
  if (!filePath) return false
  const imageExtensions = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', 
    '.svg', '.ico', '.tiff', '.tif', '.jfif', '.pjpeg', '.pjp',
    '.apng', '.avif'
  ]
  return imageExtensions.some(ext => filePath.toLowerCase().endsWith(ext))
}

const isPdfFile = (filePath: string) => {
  if (!filePath) return false
  return filePath.toLowerCase().endsWith('.pdf')
}

const openEvidenceModal = async () => {
  try {
    // Obtener el token del almacenamiento local
    const user = getStoredUser()
    const token = localStorage.getItem('token')
    
    if (!token || !ticket.value?.evidence) {
      alert('No se puedo cargar la evidencia')
      return
    }
    
    // Obtener el nombre del archivo
    const filename = ticket.value.evidence.split('/').pop() || ''
    const url = `http://192.168.100.93:8000/api/tickets/evidence/${filename}`
    
    // Hacer fetch con autenticación
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`)
    }
    
    // Convertir a blob
    const blob = await response.blob()
    
    // Crear blob URL
    if (evidenceBlobUrl.value) {
      URL.revokeObjectURL(evidenceBlobUrl.value)
    }
    evidenceBlobUrl.value = URL.createObjectURL(blob)
    
    showEvidenceModal.value = true
  } catch (error) {
    console.error('Error loading evidence:', error)
    alert(`Error al cargar la evidencia: ${error}`)
  }
}

const closeEvidenceModal = () => {
  showEvidenceModal.value = false
  // Limpiar el blob URL
  if (evidenceBlobUrl.value) {
    URL.revokeObjectURL(evidenceBlobUrl.value)
    evidenceBlobUrl.value = ''
  }
}

const downloadEvidence = () => {
  if (!evidenceBlobUrl.value || !ticket.value?.evidence) return
  
  // Crear un elemento <a> temporal para descargar
  const link = document.createElement('a')
  link.href = evidenceBlobUrl.value
  
  // Obtener el nombre del archivo original
  const filename = ticket.value.evidence.split('/').pop() || `evidencia_${ticket.value.ticket_id}`
  link.download = filename
  
  // Trigger la descarga
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const downloadEvidenceFromUrl = async () => {
  if (!ticket.value?.evidence) return
  
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('Sesión expirada. Por favor, inicia sesión nuevamente.')
      return
    }
    
    // Obtener el nombre del archivo
    const filename = ticket.value.evidence.split('/').pop() || ''
    const url = `http://192.168.100.93:8000/api/tickets/evidence/${filename}`
    
    // Hacer fetch con autenticación
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`)
    }
    
    // Convertir a blob
    const blob = await response.blob()
    
    // Crear blob URL y descargar
    const blobUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = filename
    
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // Limpiar blob URL
    URL.revokeObjectURL(blobUrl)
  } catch (error) {
    console.error('Error downloading evidence:', error)
    alert(`Error al descargar: ${error}`)
  }
}

const editTicket = () => {
  // Aquí puedes agregar la navegación a una vista de edición si la tienes
  // router.push({ name: 'EditTicket', params: { id: ticketId.value } })
  console.log('Editar ticket:', ticketId.value)
}

const deleteTicket = async () => {
  if (!canDelete.value) {
    alert('No tienes permisos para eliminar tickets')
    return
  }
  if (!confirm('¿Estás seguro de que deseas eliminar este ticket?')) return

  try {
    await ticketService.delete(ticketId.value)
    alert('Ticket eliminado exitosamente')
    router.push({ name: 'OrdenesServicio' })
  } catch (error: any) {
    console.error('Error deleting ticket:', error)
    alert(`Error al eliminar ticket: ${error.message || error}`)
  }
}

onMounted(() => {
  loadTicket()
  loadClients()
  // Cargar sucursales una vez que esté disponible el client_id
  const interval = setInterval(() => {
    if (ticket.value?.client_id) {
      loadBranches()
      clearInterval(interval)
    }
  }, 100)
})
</script>
