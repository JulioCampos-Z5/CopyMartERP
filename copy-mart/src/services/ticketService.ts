import api, { API_BASE_URL } from '@/config/api';

export interface Ticket {
  ticket_id: number;
  client_id: number;
  branch_id: number;
  area_id?: number;
  report_type: 'conectividad' | 'atasco' | 'toner' | 'quejas' | 'copia' | 'ruidos' | 'impresion' | 'otros';
  report_status: 'pendiente' | 'listo' | 'urgente' | 'programado' | 'informativo' | 'no_quedo_en_la_visita' | 'atencion';
  description: string;
  evidence?: string;
  corrective_action?: string;
  created_by: number;
  created_at: string;
  completed_at?: string;
}

export interface TicketCreate {
  client_id: number;
  branch_id: number;
  area_id?: number;
  report_type: 'conectividad' | 'atasco' | 'toner' | 'quejas' | 'copia' | 'ruidos' | 'impresion' | 'otros';
  description: string;
  evidence?: string;
  corrective_action?: string;
}

export interface TicketUpdate {
  branch_id?: number;
  area_id?: number;
  report_status?: 'pendiente' | 'listo' | 'urgente' | 'programado' | 'informativo' | 'no_quedo_en_la_visita' | 'atencion';
  report_type?: 'conectividad' | 'atasco' | 'toner' | 'quejas' | 'copia' | 'ruidos' | 'impresion' | 'otros';
  description?: string;
  evidence?: string;
  corrective_action?: string;
}

export interface EvidenceUploadResponse {
  file_path: string;
  filename: string;
}

const ticketService = {
  // Crear ticket
  async create(data: TicketCreate): Promise<Ticket> {
    const response = await api.post('/api/tickets/', data);
    return response.data;
  },

  // Obtener todos los tickets
  async getAll(params?: {
    client_id?: number;
    branch_id?: number;
    area_id?: number;
    report_status?: string;
    report_type?: string;
  }): Promise<Ticket[]> {
    const response = await api.get('/api/tickets/', { params });
    return response.data;
  },

  // Obtener mis tickets (tickets creados por el usuario actual)
  async getMyTickets(): Promise<Ticket[]> {
    const response = await api.get('/api/tickets/my-tickets');
    return response.data;
  },

  // Obtener ticket por ID
  async getById(ticketId: number): Promise<Ticket> {
    const response = await api.get(`/api/tickets/${ticketId}`);
    return response.data;
  },

  // Actualizar ticket
  async update(ticketId: number, data: TicketUpdate): Promise<Ticket> {
    const response = await api.put(`/api/tickets/${ticketId}`, data);
    return response.data;
  },

  async uploadEvidence(file: File): Promise<EvidenceUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/tickets/evidence/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  getEvidenceUrl(filePath?: string): string {
    if (!filePath) return '';
    if (filePath.startsWith('http://') || filePath.startsWith('https://')) return filePath;
    const normalized = filePath.replace(/\\/g, '/');
    const filename = normalized.split('/').pop();
    return `${API_BASE_URL}/api/tickets/evidence/${filename}`;
  },

  // Eliminar ticket
  async delete(ticketId: number): Promise<void> {
    await api.delete(`/api/tickets/${ticketId}`);
  }
};

export default ticketService;
