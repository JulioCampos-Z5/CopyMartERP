import { apiRequest, API_ENDPOINTS } from '@/config/api'

export const contactService = {
  async getContacts() {
    return apiRequest(`${API_ENDPOINTS.CONTACTS}/`)
  },

  async getContactById(id) {
    return apiRequest(`${API_ENDPOINTS.CONTACTS}/${id}`)
  },

  async searchContactByName(name) {
    return apiRequest(`${API_ENDPOINTS.CONTACTS}/search`, {
      params: { name }
    })
  },

  async createContact(contactData) {
    return apiRequest(`${API_ENDPOINTS.CONTACTS}/`, {
      method: 'POST',
      data: contactData
    })
  },

  async changeContactStatus(id, isActive) {
    return apiRequest(`${API_ENDPOINTS.CONTACTS}/${id}/status`, {
      method: 'PUT',
      params: { is_active: isActive }
    })
  }
}
