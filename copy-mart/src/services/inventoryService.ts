/**
 * Servicio de Inventario (TypeScript)
 * ====================================
 * Gestión de catálogo, items de inventario y estantes
 */

import { apiGet, apiPost, apiPut, apiPatch, apiDelete, API_ENDPOINTS, buildUrlWithParams } from '@/config/api'

// Enums
export type ColorType = 'k' | 'c' | 'm' | 'y'
export type QualityType = 'original' | 'generico' | 'reparado' | 'nueva' | 'usado' | 'n/a'
export type ItemType = 'toner' | 'refaccion'
export type SectionLocation = 'seccion_1' | 'seccion_2' | 'seccion_3' | 'seccion_4' | 'seccion_5' | 'seccion_6'

// Interfaces
export interface BrandSimple {
  brand_id: number
  name: string
  prefix: string
}

export interface SupplierSimple {
  supplier_id: number
  name: string
}

export interface EquipmentSimple {
  item_id: number
  model: string
  serie: string
}

export interface Shelf {
  shelf_id: number
  name: string
  section: SectionLocation
  description?: string
  created_at: string
  is_active: boolean
}

export interface ShelfCreate {
  name: string
  section: SectionLocation
  description?: string
}

export interface ShelfUpdate {
  name?: string
  section?: SectionLocation
  description?: string
  is_active?: boolean
}

export interface ItemCatalog {
  catalog_id: number
  item_name: string
  description?: string
  item_type: ItemType
  brand_id?: number
  color?: ColorType
  usage?: string
  created_at: string
  is_active: boolean
  brand?: BrandSimple
  total_items: number
  available_items: number
  stock_min: number
  stock_max: number
}

export interface ItemCatalogCreate {
  item_name: string
  description?: string
  item_type: ItemType
  brand_id?: number
  color?: ColorType
  usage?: string
  stock_min?: number
  stock_max?: number
}

export interface ItemCatalogUpdate {
  item_name?: string
  description?: string
  item_type?: ItemType
  brand_id?: number
  color?: ColorType
  usage?: string
  is_active?: boolean
}

export interface InventoryItem {
  inventory_id: number
  item_code: string
  catalog_id: number
  section: SectionLocation
  shelf_id?: number
  quality: QualityType
  entry_date: string
  supplier_id?: number
  invoice?: string
  cost?: number
  is_available: boolean
  comments?: string
  created_at: string
  updated_at: string
  is_active: boolean
  catalog_item?: ItemCatalog
  supplier?: SupplierSimple
  shelf?: Shelf
  equipments: EquipmentSimple[]
}

export interface InventoryItemCreate {
  catalog_id: number
  section: SectionLocation
  shelf_id?: number
  quality: QualityType
  supplier_id?: number
  invoice?: string
  cost?: number
  is_available?: boolean
  comments?: string
  equipment_ids?: number[]
}

export interface InventoryItemUpdate {
  catalog_id?: number
  section?: SectionLocation
  shelf_id?: number
  quality?: QualityType
  supplier_id?: number
  invoice?: string
  cost?: number
  is_available?: boolean
  comments?: string
  equipment_ids?: number[]
  is_active?: boolean
}

export interface BulkInventoryCreate {
  catalog_id: number
  quantity: number
  section: SectionLocation
  shelf_id?: number
  quality: QualityType
  supplier_id?: number
  invoice?: string
  cost?: number
  comments?: string
  equipment_ids?: number[]
}

export interface InventoryFilters {
  catalog_id?: number
  item_name?: string
  item_type?: ItemType
  section?: SectionLocation
  brand_id?: number
  quality?: QualityType
  color?: ColorType
  shelf_id?: number
  supplier_id?: number
  is_available?: boolean
  is_active?: boolean
  low_stock?: boolean
  search?: string
  skip?: number
  limit?: number
}

export interface CatalogFilters {
  item_type?: ItemType
  brand_id?: number
  is_active?: boolean
  search?: string
  skip?: number
  limit?: number
}

export interface StockUpdate {
  stock_min?: number
  stock_max?: number
}

