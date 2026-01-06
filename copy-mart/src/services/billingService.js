/**
 * Servicio de Facturación/Cobranza
 * =================================
 * Gestiona las operaciones para facturación de rentas y ventas.
 */

import { apiRequest, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

export const billingService = {
  async getBillings(filters = {}) {
    const url = buildUrlWithParams(API_ENDPOINTS.BILLINGS, filters)
    return apiRequest(url)
  },

  async getBilling(billingId) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/${billingId}`)
  },

  async createBilling(billingData) {
    return apiRequest(API_ENDPOINTS.BILLINGS, {
      method: 'POST',
      body: JSON.stringify(billingData)
    })
  },

  async updateBilling(billingId, billingData) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/${billingId}`, {
      method: 'PUT',
      body: JSON.stringify(billingData)
    })
  },

  async deleteBilling(billingId) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/${billingId}`, {
      method: 'DELETE'
    })
  },

  async markAsPaid(billingId, paymentData) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/${billingId}/pay`, {
      method: 'PATCH',
      body: JSON.stringify(paymentData)
    })
  },

  async getOverdueBillings(skip = 0, limit = 100) {
    const url = buildUrlWithParams(`${API_ENDPOINTS.BILLINGS}/overdue`, { skip, limit })
    return apiRequest(url)
  },

  async getPendingBillings(skip = 0, limit = 100) {
    const url = buildUrlWithParams(`${API_ENDPOINTS.BILLINGS}/pending`, { skip, limit })
    return apiRequest(url)
  },

  async getFollowUpBillings(skip = 0, limit = 100) {
    const url = buildUrlWithParams(`${API_ENDPOINTS.BILLINGS}/follow-up`, { skip, limit })
    return apiRequest(url)
  },

  async toggleFollowUp(billingId, followUp) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/${billingId}/follow-up`, {
      method: 'PATCH',
      params: { follow_up: followUp }
    })
  },

  async getClientBillingSummary(clientId) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/client/${clientId}/summary`)
  },

  async updateOverdueBillings() {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/update-overdue`, {
      method: 'POST'
    })
  },

  async getStats(filters = {}) {
    const url = buildUrlWithParams(`${API_ENDPOINTS.BILLINGS}/stats`, filters)
    return apiRequest(url)
  },

  async createBatchBillings(batchData) {
    return apiRequest(`${API_ENDPOINTS.BILLINGS}/batch`, {
      method: 'POST',
      body: JSON.stringify(batchData)
    })
  }
}

export default billingService
