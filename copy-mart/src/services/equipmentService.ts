/**
 * Servicio de Equipos (TypeScript)
 * =================================
 */

import { apiGet, apiPost, apiPut, apiPatch, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Equipment, EquipmentFilters, Brand, Supplier, PaginatedResponse } from '@/types'

export const equipmentService = {
  async getEquipments(options: EquipmentFilters = {}): Promise<PaginatedResponse<Equipment>> {
    const { page = 1, pageSize = 10, page_size, search, location_status, type, brand_id, is_active } = options
    const params: Record<string, any> = {
      page,
      page_size: page_size || pageSize,
      ...(search && { search }),
      ...(location_status && { location_status }),
      ...(type && { type }),
      ...(brand_id && { brand_id }),
      ...(is_active !== undefined && { is_active })
    }
    const url = buildUrlWithParams(`${API_ENDPOINTS.EQUIPMENT}/`, params)
    const items = await apiGet<Equipment[]>(url)
    
    // El backend devuelve una lista directa, construir respuesta paginada
    const actualPageSize = page_size || pageSize
    return {
      items: items || [],
      page,
      page_size: actualPageSize,
      total: items?.length || 0,
      total_pages: 1
    }
  },

  async getEquipmentById(id: number): Promise<Equipment> {
    return apiGet<Equipment>(`${API_ENDPOINTS.EQUIPMENT}/${id}`)
  },

  async createEquipment(data: any): Promise<Equipment> {
    return apiPost<Equipment>(`${API_ENDPOINTS.EQUIPMENT}/`, data)
  },

  async updateEquipment(id: number, data: any): Promise<Equipment> {
    return apiPut<Equipment>(`${API_ENDPOINTS.EQUIPMENT}/${id}/`, data)
  },

  async deleteEquipment(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.EQUIPMENT}/${id}/`)
  },

  async updateEquipmentStatus(id: number, status: string): Promise<Equipment> {
    return apiPatch<Equipment>(`${API_ENDPOINTS.EQUIPMENT}/${id}/status`, { location_status: status })
  },

  async getBrands(): Promise<Brand[]> {
    return apiGet<Brand[]>(`${API_ENDPOINTS.BRANDS}/`)
  },

  async getBrandById(id: number): Promise<Brand> {
    return apiGet<Brand>(`${API_ENDPOINTS.BRANDS}/${id}/`)
  },

  async createBrand(data: Omit<Brand, 'brand_id'>): Promise<Brand> {
    return apiPost<Brand>(`${API_ENDPOINTS.BRANDS}/`, data)
  },

  async updateBrand(id: number, data: Partial<Brand>): Promise<Brand> {
    return apiPut<Brand>(`${API_ENDPOINTS.BRANDS}/${id}/`, data)
  },

  async deleteBrand(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.BRANDS}/${id}/`)
  },

  async getSuppliers(): Promise<Supplier[]> {
    return apiGet<Supplier[]>(`${API_ENDPOINTS.SUPPLIERS}/`)
  },

  async getSupplierById(id: number): Promise<Supplier> {
    return apiGet<Supplier>(`${API_ENDPOINTS.SUPPLIERS}/${id}/`)
  },

  async createSupplier(data: Omit<Supplier, 'supplier_id'>): Promise<Supplier> {
    return apiPost<Supplier>(`${API_ENDPOINTS.SUPPLIERS}/`, data)
  },

  async updateSupplier(id: number, data: Partial<Supplier>): Promise<Supplier> {
    return apiPut<Supplier>(`${API_ENDPOINTS.SUPPLIERS}/${id}/`, data)
  },

  async deleteSupplier(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.SUPPLIERS}/${id}/`)
  },
  
  // Alias de compatibilidad: algunas vistas usan getEquipment() para lista
  async getEquipment(): Promise<PaginatedResponse<Equipment>> {
    return equipmentService.getEquipments({ page: 1, pageSize: 1000 })
  }
}
