import { apiGet, apiPost, apiPut, apiDelete, API_ENDPOINTS } from '@/config/api'

export interface RouteStop {
  stop_id: number
  route_id: number
  client_id: number | null
  branch_id: number | null
  client_name: string | null
  branch_name: string | null
  stop_order: number
  address: string | null
  city: string | null
  notes: string | null
  is_completed: boolean
  visit_status: 'pendiente' | 'visitado' | 'no_visitado' | 'reagendado'
  no_visit_reason: string | null
  created_at: string
}

export interface RouteStopCreate {
  client_id?: number | null
  branch_id?: number | null
  stop_order?: number
  address?: string
  city?: string
  notes?: string
}

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
  stops: RouteStop[]
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
  },

  // Stops
  async getStops(routeId: number): Promise<RouteStop[]> {
    return apiGet<RouteStop[]>(`${API_ENDPOINTS.ROUTES}/${routeId}/stops`)
  },

  async addStop(routeId: number, data: RouteStopCreate): Promise<RouteStop> {
    return apiPost<RouteStop>(`${API_ENDPOINTS.ROUTES}/${routeId}/stops`, data)
  },

  async updateStop(stopId: number, data: Partial<RouteStopCreate & { is_completed?: boolean }>): Promise<RouteStop> {
    return apiPut<RouteStop>(`${API_ENDPOINTS.ROUTES}/stops/${stopId}`, data)
  },

  async deleteStop(stopId: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.ROUTES}/stops/${stopId}`)
  }
}
