import api from '@/config/api'

export interface AppNotification {
  id: number
  user_id: number
  type: string
  title: string
  message: string | null
  link: string | null
  is_read: boolean
  created_at: string
}

const notificationService = {
  async getAll(params?: { skip?: number; limit?: number; unread_only?: boolean }): Promise<AppNotification[]> {
    const response = await api.get('/api/notifications/', { params })
    return response.data
  },

  async getUnreadCount(): Promise<number> {
    const response = await api.get('/api/notifications/unread-count')
    return response.data.count
  },

  async markAsRead(id: number): Promise<void> {
    await api.put(`/api/notifications/${id}/read`)
  },

  async markAllRead(): Promise<number> {
    const response = await api.put('/api/notifications/read-all')
    return response.data.marked
  },

  async generateNotifications(): Promise<void> {
    await api.post('/api/notifications/generate')
  }
}

export default notificationService
