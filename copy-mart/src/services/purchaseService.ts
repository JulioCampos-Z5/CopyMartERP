/**
 * Servicio de Compras (TypeScript)
 * =================================
 * Gestiona las operaciones de compras
 */

import { apiRequest, apiGet, apiPost, apiPut, apiPatch, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Purchase, PurchaseCreate, PurchaseFilters, PurchaseStatus, PaginatedResponse } from '@/types'

export const purchaseService = {
  /**
   * Obtener lista de compras con filtros y paginación
   */
  async getPurchases(options: PurchaseFilters = {}): Promise<PaginatedResponse<Purchase>> {
    const {
      page = 1,
      pageSize = 10,
      search,
      status,
      type,
      userId,
      sparepartId,
      startDate,
      endDate
    } = options

    const params: Record<string, any> = {
      page,
      page_size: pageSize,
      ...(search && { search }),
      ...(status && { status }),
      ...(type && { type }),
      ...(userId && { user_id: userId }),
      ...(sparepartId && { sparepart_id: sparepartId }),
      ...(startDate && { start_date: startDate }),
      ...(endDate && { end_date: endDate })
    }

    const url = buildUrlWithParams(`${API_ENDPOINTS.PURCHASES}/`, params)
    return apiGet<PaginatedResponse<Purchase>>(url)
  },

  /**
   * Obtener una compra por ID
   */
  async getPurchaseById(id: number): Promise<Purchase> {
    return apiGet<Purchase>(`${API_ENDPOINTS.PURCHASES}/${id}`)
  },

  /**
   * Crear nueva compra
   */
  async createPurchase(purchaseData: PurchaseCreate): Promise<Purchase> {
    return apiPost<Purchase>(`${API_ENDPOINTS.PURCHASES}/`, purchaseData)
  },

  /**
   * Actualizar compra existente
   */
  async updatePurchase(id: number, purchaseData: Partial<PurchaseCreate>): Promise<Purchase> {
    return apiPut<Purchase>(`${API_ENDPOINTS.PURCHASES}/${id}`, purchaseData)
  },

  /**
   * Actualizar estado de una compra
   */
  async updatePurchaseStatus(id: number, status: PurchaseStatus, comments?: string): Promise<Purchase> {
    return apiPatch<Purchase>(`${API_ENDPOINTS.PURCHASES}/${id}/status`, {
      status,
      ...(comments && { comments })
    })
  },

  /**
   * Eliminar compra
   */
  async deletePurchase(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.PURCHASES}/${id}`)
  },

  /**
   * Marcar compra como recibida
   */
  async markAsReceived(id: number, comments?: string): Promise<Purchase> {
    return this.updatePurchaseStatus(id, 'Concluido', comments)
  },

  /**
   * Cancelar compra
   */
  async cancelPurchase(id: number, comments?: string): Promise<Purchase> {
    return this.updatePurchaseStatus(id, 'Rechazado', comments)
  }
}
