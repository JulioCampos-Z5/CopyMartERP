/**
 * Servicio de Refacciones
 * =======================
 * Gestiona las operaciones de refacciones/repuestos
 */

import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

export const sparepartService = {
  /**
   * Crear nueva refacción
   */
  async createSparepart(sparepartData) {
    return apiRequest(API_ENDPOINTS.SPAREPARTS, {
      method: 'POST',
      data: sparepartData
    })
  },

  /**
   * Listar todas las refacciones con paginación y filtros
   */
  async getSpareparts(options = {}) {
    const {
      page = 1,
      pageSize = 10,
      search,
      brand,
      color,
      supplier
    } = options

    const params = {
      page,
      page_size: pageSize,
      ...(search && { search }),
      ...(brand && { brand }),
      ...(color && { color }),
      ...(supplier && { supplier })
    }

    const url = buildUrlWithParams(API_ENDPOINTS.SPAREPARTS, params)
    return apiRequest(url)
  },

  /**
   * Obtener una refacción por ID
   */
  async getSparepartById(sparepartId) {
    return apiRequest(`${API_ENDPOINTS.SPAREPARTS}/${sparepartId}`)
  },

  /**
   * Obtener una refacción por código
   */
  async getSparepartByCode(code) {
    return apiRequest(`${API_ENDPOINTS.SPAREPARTS}/code/${code}`)
  },

  /**
   * Actualizar una refacción
   */
  async updateSparepart(sparepartId, sparepartData) {
    return apiRequest(`${API_ENDPOINTS.SPAREPARTS}/${sparepartId}`, {
      method: 'PUT',
      data: sparepartData
    })
  },

  /**
   * Eliminar una refacción
   */
  async deleteSparepart(sparepartId) {
    return apiRequest(`${API_ENDPOINTS.SPAREPARTS}/${sparepartId}`, {
      method: 'DELETE'
    })
  },

  /**
   * Actualizar stock de una refacción
   */
  async updateStock(sparepartId, stockData) {
    return apiRequest(`${API_ENDPOINTS.SPAREPARTS}/${sparepartId}/stock`, {
      method: 'PATCH',
      data: stockData
    })
  },

  /**
   * Buscar refacciones por término
   */
  async searchSpareparts(searchTerm) {
    const params = { search: searchTerm }
    const url = buildUrlWithParams(API_ENDPOINTS.SPAREPARTS, params)
    return apiRequest(url)
  },

  /**
   * Obtener refacciones con stock bajo
   */
  async getLowStockSpareparts(threshold = 10) {
    return apiRequest(`${API_ENDPOINTS.SPAREPARTS}/low-stock`, {
      params: { threshold }
    })
  },

  /**
   * Obtener refacciones por marca
   */
  async getSparepartsByBrand(brand) {
    const params = { brand }
    const url = buildUrlWithParams(API_ENDPOINTS.SPAREPARTS, params)
    return apiRequest(url)
  },

  /**
   * Obtener refacciones por proveedor
   */
  async getSparepartsBySupplier(supplier) {
    const params = { supplier }
    const url = buildUrlWithParams(API_ENDPOINTS.SPAREPARTS, params)
    return apiRequest(url)
  }
}

export default sparepartService
