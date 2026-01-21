import api from '@/config/api';

export interface PrintCounter {
  counter_id: number;
  rent_id: number;
  billing_id?: number;
  period_month: number;
  period_year: number;
  bn_current: number;
  bn_previous: number;
  bn_printed: number;
  bn_included: number;
  bn_excess: number;
  bn_cost_per_page: number;
  bn_excess_amount: number;
  color_current: number;
  color_previous: number;
  color_printed: number;
  color_included: number;
  color_excess: number;
  color_cost_per_page: number;
  color_excess_amount: number;
  total_excess_amount: number;
  counter_photo_url?: string;
  notes?: string;
  reading_date: string;
  is_billed: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface PrintCounterCreate {
  rent_id: number;
  period_month: number;
  period_year: number;
  bn_current?: number;
  color_current?: number;
  counter_photo_url?: string;
  notes?: string;
  reading_date?: string;
}

export interface PrintCounterUpdate {
  bn_current?: number;
  color_current?: number;
  counter_photo_url?: string;
  notes?: string;
  reading_date?: string;
}

export interface PrintCounterBatch {
  rent_id: number;
  period_month: number;
  period_year: number;
}

export interface PrintCounterStats {
  total_bn_printed: number;
  total_color_printed: number;
  total_excess_amount: number;
  total_counters: number;
  pending_billing: number;
}

const printService = {
  // Crear contador
  async create(data: PrintCounterCreate): Promise<PrintCounter> {
    const response = await api.post('/print-counters/', data);
    return response.data;
  },

  // Crear contadores en lote
  async createBatch(data: PrintCounterBatch[]): Promise<any> {
    const response = await api.post('/print-counters/batch', { counters: data });
    return response.data;
  },

  // Obtener todos los contadores
  async getAll(params?: {
    rent_id?: number;
    client_id?: number;
    period_month?: number;
    period_year?: number;
    is_billed?: boolean;
  }): Promise<PrintCounter[]> {
    const response = await api.get('/print-counters/', { params });
    return response.data;
  },

  // Obtener contador por ID
  async getById(counterId: number): Promise<PrintCounter> {
    const response = await api.get(`/print-counters/${counterId}`);
    return response.data;
  },

  // Actualizar contador
  async update(counterId: number, data: PrintCounterUpdate): Promise<PrintCounter> {
    const response = await api.put(`/print-counters/${counterId}`, data);
    return response.data;
  },

  // Eliminar contador
  async delete(counterId: number): Promise<void> {
    await api.delete(`/print-counters/${counterId}`);
  },

  // Obtener estadísticas
  async getStats(params?: {
    period_month?: number;
    period_year?: number;
    client_id?: number;
  }): Promise<PrintCounterStats> {
    const response = await api.get('/print-counters/stats/summary', { params });
    return response.data;
  },

  // Obtener historial de un contrato de renta
  async getHistory(rentId: number): Promise<PrintCounter[]> {
    const response = await api.get(`/print-counters/rent/${rentId}/history`);
    return response.data;
  }
};

export default printService;
