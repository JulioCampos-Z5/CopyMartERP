import api from '@/config/api'

export interface AuditLog {
  id: number
  user_id: number | null
  action: string
  module: string
  record_id: number | null
  detail: string | null
  ip_address: string | null
  created_at: string
  user_name: string | null
}

const auditService = {
  async getLogs(params?: {
    skip?: number
    limit?: number
    module?: string
    action?: string
    user_id?: number
  }): Promise<AuditLog[]> {
    const response = await api.get('/api/audit/', { params })
    return response.data
  },

  async getCount(params?: {
    module?: string
    action?: string
    user_id?: number
  }): Promise<number> {
    const response = await api.get('/api/audit/count', { params })
    return response.data.count
  },

  async createLog(data: {
    action: string
    module: string
    record_id?: number
    detail?: string
  }): Promise<AuditLog> {
    const response = await api.post('/api/audit/', data)
    return response.data
  }
}

export default auditService
