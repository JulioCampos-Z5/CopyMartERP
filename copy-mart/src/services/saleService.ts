/**
 * Servicio de Ventas (TypeScript)
 * ================================
 */

import { apiGet, apiPost, apiPut, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Sale, SaleFilters, PaginatedResponse } from '@/types'

export const saleService = {
  async getSales(options: SaleFilters = {}): Promise<PaginatedResponse<Sale>> {
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
    const url = buildUrlWithParams(`${API_ENDPOINTS.SALES}/`, params)
    const items = await apiGet<Sale[]>(url)
    
    // El backend devuelve una lista, construir respuesta paginada
    return {
      items: items || [],
      page,
      page_size: actualPageSize,
      total: items?.length || 0,
      total_pages: 1
    }
  },

  async getSaleById(id: number): Promise<Sale> {
    return apiGet<Sale>(`${API_ENDPOINTS.SALES}/${id}`)
  },

  async createSale(data: Omit<Sale, 'sale_id' | 'created_at'>): Promise<Sale> {
    return apiPost<Sale>(`${API_ENDPOINTS.SALES}/`, data)
  },

  async updateSale(id: number, data: Partial<Sale>): Promise<Sale> {
    return apiPut<Sale>(`${API_ENDPOINTS.SALES}/${id}`, data)
  },

  async deleteSale(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.SALES}/${id}`)
  }
}
