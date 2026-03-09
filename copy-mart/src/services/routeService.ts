import { apiGet, apiPost, apiPut, apiDelete, API_ENDPOINTS } from '@/config/api'

export interface Route {
  route_id: number
  route_code: string
  driver_name: string
  vehicle: string | null
  status: string
  scheduled_date: string
  total_stops: number
  completed_stops: number
  notes: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface RouteCreate {
  route_code: string
  driver_name: string
  vehicle?: string
  status?: string
  scheduled_date: string
  total_stops?: number
  completed_stops?: number
  notes?: string
}

export const routeService = {
  async getRoutes(params: Record<string, any> = {}): Promise<Route[]> {
    const query = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') query.append(k, String(v))
    })
    const url = `${API_ENDPOINTS.ROUTES}/${query.toString() ? '?' + query.toString() : ''}`
    return apiGet<Route[]>(url)
  },

  async getRouteById(id: number): Promise<Route> {
    return apiGet<Route>(`${API_ENDPOINTS.ROUTES}/${id}`)
  },

  async createRoute(data: RouteCreate): Promise<Route> {
    return apiPost<Route>(`${API_ENDPOINTS.ROUTES}/`, data)
  },

  async updateRoute(id: number, data: Partial<RouteCreate>): Promise<Route> {
    return apiPut<Route>(`${API_ENDPOINTS.ROUTES}/${id}`, data)
  },

  async deleteRoute(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.ROUTES}/${id}`)
  }
}
