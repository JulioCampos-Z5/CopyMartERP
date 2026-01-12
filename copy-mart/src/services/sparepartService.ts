/**
 * Servicio de Refacciones (TypeScript)
 * ====================================
 */

import { apiGet, apiPost, apiPut, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Sparepart, SparepartFilters, PaginatedResponse } from '@/types'

export const sparepartService = {
  async getSpareparts(options: SparepartFilters = {}): Promise<PaginatedResponse<Sparepart>> {
    const { page = 1, pageSize = 10, page_size, search, brand, color, supplier, low_stock } = options
    const params: Record<string, any> = {
      page,
      page_size: page_size || pageSize,
      ...(search && { search }),
      ...(brand && { brand }),
      ...(color && { color }),
      ...(supplier && { supplier }),
      ...(low_stock !== undefined && { low_stock })
    }
    const url = buildUrlWithParams(API_ENDPOINTS.SPAREPARTS, params)
    return apiGet<PaginatedResponse<Sparepart>>(url)
  },

  async getSparepartById(id: number): Promise<Sparepart> {
    return apiGet<Sparepart>(`${API_ENDPOINTS.SPAREPARTS}/${id}`)
  },

  async createSparepart(data: Omit<Sparepart, 'sparepart_id' | 'created_at'>): Promise<Sparepart> {
    return apiPost<Sparepart>(API_ENDPOINTS.SPAREPARTS, data)
  },

  async updateSparepart(id: number, data: Partial<Sparepart>): Promise<Sparepart> {
    return apiPut<Sparepart>(`${API_ENDPOINTS.SPAREPARTS}/${id}`, data)
  },

  async deleteSparepartById(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.SPAREPARTS}/${id}`)
  }
}
