/**
 * Servicio de Contactos (TypeScript)
 * ===================================
 */

import { apiGet, apiPost, apiPatch, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'
import type { Contact, ContactFilters, PaginatedResponse } from '@/types'

export const contactService = {
  async getContacts(options: ContactFilters = {}): Promise<PaginatedResponse<Contact>> {
    const { page = 1, pageSize = 10, page_size, search, client_id, branch_id, is_active } = options
    
    const actualPageSize = page_size || pageSize
    const skip = (page - 1) * actualPageSize
    const limit = actualPageSize
    
    const params = {
      skip,
      limit,
      ...(search && { search }),
      ...(client_id && { client_id }),
      ...(branch_id && { branch_id }),
      ...(is_active !== undefined && { is_active })
    }
    const url = buildUrlWithParams(`${API_ENDPOINTS.CONTACTS}/`, params)
    const items = await apiGet<Contact[]>(url)
    
    return {
      items: items || [],
      page,
      page_size: actualPageSize,
      total: items?.length || 0,
      total_pages: 1
    }
  },

  async getContactById(id: number): Promise<Contact> {
    return apiGet<Contact>(`${API_ENDPOINTS.CONTACTS}/${id}`)
  },

  async createContact(contactData: Omit<Contact, 'contact_id' | 'created_at' | 'updated_at'>): Promise<Contact> {
    return apiPost<Contact>(`${API_ENDPOINTS.CONTACTS}/`, contactData)
  },

  async updateContact(id: number, contactData: Partial<Contact>): Promise<Contact> {
    return apiPatch<Contact>(`${API_ENDPOINTS.CONTACTS}/${id}`, contactData)
  },

  async deleteContact(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.CONTACTS}/${id}`)
  }
}
