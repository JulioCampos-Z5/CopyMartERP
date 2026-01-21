import api from '@/config/api';

export interface Ticket {
  ticket_id: number;
  client_id: number;
  branch_id: number;
  area_id?: number;
  report_type: 'PREVENTIVO' | 'CORRECTIVO' | 'INSTALACION' | 'DESINSTALACION' | 'VISITA_CLIENTE';
  report_status: 'PENDIENTE' | 'EN_PROCESO' | 'COMPLETADO' | 'CANCELADO';
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
  report_type: 'PREVENTIVO' | 'CORRECTIVO' | 'INSTALACION' | 'DESINSTALACION' | 'VISITA_CLIENTE';
  description: string;
  evidence?: string;
  corrective_action?: string;
}

export interface TicketUpdate {
  branch_id?: number;
  area_id?: number;
  report_status?: 'PENDIENTE' | 'EN_PROCESO' | 'COMPLETADO' | 'CANCELADO';
  report_type?: 'PREVENTIVO' | 'CORRECTIVO' | 'INSTALACION' | 'DESINSTALACION' | 'VISITA_CLIENTE';
  description?: string;
  evidence?: string;
  corrective_action?: string;
}

const ticketService = {
  // Crear ticket
  async create(data: TicketCreate): Promise<Ticket> {
    const response = await api.post('/tickets/', data);
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
    const response = await api.get('/tickets/', { params });
    return response.data;
  },

  // Obtener mis tickets (tickets creados por el usuario actual)
  async getMyTickets(): Promise<Ticket[]> {
    const response = await api.get('/tickets/my-tickets');
    return response.data;
  },

  // Obtener ticket por ID
  async getById(ticketId: number): Promise<Ticket> {
    const response = await api.get(`/tickets/${ticketId}`);
    return response.data;
  },

  // Actualizar ticket
  async update(ticketId: number, data: TicketUpdate): Promise<Ticket> {
    const response = await api.put(`/tickets/${ticketId}`, data);
    return response.data;
  },

  // Eliminar ticket
  async delete(ticketId: number): Promise<void> {
    await api.delete(`/tickets/${ticketId}`);
  }
};

export default ticketService;
