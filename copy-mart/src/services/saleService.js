/**
 * Servicio de Ventas
 * ==================
 * Gestiona las operaciones CRUD para ventas de equipos.
 * 
 * Endpoints:
 * - GET    /sales/                    - Listar ventas con filtros
 * - POST   /sales/                    - Crear nueva venta
 * - GET    /sales/{id}                - Obtener venta por ID
 * - PUT    /sales/{id}                - Actualizar venta
 * - DELETE /sales/{id}                - Cancelar venta
 * - PATCH  /sales/{id}/status         - Cambiar estado de venta
 * - GET    /sales/client/{id}/summary - Resumen de ventas por cliente
 */

import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

export const saleService = {
  /**
   * Obtiene lista de ventas con filtros opcionales
   * @param {Object} filters - Filtros opcionales
   * @param {number} filters.client_id - ID del cliente
   * @param {number} filters.branch_id - ID de la sucursal
   * @param {number} filters.area_id - ID del área
   * @param {string} filters.sale_status - Estado: pendiente, confirmada, entregada, cancelada
   * @param {boolean} filters.is_foreign - Si es servicio foráneo
   * @param {boolean} filters.is_active - Si está activa
   */
  async getSales(filters = {}) {
    const url = buildUrlWithParams(API_ENDPOINTS.SALES, filters)
    console.log('🔍 getSales - API_ENDPOINTS.SALES:', API_ENDPOINTS.SALES)
    console.log('🔍 getSales - filters:', filters)
    console.log('🔍 getSales - URL construida:', url)
    return apiRequest(url)
  },

  /**
   * Obtiene una venta por ID
   * @param {number} saleId - ID de la venta
   */
  async getSale(saleId) {
    return apiRequest(`${API_ENDPOINTS.SALES}/${saleId}`)
  },

  /**
   * Crea una nueva venta
   * @param {Object} saleData - Datos de la venta
   * @param {number} saleData.client_id - ID del cliente (requerido)
   * @param {number} saleData.item_id - ID del equipo (requerido)
   * @param {number} saleData.sale_price - Precio de venta (requerido)
   * @param {number} saleData.branch_id - ID de la sucursal (opcional)
   * @param {number} saleData.area_id - ID del área (opcional)
   * @param {string} saleData.sale_status - Estado inicial
   * @param {boolean} saleData.is_foreign - Si es foráneo
   */
  async createSale(saleData) {
    return apiRequest(`${API_ENDPOINTS.SALES}/`, {
      method: 'POST',
      body: JSON.stringify(saleData)
    })
  },

  /**
   * Actualiza una venta existente
   * @param {number} saleId - ID de la venta
   * @param {Object} saleData - Datos a actualizar
   */
  async updateSale(saleId, saleData) {
    return apiRequest(`${API_ENDPOINTS.SALES}/${saleId}`, {
      method: 'PUT',
      body: JSON.stringify(saleData)
    })
  },

  /**
   * Cancela una venta (devuelve equipo a bodega)
   * @param {number} saleId - ID de la venta
   */
  async deleteSale(saleId) {
    return apiRequest(`${API_ENDPOINTS.SALES}/${saleId}`, {
      method: 'DELETE'
    })
  },

  /**
   * Actualiza el estado de la venta
   * @param {number} saleId - ID de la venta
   * @param {string} newStatus - Nuevo estado: pendiente, confirmada, entregada, cancelada
   */
  async updateSaleStatus(saleId, newStatus) {
    return apiRequest(`${API_ENDPOINTS.SALES}/${saleId}/status?new_status=${newStatus}`, {
      method: 'PATCH'
    })
  },

  /**
   * Obtiene resumen de ventas por cliente
   * @param {number} clientId - ID del cliente
   */
  async getClientSaleSummary(clientId) {
    return apiRequest(`${API_ENDPOINTS.SALES}/client/${clientId}/summary`)
  }
}

export default saleService