export interface InventoryStats {
  total_catalog_items: number
  total_inventory_items: number
  total_toners: number
  total_refacciones: number
  available_items: number
  low_stock_items: number
  items_by_section: Record<string, number>
  items_by_quality: Record<string, number>
  total_value: number
}

// ==================== Servicio de Catálogo ====================
export const catalogService = {
  async getCatalogItems(filters: CatalogFilters = {}): Promise<ItemCatalog[]> {
    const params: Record<string, any> = {}
    if (filters.item_type) params.item_type = filters.item_type
    if (filters.brand_id) params.brand_id = filters.brand_id
    if (filters.is_active !== undefined) params.is_active = filters.is_active
    if (filters.search) params.search = filters.search
    if (filters.skip) params.skip = filters.skip
    if (filters.limit) params.limit = filters.limit

    const url = buildUrlWithParams(API_ENDPOINTS.CATALOG, params)
    return apiGet<ItemCatalog[]>(url)
  },

  async getCatalogItemById(id: number): Promise<ItemCatalog> {
    return apiGet<ItemCatalog>(`${API_ENDPOINTS.CATALOG}/${id}`)
  },

  async createCatalogItem(data: ItemCatalogCreate): Promise<ItemCatalog> {
    return apiPost<ItemCatalog>(API_ENDPOINTS.CATALOG, data)
  },

  async updateCatalogItem(id: number, data: ItemCatalogUpdate): Promise<ItemCatalog> {
    return apiPut<ItemCatalog>(`${API_ENDPOINTS.CATALOG}/${id}`, data)
  },

  async updateStockLevels(id: number, data: StockUpdate): Promise<any> {
    return apiPatch<any>(`${API_ENDPOINTS.CATALOG}/${id}/stock`, data)
  }
}

// ==================== Servicio de Inventario ====================
export const inventoryService = {
  async getInventoryItems(filters: InventoryFilters = {}): Promise<InventoryItem[]> {
    const params: Record<string, any> = {}
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params[key] = value
      }
    })

    const url = buildUrlWithParams(API_ENDPOINTS.INVENTORY, params)
    return apiGet<InventoryItem[]>(url)
  },

  async getInventoryItemById(id: number): Promise<InventoryItem> {
    return apiGet<InventoryItem>(`${API_ENDPOINTS.INVENTORY}/${id}`)
  },

  async createInventoryItem(data: InventoryItemCreate): Promise<InventoryItem> {
    return apiPost<InventoryItem>(API_ENDPOINTS.INVENTORY, data)
  },

  async createBulkInventory(data: BulkInventoryCreate): Promise<InventoryItem[]> {
    return apiPost<InventoryItem[]>(`${API_ENDPOINTS.INVENTORY}/bulk`, data)
  },

  async updateInventoryItem(id: number, data: InventoryItemUpdate): Promise<InventoryItem> {
    return apiPut<InventoryItem>(`${API_ENDPOINTS.INVENTORY}/${id}`, data)
  },

  async deleteInventoryItem(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.INVENTORY}/${id}`)
  },

  async getStats(): Promise<InventoryStats> {
    return apiGet<InventoryStats>(`${API_ENDPOINTS.INVENTORY}/stats`)
  }
}

// ==================== Servicio de Estantes ====================
export const shelfService = {
  async getShelves(section?: SectionLocation): Promise<Shelf[]> {
    const params: Record<string, any> = {}
    if (section) params.section = section
    
    const url = buildUrlWithParams(API_ENDPOINTS.SHELVES, params)
    return apiGet<Shelf[]>(url)
  },

  async getShelfById(id: number): Promise<Shelf> {
    return apiGet<Shelf>(`${API_ENDPOINTS.SHELVES}/${id}`)
  },

  async createShelf(data: ShelfCreate): Promise<Shelf> {
    return apiPost<Shelf>(API_ENDPOINTS.SHELVES, data)
  },

  async updateShelf(id: number, data: ShelfUpdate): Promise<Shelf> {
    return apiPut<Shelf>(`${API_ENDPOINTS.SHELVES}/${id}`, data)
  },

  async deleteShelf(id: number): Promise<void> {
    return apiDelete<void>(`${API_ENDPOINTS.SHELVES}/${id}`)
  }
}
