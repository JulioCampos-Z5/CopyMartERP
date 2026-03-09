import api, { API_ENDPOINTS } from '@/config/api';

export interface Repair {
  repair_id: number;
  item_id: number;
  model: string;
  serie: string;
  model_toner: string;
  procedencia: string;
  estado_taller: string;
  ubicacion: string | null;
  proceso: string | null;
  estatus: string | null;
  diagnostico_inicial: string | null;
  comments: string | null;
  fecha_alta: string;
  fecha_conclusion: string | null;
  folio_escaneado: string | null;
  foto_evidencia: string | null;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  equipment?: {
    item_id: number;
    sku: string | null;
    brand_name: string | null;
    model: string;
    serie: string;
    model_toner: string;
    location_status: string;
  };
}

export interface RepairCreate {
  item_id: number;
  procedencia: string;
  estado_taller?: string;
  ubicacion?: string;
  proceso?: string;
  estatus?: string;
  diagnostico_inicial?: string;
  comments?: string;
}

export interface RepairUpdate {
  estado_taller?: string;
  ubicacion?: string;
  proceso?: string;
  estatus?: string;
  diagnostico_inicial?: string;
  comments?: string;
  is_active?: boolean;
}

const BASE = API_ENDPOINTS.REPAIRS;

const repairService = {
  async getRepairs(params?: {
    skip?: number;
    limit?: number;
    estado_taller?: string;
    estatus?: string;
    ubicacion?: string;
    search?: string;
  }) {
    const response = await api.get(BASE, { params });
    return response.data;
  },

  async getRepairById(repairId: number): Promise<Repair> {
    const response = await api.get(`${BASE}/${repairId}`);
    return response.data;
  },

  async createRepair(data: RepairCreate): Promise<Repair> {
    const response = await api.post(BASE, data);
    return response.data;
  },

  async updateRepair(repairId: number, data: RepairUpdate): Promise<Repair> {
    const response = await api.put(`${BASE}/${repairId}`, data);
    return response.data;
  },

  async deleteRepair(repairId: number): Promise<void> {
    await api.delete(`${BASE}/${repairId}`);
  },

  async getRepairsByEquipment(itemId: number): Promise<Repair[]> {
    const response = await api.get(`${BASE}/equipment/${itemId}`);
    return response.data;
  },

  async returnToBodega(repairId: number): Promise<Repair> {
    const response = await api.post(`${BASE}/${repairId}/return-to-bodega`);
    return response.data;
  },

  async getStatsByStatus() {
    const response = await api.get(`${BASE}/stats/by-status`);
    return response.data;
  },

  async getStatsByEstatus() {
    const response = await api.get(`${BASE}/stats/by-estatus`);
    return response.data;
  },

  async getStatsByUbicacion() {
    const response = await api.get(`${BASE}/stats/by-ubicacion`);
    return response.data;
  }
};

export default repairService;
