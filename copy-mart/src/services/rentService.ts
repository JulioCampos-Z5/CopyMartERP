/**
 * Servicio de Rentas (TypeScript)
 * ================================
 */

import { apiGet, apiPost, apiPut, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Rent, RentFilters, PaginatedResponse } from '@/types'

export const rentService = {
  async getRents(options: RentFilters = {}): Promise<PaginatedResponse<Rent>> {
    const { page = 1, pageSize = 10, page_size, search, client_id } = options
    
    // Convertir page/pageSize a skip/limit para el backend
    const actualPageSize = page_size || pageSize
    const skip = (page - 1) * actualPageSize
    const limit = actualPageSize
    
    const params: Record<string, any> = {
      skip,
      limit,
      ...(search && { search }),
      ...(client_id && { client_id })
    }
    const url = buildUrlWithParams(`${API_ENDPOINTS.RENTS}/`, params)
    const items = await apiGet<Rent[]>(url)
    
    // El backend devuelve una lista, construir respuesta paginada
    return {
      items: items || [],
      page,
      page_size: actualPageSize,
      total: items?.length || 0,
      total_pages: 1
    }
  },

  async getRentById(id: number): Promise<Rent> {
    return apiGet<Rent>(`${API_ENDPOINTS.RENTS}/${id}`)
  },

  async createRent(data: Omit<Rent, 'rent_id' | 'created_at'>): Promise<Rent> {
    return apiPost<Rent>(`${API_ENDPOINTS.RENTS}/`, data)
  },

  async updateRent(id: number, data: Partial<Rent>): Promise<Rent> {
    return apiPut<Rent>(`${API_ENDPOINTS.RENTS}/${id}`, data)
  },

  async deleteRent(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.RENTS}/${id}`)
  }
}
