/**
 * Servicio de Compras
 * ===================
 * Gestiona las operaciones de compras de refacciones y equipos
 */

import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

// Enums para compras
export const PurchaseStatus = {
  PENDIENTE: 'PENDIENTE',
  EN_TRANSITO: 'EN_TRANSITO',
  RECIBIDO: 'RECIBIDO',
  CANCELADO: 'CANCELADO'
}

export const PurchaseType = {
  INTERNA: 'INTERNA',
  VENTA: 'VENTA'
}

export const purchaseService = {
  /**
   * Crear nueva compra
   */
  async createPurchase(purchaseData) {
    return apiRequest(API_ENDPOINTS.PURCHASES, {
      method: 'POST',
      data: purchaseData
    })
  },

  /**
   * Listar todas las compras con paginación y filtros
   */
  async getPurchases(options = {}) {
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

    const params = {
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

    const url = buildUrlWithParams(API_ENDPOINTS.PURCHASES, params)
    return apiRequest(url)
  },

  /**
   * Obtener una compra por ID
   */
  async getPurchaseById(purchaseId) {
    return apiRequest(`${API_ENDPOINTS.PURCHASES}/${purchaseId}`)
  },

  /**
   * Actualizar una compra
   */
  async updatePurchase(purchaseId, purchaseData) {
    return apiRequest(`${API_ENDPOINTS.PURCHASES}/${purchaseId}`, {
      method: 'PUT',
      data: purchaseData
    })
  },

  /**
   * Actualizar estado de una compra
   */
  async updatePurchaseStatus(purchaseId, status, comments = null) {
    return apiRequest(`${API_ENDPOINTS.PURCHASES}/${purchaseId}/status`, {
      method: 'PATCH',
      data: {
        status,
        ...(comments && { comments })
      }
    })
  },

  /**
   * Eliminar una compra
   */
  async deletePurchase(purchaseId) {
    return apiRequest(`${API_ENDPOINTS.PURCHASES}/${purchaseId}`, {
      method: 'DELETE'
    })
  },

  /**
   * Obtener compras pendientes
   */
  async getPendingPurchases() {
    return apiRequest(`${API_ENDPOINTS.PURCHASES}/pending`)
  },

  /**
   * Obtener estadísticas de compras
   */
  async getPurchaseStatistics() {
    return apiRequest(`${API_ENDPOINTS.PURCHASES}/statistics`)
  },

  /**
   * Marcar compra como recibida
   */
  async markAsReceived(purchaseId, comments = null) {
    return this.updatePurchaseStatus(purchaseId, PurchaseStatus.RECIBIDO, comments)
  },

  /**
   * Cancelar compra
   */
  async cancelPurchase(purchaseId, reason) {
    return this.updatePurchaseStatus(purchaseId, PurchaseStatus.CANCELADO, reason)
  }
}

export default purchaseService
