/**
 * Store de Filtros y Paginación
 * ==============================
 * Centraliza y persiste el estado de filtros y paginación para listas
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { PaginationParams } from '@/types'

interface FilterState {
  [key: string]: any
}

interface PaginationState {
  page: number
  page_size: number
  total: number
  total_pages: number
}

export const useFiltersStore = defineStore('filters', () => {
  // ============================================
  // STATE
  // ============================================
  
  // Almacena filtros por módulo
  const filters = ref<Record<string, FilterState>>({
    purchases: {},
    billings: {},
    sales: {},
    rents: {},
    clients: {},
    equipments: {},
    spareparts: {}
  })

  // Almacena paginación por módulo
  const pagination = ref<Record<string, PaginationState>>({
    purchases: { page: 1, page_size: 10, total: 0, total_pages: 0 },
    billings: { page: 1, page_size: 10, total: 0, total_pages: 0 },
    sales: { page: 1, page_size: 10, total: 0, total_pages: 0 },
    rents: { page: 1, page_size: 10, total: 0, total_pages: 0 },
    clients: { page: 1, page_size: 10, total: 0, total_pages: 0 },
    equipments: { page: 1, page_size: 10, total: 0, total_pages: 0 },
    spareparts: { page: 1, page_size: 10, total: 0, total_pages: 0 }
  })

  // ============================================
  // GETTERS
  // ============================================
  
  const getFilters = computed(() => (module: string) => {
    return filters.value[module] || {}
  })

  const getPagination = computed(() => (module: string) => {
    return pagination.value[module] || { page: 1, page_size: 10, total: 0, total_pages: 0 }
  })

  // ============================================
  // ACTIONS
  // ============================================
  
  /**
   * Actualiza filtros de un módulo
   */
  function setFilters(module: string, newFilters: FilterState) {
    filters.value[module] = { ...filters.value[module], ...newFilters }
    // Persistir en localStorage
    saveToLocalStorage(module)
  }

  /**
   * Actualiza un filtro específico
   */
  function setFilter(module: string, key: string, value: any) {
    if (!filters.value[module]) {
      filters.value[module] = {}
    }
    filters.value[module][key] = value
    saveToLocalStorage(module)
  }

  /**
   * Limpia filtros de un módulo
   */
  function clearFilters(module: string) {
    filters.value[module] = {}
    pagination.value[module] = { page: 1, page_size: 10, total: 0, total_pages: 0 }
    saveToLocalStorage(module)
  }

  /**
   * Actualiza paginación de un módulo
   */
  function setPagination(module: string, newPagination: Partial<PaginationState>) {
    pagination.value[module] = { ...pagination.value[module], ...newPagination }
    saveToLocalStorage(module)
  }

  /**
   * Actualiza la página actual
   */
  function setPage(module: string, page: number) {
    pagination.value[module].page = page
    saveToLocalStorage(module)
  }

  /**
   * Actualiza el tamaño de página
   */
  function setPageSize(module: string, pageSize: number) {
    pagination.value[module].page_size = pageSize
    pagination.value[module].page = 1 // Resetear a página 1
    saveToLocalStorage(module)
  }

  /**
   * Obtiene configuración completa para una petición
   */
  function getRequestConfig(module: string): FilterState & PaginationParams {
    return {
      ...filters.value[module],
      page: pagination.value[module].page,
      page_size: pagination.value[module].page_size
    }
  }

  /**
   * Guarda en localStorage
   */
  function saveToLocalStorage(module: string) {
    try {
      const state = {
        filters: filters.value[module],
        pagination: {
          page: pagination.value[module].page,
          page_size: pagination.value[module].page_size
        }
      }
      localStorage.setItem(`filters_${module}`, JSON.stringify(state))
    } catch (error) {
      console.error('Error saving filters to localStorage:', error)
    }
  }

  /**
   * Carga desde localStorage
   */
  function loadFromLocalStorage(module: string) {
    try {
      const stored = localStorage.getItem(`filters_${module}`)
      if (stored) {
        const state = JSON.parse(stored)
        filters.value[module] = state.filters || {}
        if (state.pagination) {
          pagination.value[module] = {
            ...pagination.value[module],
            ...state.pagination
          }
        }
      }
    } catch (error) {
      console.error('Error loading filters from localStorage:', error)
    }
  }

  /**
   * Inicializa filtros de todos los módulos desde localStorage
   */
  function initialize() {
    Object.keys(filters.value).forEach(module => {
      loadFromLocalStorage(module)
    })
  }

  // ============================================
  // INITIALIZATION
  // ============================================
  
  initialize()

  return {
    // State
    filters,
    pagination,
    
    // Getters
    getFilters,
    getPagination,
    
    // Actions
    setFilters,
    setFilter,
    clearFilters,
    setPagination,
    setPage,
    setPageSize,
    getRequestConfig,
    loadFromLocalStorage,
    initialize
  }
})
