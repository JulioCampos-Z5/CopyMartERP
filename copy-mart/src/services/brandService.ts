/**
 * Servicio de Marcas (TypeScript)
 * ================================
 */

import { apiGet, apiPost, apiDelete, API_ENDPOINTS } from '@/config/api'
import type { Brand, BrandCreate } from '@/types'

export const brandService = {
  async getBrands(): Promise<Brand[]> {
    return apiGet<Brand[]>(`${API_ENDPOINTS.BRANDS}/`)
  },

  async createBrand(brandData: BrandCreate): Promise<Brand> {
    return apiPost<Brand>(`${API_ENDPOINTS.BRANDS}/`, brandData)
  },

  async deleteBrand(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.BRANDS}/${id}/`)
  }
}
