/**
 * Servicio de Facturación (TypeScript)
 * ====================================
 * Gestiona las operaciones de facturación
 */

import { apiGet, apiPost, apiPut, apiPatch, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Billing, BillingCreate, BillingFilters, PaginatedResponse } from '@/types'

interface PaymentData {
  payment_date: string
  comments?: string
  payment_method?: string
}

interface BillingStats {
  pending_amount: number
  paid_amount: number
  by_status: Record<string, number>
}

export const billingService = {
  /**
   * Obtener lista de facturas con filtros y paginación
   */
  async getBillings(options: BillingFilters = {}): Promise<PaginatedResponse<Billing>> {
    const {
      page = 1,
      pageSize = 10,
      page_size,
      search,
      status,
      billing_type,
      client_id,
      startDate,
      start_date,
      endDate,
      end_date,
      follow_up,
      is_active = true
    } = options

    // Convertir page/pageSize a skip/limit para el backend
    const actualPageSize = page_size || pageSize
    const skip = (page - 1) * actualPageSize
    const limit = actualPageSize

    const params: Record<string, any> = {
      skip,
      limit,
      ...(search && { search }),
      ...(status && { status }),
      ...(billing_type && { billing_type }),
      ...(client_id && { client_id }),
      ...(start_date && { date_from: start_date }),
      ...(startDate && !start_date && { date_from: startDate }),
      ...(end_date && { date_to: end_date }),
      ...(endDate && !end_date && { date_to: endDate }),
      ...(follow_up !== undefined && { follow_up }),
      is_active
    }

    const url = buildUrlWithParams(`${API_ENDPOINTS.BILLINGS}/`, params)
    const items = await apiGet<Billing[]>(url)
    
    // El backend devuelve una lista, construir respuesta paginada
    return {
      items: items || [],
      page,
      page_size: actualPageSize,
      total: items?.length || 0,
      total_pages: 1
    }
  },

  /**
   * Obtener una factura por ID
   */
  async getBillingById(id: number): Promise<Billing> {
    return apiGet<Billing>(`${API_ENDPOINTS.BILLINGS}/${id}`)
  },

  /**
   * Crear nueva factura
   */
  async createBilling(billingData: BillingCreate): Promise<Billing> {
    return apiPost<Billing>(`${API_ENDPOINTS.BILLINGS}/`, billingData)
  },

  /**
   * Actualizar factura existente
   */
  async updateBilling(id: number, billingData: Partial<BillingCreate>): Promise<Billing> {
    return apiPut<Billing>(`${API_ENDPOINTS.BILLINGS}/${id}`, billingData)
  },

  /**
   * Marcar factura como pagada
   */
  async markAsPaid(id: number, paymentData: PaymentData): Promise<Billing> {
    return apiPatch<Billing>(`${API_ENDPOINTS.BILLINGS}/${id}/pay`, paymentData)
  },

  /**
   * Cambiar estado de seguimiento
   */
  async toggleFollowUp(id: number, followUp: boolean): Promise<Billing> {
    return apiPatch<Billing>(`${API_ENDPOINTS.BILLINGS}/${id}/follow-up`, { follow_up: followUp })
  },

  /**
   * Obtener facturas vencidas
   */
  async getOverdueBillings(): Promise<Billing[]> {
    return apiGet<Billing[]>(`${API_ENDPOINTS.BILLINGS}/overdue`)
  },

  /**
   * Obtener facturas pendientes
   */
  async getPendingBillings(): Promise<Billing[]> {
    return apiGet<Billing[]>(`${API_ENDPOINTS.BILLINGS}/pending`)
  },

  /**
   * Obtener facturas en seguimiento
   */
  async getFollowUpBillings(): Promise<Billing[]> {
    return apiGet<Billing[]>(`${API_ENDPOINTS.BILLINGS}/follow-up`)
  },

  /**
   * Obtener resumen de facturación por cliente
   */
  async getClientBillingSummary(clientId: number): Promise<any> {
    return apiGet<any>(`${API_ENDPOINTS.BILLINGS}/client/${clientId}/summary`)
  },

  /**
   * Actualizar facturas vencidas automáticamente
   */
  async updateOverdueBillings(): Promise<{ updated: number }> {
    return apiPost<{ updated: number }>(`${API_ENDPOINTS.BILLINGS}/update-overdue`, {})
  },

  /**
   * Obtener estadísticas de facturación
   * Intenta consumir /api/billings/stats; si no existe, calcula con un fallback.
   */
  getStats: async (): Promise<BillingStats> => {
    // 1) Intentar endpoint dedicado
    try {
      const stats = await apiGet<BillingStats>(`${API_ENDPOINTS.BILLINGS}/stats`)
      // Validar estructura mínima
      if (stats && typeof stats === 'object') {
        const by_status = stats.by_status || {}
        return {
          pending_amount: Number(stats.pending_amount || 0),
          paid_amount: Number(stats.paid_amount || 0),
          by_status: {
            pendiente: Number(by_status.pendiente || by_status.Pendiente || 0),
            pagada: Number(by_status.pagada || by_status.Pagada || 0),
            vencida: Number(by_status.vencida || by_status.Vencida || 0),
            cancelada: Number(by_status.cancelada || by_status.Cancelada || 0)
          }
        }
      }
    } catch (e) {
      // Continuar con fallback si el endpoint no existe o falla
    }

    // 2) Fallback: calcular a partir del listado (primera página grande)
    try {
      const response = await billingService.getBillings({ page: 1, page_size: 1000 })
      const items = response.items || []

      const now = new Date()
      const currentMonth = now.getMonth()
      const currentYear = now.getFullYear()

      let pending_amount = 0
      let paid_amount = 0
      const by_status: Record<string, number> = { pendiente: 0, pagada: 0, vencida: 0, cancelada: 0 }

      items.forEach((b: any) => {
        const status = String(b.status || '').toLowerCase()
        const total = Number(b.amount_total || b.amount || 0)

        if (status === 'pendiente') pending_amount += total

        // Pagadas este mes
        if (status === 'pagada') {
          by_status.pagada += 1
          if (b.payment_date) {
            const d = new Date(b.payment_date)
            if (!isNaN(d.getTime()) && d.getMonth() === currentMonth && d.getFullYear() === currentYear) {
              paid_amount += total
            }
          }
        } else if (status === 'vencida') {
          by_status.vencida += 1
        } else if (status === 'pendiente') {
          by_status.pendiente += 1
        } else if (status === 'cancelada') {
          by_status.cancelada += 1
        }
      })

      return { pending_amount, paid_amount, by_status }
    } catch (e) {
      // Si también falla, retornar estructura vacía para evitar romper la vista
      return { pending_amount: 0, paid_amount: 0, by_status: { pendiente: 0, pagada: 0, vencida: 0, cancelada: 0 } }
    }
  }
}
