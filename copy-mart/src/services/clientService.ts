/**
 * Servicio de Clientes (TypeScript)
 * ==================================
 */

import { apiGet, apiPost, apiPatch, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Client, ClientFilters, PaginatedResponse, Branch, BranchCreate, Area, AreaCreate } from '@/types'

export const clientService = {
  async getClients(options: ClientFilters = {}): Promise<PaginatedResponse<Client>> {
    const { page = 1, pageSize = 10, page_size, search, is_active } = options
    
    // Convertir page/pageSize a skip/limit para el backend
    const actualPageSize = page_size || pageSize
    const skip = (page - 1) * actualPageSize
    const limit = actualPageSize
    
    const params = {
      skip,
      limit,
      ...(search && { search }),
      ...(is_active !== undefined && { is_active })
    }
    const url = buildUrlWithParams(`${API_ENDPOINTS.CLIENTS}/`, params)
    const items = await apiGet<Client[]>(url)
    
    // El backend devuelve una lista, construir respuesta paginada
    return {
      items: items || [],
      page,
      page_size: actualPageSize,
      total: items?.length || 0,
      total_pages: 1
    }
  },

  async getClientById(id: number): Promise<Client> {
    return apiGet<Client>(`${API_ENDPOINTS.CLIENTS}/${id}`)
  },

  async createClient(clientData: Omit<Client, 'client_id' | 'created_at'>): Promise<Client> {
    return apiPost<Client>(`${API_ENDPOINTS.CLIENTS}/`, clientData)
  },

  async updateClient(id: number, clientData: Partial<Client>): Promise<Client> {
    return apiPatch<Client>(`${API_ENDPOINTS.CLIENTS}/${id}`, clientData)
  },

  async deleteClient(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.CLIENTS}/${id}`)
  },

  // ============================================
  // BRANCHES (SUCURSALES)
  // ============================================
  
  async getClientBranches(clientId: number): Promise<Branch[]> {
    return apiGet<Branch[]>(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches`)
  },

  async getBranchById(branchId: number): Promise<Branch> {
    return apiGet<Branch>(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}`)
  },

  async createBranch(clientId: number, branchData: BranchCreate): Promise<Branch> {
    return apiPost<Branch>(`${API_ENDPOINTS.CLIENTS}/${clientId}/branches`, branchData)
  },

  async updateBranch(branchId: number, branchData: Partial<Branch>): Promise<Branch> {
    return apiPatch<Branch>(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}`, branchData)
  },

  async deleteBranch(branchId: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}`)
  },

  // ============================================
  // AREAS
  // ============================================
  
  async getBranchAreas(branchId: number): Promise<Area[]> {
    return apiGet<Area[]>(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}/areas`)
  },

  async getAreaById(areaId: number): Promise<Area> {
    return apiGet<Area>(`${API_ENDPOINTS.CLIENTS}/areas/${areaId}`)
  },

  async createArea(branchId: number, areaData: AreaCreate): Promise<Area> {
    return apiPost<Area>(`${API_ENDPOINTS.CLIENTS}/branches/${branchId}/areas`, areaData)
  },

  async updateArea(areaId: number, areaData: Partial<Area>): Promise<Area> {
    return apiPatch<Area>(`${API_ENDPOINTS.CLIENTS}/areas/${areaId}`, areaData)
  },

  async deleteArea(areaId: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.CLIENTS}/areas/${areaId}`)
  }
}
