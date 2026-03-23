import api from '@/config/api'

export interface SearchResult {
  type: string
  id: number
  title: string
  subtitle: string
  link: string
}

export interface ReportsSummary {
  clients: number
  sales: { total: number; this_month: number }
  rents: { total: number; active: number }
  billing: { overdue: number; pending: number }
  tickets: { open: number }
  equipment: { total: number }
  repairs: { pending: number }
  purchases: { active: number }
}

const systemService = {
  // Reports
  async getReportsSummary(): Promise<ReportsSummary> {
    const response = await api.get('/api/system/reports/summary')
    return response.data
  },

  async getSalesByMonth(months = 12): Promise<{ month: string; count: number }[]> {
    const response = await api.get('/api/system/reports/sales-by-month', { params: { months } })
    return response.data
  },

  async getRentsByStatus(): Promise<{ status: string; count: number }[]> {
    const response = await api.get('/api/system/reports/rents-by-status')
    return response.data
  },

  async getBillingAging(): Promise<Record<string, number>> {
    const response = await api.get('/api/system/reports/billing-aging')
    return response.data
  },

  async getTicketsByType(): Promise<{ type: string; count: number }[]> {
    const response = await api.get('/api/system/reports/tickets-by-type')
    return response.data
  },

  async getEquipmentByLocation(): Promise<{ location: string; count: number }[]> {
    const response = await api.get('/api/system/reports/equipment-by-location')
    return response.data
  },

  // Search
  async globalSearch(q: string): Promise<SearchResult[]> {
    const response = await api.get('/api/system/search', { params: { q } })
    return response.data
  },

  // SMTP
  async getSmtpConfig(): Promise<any> {
    const response = await api.get('/api/system/smtp/config')
    return response.data
  },

  async testSmtp(): Promise<{ success: boolean; message?: string; error?: string }> {
    const response = await api.post('/api/system/smtp/test')
    return response.data
  },

  // Backups
  async createBackup(): Promise<{ success: boolean; filename?: string; size_mb?: number; error?: string }> {
    const response = await api.post('/api/system/backup')
    return response.data
  },

  async listBackups(): Promise<{ filename: string; size_mb: number; created_at: string }[]> {
    const response = await api.get('/api/system/backups')
    return response.data
  },

  // DB Migrations
  async getDbTables(): Promise<any> {
    const response = await api.get('/api/system/db/tables')
    return response.data
  },

  async getTableColumns(tableName: string): Promise<any> {
    const response = await api.get(`/api/system/db/table/${tableName}/columns`)
    return response.data
  },

  async runMigration(): Promise<any> {
    const response = await api.post('/api/system/db/migrate')
    return response.data
  }
}

export default systemService
