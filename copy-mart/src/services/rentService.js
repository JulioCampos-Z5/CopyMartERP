/**
 * Servicio de Rentas
 * ==================
 * Gestiona las operaciones CRUD para contratos de renta de equipos.
 * 
 * Endpoints:
 * - GET    /rents/           - Listar rentas con filtros
 * - POST   /rents/           - Crear nueva renta
 * - GET    /rents/{id}       - Obtener renta por ID
 * - PUT    /rents/{id}       - Actualizar renta
 * - DELETE /rents/{id}       - Cancelar renta
 * - PATCH  /rents/{id}/status - Cambiar estado del contrato
 */

import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

export const rentService = {
  /**
   * Obtiene lista de rentas con filtros opcionales
   * @param {Object} filters - Filtros opcionales
   * @param {number} filters.client_id - ID del cliente
   * @param {number} filters.branch_id - ID de la sucursal
   * @param {number} filters.area_id - ID del área
   * @param {string} filters.contract_status - Estado: pendiente, sin_firmar, vigente, vencido
   * @param {boolean} filters.is_foreign - Si es servicio foráneo
   * @param {boolean} filters.is_active - Si está activa
   */
  async getRents(filters = {}) {
    const url = buildUrlWithParams(API_ENDPOINTS.RENTS, filters)
    return apiRequest(url)
  },

  /**
   * Obtiene una renta por ID
   * @param {number} rentId - ID de la renta
   */
  async getRent(rentId) {
    return apiRequest(`${API_ENDPOINTS.RENTS}/${rentId}`)
  },

  /**
   * Crea una nueva renta
   * @param {Object} rentData - Datos de la renta
   * @param {number} rentData.client_id - ID del cliente (requerido)
   * @param {number} rentData.item_id - ID del equipo (requerido)
   * @param {number} rentData.rent - Monto de la renta (requerido)
   * @param {number} rentData.branch_id - ID de la sucursal (opcional)
   * @param {number} rentData.area_id - ID del área (opcional)
   * @param {string} rentData.contract_status - Estado inicial
   * @param {boolean} rentData.is_foreign - Si es foráneo
   */
  async createRent(rentData) {
    return apiRequest(`${API_ENDPOINTS.RENTS}/`, {
      method: 'POST',
      body: JSON.stringify(rentData)
    })
  },

  /**
   * Actualiza una renta existente
   * @param {number} rentId - ID de la renta
   * @param {Object} rentData - Datos a actualizar
   */
  async updateRent(rentId, rentData) {
    return apiRequest(`${API_ENDPOINTS.RENTS}/${rentId}`, {
      method: 'PUT',
      body: JSON.stringify(rentData)
    })
  },

  /**
   * Cancela una renta (devuelve equipo a bodega)
   * @param {number} rentId - ID de la renta
   */
  async deleteRent(rentId) {
    return apiRequest(`${API_ENDPOINTS.RENTS}/${rentId}`, {
      method: 'DELETE'
    })
  },

  /**
   * Actualiza el estado del contrato
   * @param {number} rentId - ID de la renta
   * @param {string} newStatus - Nuevo estado: pendiente, sin_firmar, vigente, vencido
   */
  async updateContractStatus(rentId, newStatus) {
    return apiRequest(`${API_ENDPOINTS.RENTS}/${rentId}/status?new_status=${newStatus}`, {
      method: 'PATCH'
    })
  },

  /**
   * Obtiene resumen de rentas por cliente
   * @param {number} clientId - ID del cliente
   */
  async getClientRentSummary(clientId) {
    return apiRequest(`${API_ENDPOINTS.RENTS}/client/${clientId}/summary`)
  }
}

export default rentService
