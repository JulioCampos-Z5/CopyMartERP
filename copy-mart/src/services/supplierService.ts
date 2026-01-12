/**
 * Servicio de Proveedores (TypeScript)
 * =====================================
 */

import { apiGet, apiPost, apiDelete, API_ENDPOINTS } from '@/config/api'
import type { Supplier, SupplierCreate } from '@/types'

export const supplierService = {
  async getSuppliers(): Promise<Supplier[]> {
    return apiGet<Supplier[]>(`${API_ENDPOINTS.SUPPLIERS}/`)
  },

  async createSupplier(supplierData: SupplierCreate): Promise<Supplier> {
    return apiPost<Supplier>(`${API_ENDPOINTS.SUPPLIERS}/`, supplierData)
  },

  async deleteSupplier(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.SUPPLIERS}/${id}/`)
  }
}
