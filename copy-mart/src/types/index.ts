// ============================================
// TIPOS BASE
// ============================================

export interface PaginationParams {
  page?: number
  pageSize?: number
  page_size?: number
}

export interface PaginatedResponse<T> {
  items: T[]
  page: number
  page_size: number
  total: number
  total_pages: number
}

export interface ApiError {
  message: string
  detail?: string
  status?: number
}

// ============================================
// PURCHASE TYPES
// ============================================

export type PurchaseStatus = 
  | 'En Curso'
  | 'En Tránsito'
  | 'Solicitud Guía Almacén'
  | 'Falta Pago Proveedor'
  | 'Falta Factura'
  | 'Por Revisar'
  | 'Pausado Back Orders'
  | 'Concluido'
  | 'Rechazado'

export type PurchaseType = 'Interna' | 'Venta'

export interface Purchase {
  purchase_id: number
  name: string
  sparepart_id: number
  user_id: number
  amount: number
  type: PurchaseType
  status: PurchaseStatus
  shipping_code?: string
  shipping_method?: string
  shipping_cost?: number
  quality?: string
  justification?: string
  comments?: string
  created_at: string
  updated_at?: string
}

export interface PurchaseCreate {
  name: string
  sparepart_id: number
  amount: number
  type: PurchaseType
  status?: PurchaseStatus
  shipping_code?: string
  shipping_method?: string
  shipping_cost?: number
  quality?: string
  justification?: string
  comments?: string
}

export interface PurchaseFilters extends PaginationParams {
  search?: string
  status?: PurchaseStatus
  type?: PurchaseType
  userId?: number
  sparepartId?: number
  startDate?: string
  endDate?: string
}

// ============================================
// BILLING TYPES
// ============================================

export type BillingStatus = 'pendiente' | 'pagado' | 'vencido' | 'cancelado' | 'Pendiente' | 'Pagado' | 'Vencido' | 'Cancelado'
export type BillingType = 'venta' | 'renta' | 'Venta' | 'Renta'

export interface Billing {
  billing_id: number
  client_id: number
  client_name?: string
  client?: {
    client_id: number
    name: string
    comercial_name?: string
  }
  branch_id?: number
  branch_name?: string
  branch?: {
    branch_id: number
    name: string
  }
  area_id?: number
  billing_type: BillingType
  sale_id?: number
  rent_id?: number
  sale?: {
    sale_id: number
    invoice_number?: string
    sale_price: number
  }
  rent?: {
    rent_id: number
    contract_number?: string
    rent: number
  }
  amount?: number  // Campo del backend
  amount_subtotal?: number
  amount_tax?: number
  amount_total?: number
  target_date: string
  due_date: string
  payment_date?: string
  status: BillingStatus
  follow_up: boolean
  created_at: string
  updated_at?: string
  comment?: string
}

export interface BillingCreate {
  billing_type: BillingType
  rent_id?: number
  sale_id?: number
  target_date: string
  due_date: string
  payment_term?: number
  payment_day?: number
  follow_up?: boolean
  comment?: string
}

export interface BillingFilters extends PaginationParams {
  search?: string
  status?: BillingStatus
  billing_type?: BillingType
  client_id?: number
  startDate?: string
  start_date?: string
  endDate?: string
  end_date?: string
  follow_up?: boolean
}

// ============================================
// CLIENT TYPES
// ============================================

export interface Client {
  client_id: number
  name: string
  rfc?: string
  comercial_name?: string
  address?: string
  colonia?: string
  zip_code?: string
  city?: string
  is_active?: boolean
  created_at: string
  branches?: Branch[]
  contact?: Contact
  total_branches?: number
  total_areas?: number
  contact_name?: string
  contact_email?: string
  contact_phone?: string
  contact_rol?: string
}

export interface ClientFilters extends PaginationParams {
  search?: string
  is_active?: boolean
}

// ============================================
// BRANCH TYPES
// ============================================

export interface Branch {
  branch_id: number
  client_id: number
  is_main?: boolean
  name: string
  address?: string
  colonia?: string
  zip_code?: string
  city?: string
  created_at?: string
  areas?: Area[]
}

export interface BranchCreate {
  client_id: number
  is_main?: boolean
  name: string
  address?: string
  colonia?: string
  zip_code?: string
  city?: string
}

// ============================================
// AREA TYPES  
// ============================================

export interface Area {
  area_id: number
  branch_id: number
  name: string
  created_at?: string
}

export interface AreaCreate {
  branch_id: number
  name: string
}

// ============================================
// CONTACT TYPES
// ============================================

export interface Contact {
  contact_id: number
  client_id?: number
  branch_id?: number
  area_id?: number
  name: string
  position?: string
  phone?: string
  email?: string
  company?: string
  rol?: string
  is_primary?: boolean
  is_client?: boolean
  is_active?: boolean
  created_at?: string
  updated_at?: string
}

export interface ContactFilters extends PaginationParams {
  search?: string
  client_id?: number
  branch_id?: number
  is_active?: boolean
}

// ============================================
// SPAREPART TYPES
// ============================================

export type SparepartColor = 'NA' | 'K' | 'C' | 'M' | 'Y' | 'COLOR'

export interface Sparepart {
  sparepart_id: number
  sku: string
  name: string
  model?: string
  color: SparepartColor
  brand: string
  supplier: string
  stock: number
  min_stock?: number
  price: number
  created_at: string
}

export interface SparepartFilters extends PaginationParams {
  search?: string
  color?: SparepartColor
  brand?: string
  supplier?: string
  low_stock?: boolean
}

// ============================================
// EQUIPMENT TYPES
// ============================================

export type EquipmentType = 'monocromo' | 'color'
export type LocationStatus = 'bodega' | 'asignado' | 'vendido' | 'taller' | 'desconocido'

export interface Brand {
  brand_id: number
  name: string
  prefix: string
}

export interface Supplier {
  supplier_id: number
  name: string
}

export interface Equipment {
  equipment_id: number
  brand?: Brand
  brand_id: number
  model: string
  serie: string
  sku?: string
  model_toner: string
  type: EquipmentType
  supplier_id: number
  location_status: LocationStatus
  is_active: boolean
  invoice?: string
  cost?: number
  comments?: string
  created_at: string
}

export interface EquipmentFilters extends PaginationParams {
  search?: string
  location_status?: LocationStatus
  type?: EquipmentType
  brand_id?: number
  is_active?: boolean
}

// ============================================
// SALE TYPES
// ============================================

export interface Sale {
  sale_id: number
  invoice_number: string
  client_id: number
  client_name?: string
  total_amount: number
  created_at: string
}

export interface SaleFilters extends PaginationParams {
  search?: string
  client_id?: number
}

// ============================================
// RENT TYPES
// ============================================

export interface Rent {
  rent_id: number
  contract_number: string
  client_id: number
  client_name?: string
  monthly_rent: number
  created_at: string
}

export interface RentFilters extends PaginationParams {
  search?: string
  client_id?: number
}

// ============================================
// USER TYPES
// ============================================

export interface User {
  user_id: number
  username: string
  email: string
  full_name: string
  role: string
  permissions: string[]
  is_active: boolean
  created_at: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

// ============================================
// BRAND TYPES
// ============================================

export interface Brand {
  brand_id: number
  name: string
  prefix: string
}

export interface BrandCreate {
  name: string
  prefix: string
}

// ============================================
// SUPPLIER TYPES
// ============================================

export interface Supplier {
  supplier_id: number
  name: string
}

export interface SupplierCreate {
  name: string
}
