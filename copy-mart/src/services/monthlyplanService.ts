import api from '@/config/api';

export interface MonthlyPlan {
  monthlyplan_id: number;
  client_id: number;
  branch_id: number;
  area_id?: number;
  ticket_id?: number;
  service_type_id: number;
  description?: string;
  visit_date: string;
  attendance_status: 'PENDIENTE' | 'ASISTIO' | 'NO_ASISTIO' | 'REPROGRAMADO';
  created_by: number;
  created_at: string;
  updated_at: string;
  assigned_users: UserBasicInfo[];
}

export interface UserBasicInfo {
  user_id: number;
  username: string;
  email?: string;
}

export interface ServiceType {
  service_type_id: number;
  name: string;
  description?: string;
  is_active: number;
  created_at: string;
}

export interface MonthlyPlanCreate {
  client_id: number;
  branch_id: number;
  area_id?: number;
  ticket_id?: number;
  service_type_id: number;
  description?: string;
  visit_date: string;
  assigned_user_ids?: number[];
}

export interface MonthlyPlanUpdate {
  branch_id?: number;
  area_id?: number;
  ticket_id?: number;
  service_type_id?: number;
  attendance_status?: 'PENDIENTE' | 'ASISTIO' | 'NO_ASISTIO' | 'REPROGRAMADO';
  description?: string;
  visit_date?: string;
  assigned_user_ids?: number[];
}

export interface ServiceTypeCreate {
  name: string;
  description?: string;
}

const monthlyplanService = {
  // Planes mensuales
  async create(data: MonthlyPlanCreate): Promise<MonthlyPlan> {
    const response = await api.post('/api/monthly-plans/', data);
    return response.data;
  },

  async getAll(params?: {
    client_id?: number;
    branch_id?: number;
    area_id?: number;
    attendance_status?: string;
    assigned_user_id?: number;
    start_date?: string;
    end_date?: string;
  }): Promise<MonthlyPlan[]> {
    const response = await api.get('/api/monthly-plans/', { params });
    return response.data;
  },

  async getById(planId: number): Promise<MonthlyPlan> {
    const response = await api.get(`/api/monthly-plans/${planId}`);
    return response.data;
  },

  async update(planId: number, data: MonthlyPlanUpdate): Promise<MonthlyPlan> {
    const response = await api.put(`/api/monthly-plans/${planId}`, data);
    return response.data;
  },

  async delete(planId: number): Promise<void> {
    await api.delete(`/api/monthly-plans/${planId}`);
  },

  // Tipos de servicio
  async createServiceType(data: ServiceTypeCreate): Promise<ServiceType> {
    const response = await api.post('/api/service/', data);
    return response.data;
  },

  async getServiceTypes(): Promise<ServiceType[]> {
    const response = await api.get('/api/service/');
    return response.data;
  },

  async updateServiceType(typeId: number, data: Partial<ServiceTypeCreate>): Promise<ServiceType> {
    const response = await api.put(`/api/service/${typeId}`, data);
    return response.data;
  },

  async deleteServiceType(typeId: number): Promise<void> {
    await api.delete(`/api/service/${typeId}`);
  }
};

export default monthlyplanService;
