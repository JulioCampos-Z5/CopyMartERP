const API_URL = 'http://localhost:8000'

export const contactService = {
  // Obtener todos los contactos
  async getContacts() {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/api/contacts/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) throw new Error('Error al obtener contactos')
    return response.json()
  },

  // Obtener un contacto por ID
  async getContactById(id) {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/api/contacts/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) throw new Error('Error al obtener contacto')
    return response.json()
  },

  // Buscar contacto por nombre
  async searchContactByName(name) {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/api/contacts/search?name=${encodeURIComponent(name)}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) throw new Error('Error al buscar contacto')
    return response.json()
  },

  // Crear un nuevo contacto
  async createContact(contactData) {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/api/contacts/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contactData)
    })
    if (!response.ok) throw new Error('Error al crear contacto')
    return response.json()
  },

  // Cambiar estado de un contacto
  async changeContactStatus(id, isActive) {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_URL}/api/contacts/${id}/status?is_active=${isActive}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) throw new Error('Error al cambiar estado del contacto')
    return response.json()
  }
}
