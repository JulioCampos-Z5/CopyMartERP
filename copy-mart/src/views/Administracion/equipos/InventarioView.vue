<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <h1 class="text-3xl font-bold text-purple-800 mb-2">Gestión de Inventario</h1>
          <p class="text-purple-600">Administra el inventario de equipos y suministros</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total Equipos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Disponibles</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.available }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Renta</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.rented }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Vendidos</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.sold }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <!-- Tabs -->
          <div class="flex border-b border-gray-200 mb-4 overflow-x-auto">
            <button 
              @click="activeTab = 'equipos'" 
              :class="['px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap', activeTab === 'equipos' ? 'border-purple-600 text-purple-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
              Equipos
            </button>
            <button 
              @click="activeTab = 'refacciones'" 
              :class="['px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap', activeTab === 'refacciones' ? 'border-purple-600 text-purple-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
              Refacciones
            </button>
            <button 
              @click="activeTab = 'catalogo'; loadCatalog()" 
              :class="['px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap', activeTab === 'catalogo' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
              Catálogo
            </button>
            <button 
              @click="activeTab = 'stock'; loadStock()" 
              :class="['px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap', activeTab === 'stock' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
              Stock
            </button>
            <button 
              @click="activeTab = 'estantes'; loadShelves()" 
              :class="['px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap', activeTab === 'estantes' ? 'border-amber-600 text-amber-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
              Estantes
            </button>
          </div>
          
          <!-- Equipos Actions -->
          <div v-if="activeTab === 'equipos'" class="flex flex-wrap gap-4">
            <button @click="goToNewEquipment" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Agregar Equipo
            </button>
            <button @click="openBrandModal" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              Registrar Marca
            </button>
            <button @click="loadEquipment" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <select v-model="filterCategory" class="input-field w-40">
              <option value="">Todas las categorías</option>
              <option value="copiadoras">Copiadoras</option>
              <option value="impresoras">Impresoras</option>
              <option value="multifuncionales">Multifuncionales</option>
              <option value="consumibles">Consumibles</option>
            </select>
            <select v-model="filterStatus" class="input-field w-40">
              <option value="">Todos los estados</option>
              <option value="disponible">Disponible</option>
              <option value="rentado">En Renta</option>
              <option value="vendido">Vendido</option>
              <option value="mantenimiento">Mantenimiento</option>
            </select>
          </div>
          
          <!-- Refacciones Actions -->
          <div v-else class="flex flex-wrap gap-4">
            <button @click="goToNewSparepart" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Agregar Refacción
            </button>
            <button @click="loadSpareparts" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <input 
              v-model="sparepartSearch" 
              type="text" 
              placeholder="Buscar por código o nombre..." 
              class="input-field flex-1 max-w-md"
            />
          </div>
        </div>

        <!-- Equipos Table -->
        <div v-if="activeTab === 'equipos'" class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Equipos en Inventario</h2>
          </div>
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <p class="text-gray-500">Cargando equipos...</p>
            </div>
            <div v-else-if="error" class="text-center py-8">
              <p class="text-red-500">{{ error }}</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Marca</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Modelo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serie</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredEquipment.length === 0">
                    <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                      No hay equipos registrados
                    </td>
                  </tr>
                  <tr v-for="item in filteredEquipment" :key="item.item_id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.sku }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ getBrandName(item.brand_id) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.model }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.serie }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.type }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatusClass(item.location_status)]">
                        {{ item.location_status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button @click="goToEquipmentDetail(item.item_id)" class="text-purple-600 hover:text-purple-900 mr-3">Ver</button>
                      <button @click="goToEditEquipment(item.item_id)" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                      <button @click="deleteEquipment(item.item_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Refacciones Table -->
        <div v-if="activeTab === 'refacciones'" class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Refacciones en Inventario</h2>
          </div>
          <div class="p-6">
            <div v-if="loadingSpareparts" class="text-center py-8">
              <p class="text-gray-500">Cargando refacciones...</p>
            </div>
            <div v-else-if="errorSpareparts" class="text-center py-8">
              <p class="text-red-500">{{ errorSpareparts }}</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Marca</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Equipo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Proveedor</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredSpareparts.length === 0">
                    <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                      No hay refacciones registradas
                    </td>
                  </tr>
                  <tr v-for="part in filteredSpareparts" :key="part.sparepart_id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-purple-600">{{ part.code || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ part.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ part.brand || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span v-if="part.color" :class="{
                        'bg-gray-800 text-white': part.color === 'K',
                        'bg-yellow-400 text-gray-900': part.color === 'Y',
                        'bg-pink-500 text-white': part.color === 'M',
                        'bg-cyan-500 text-white': part.color === 'C',
                        'bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-500 text-white': part.color === 'COLOR'
                      }" class="px-2 py-1 text-xs font-medium rounded">
                        {{ part.color }}
                      </span>
                      <span v-else class="text-gray-400">-</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ part.equipment || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ part.supplier || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button @click="goToSparepartDetail(part.sparepart_id)" class="text-purple-600 hover:text-purple-900 mr-3">Ver</button>
                      <button @click="goToEditSparepart(part.sparepart_id)" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                      <button @click="deleteSparepart(part.sparepart_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Catálogo Tab -->
        <div v-if="activeTab === 'catalogo'" class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200 flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-900">Catálogo de Items</h2>
            <button @click="openCatalogModal()" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 flex items-center text-sm">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Item
            </button>
          </div>
          <div class="p-6">
            <div v-if="loadingCatalog" class="text-center py-8">
              <p class="text-gray-500">Cargando catálogo...</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Marca</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Disponible</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Stock Mín/Máx</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="catalogItems.length === 0">
                    <td colspan="7" class="px-6 py-8 text-center text-gray-500">No hay items en el catálogo</td>
                  </tr>
                  <tr v-for="item in catalogItems" :key="item.catalog_id">
                    <td class="px-6 py-4">
                      <div class="font-medium text-gray-900">{{ item.item_name }}</div>
                      <div v-if="item.description" class="text-xs text-gray-500">{{ item.description }}</div>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', item.item_type === 'toner' ? 'bg-cyan-100 text-cyan-800' : 'bg-orange-100 text-orange-800']">
                        {{ item.item_type === 'toner' ? 'Toner' : 'Refacción' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">{{ item.brand?.name || '-' }}</td>
                    <td class="px-6 py-4">
                      <span v-if="item.color" :class="['px-2 py-1 text-xs font-medium rounded', colorClasses[item.color]]">
                        {{ colorLabels[item.color] }}
                      </span>
                      <span v-else class="text-gray-400">-</span>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <span :class="['font-medium', item.available_items < item.stock_min ? 'text-red-600' : 'text-green-600']">
                        {{ item.available_items }} / {{ item.total_items }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-center text-sm text-gray-500">{{ item.stock_min }} / {{ item.stock_max }}</td>
                    <td class="px-6 py-4 text-sm font-medium">
                      <button @click="openCatalogModal(item)" class="text-indigo-600 hover:text-indigo-900 mr-3">Editar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Stock Tab -->
        <div v-if="activeTab === 'stock'" class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200 flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-900">Stock de Inventario</h2>
            <div class="flex gap-2">
              <button @click="openBulkStockModal()" class="bg-emerald-100 text-emerald-700 px-4 py-2 rounded-lg hover:bg-emerald-200 flex items-center text-sm">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Entrada Masiva
              </button>
              <button @click="openStockModal()" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 flex items-center text-sm">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Nueva Entrada
              </button>
            </div>
          </div>
          <div class="p-6">
            <div v-if="loadingStock" class="text-center py-8">
              <p class="text-gray-500">Cargando stock...</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Item</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sección</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estante</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Calidad</th>
                    <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Costo</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="stockItems.length === 0">
                    <td colspan="8" class="px-6 py-8 text-center text-gray-500">No hay items en stock</td>
                  </tr>
                  <tr v-for="item in stockItems" :key="item.inventory_id">
                    <td class="px-4 py-3">
                      <span class="font-mono text-sm font-medium text-emerald-700">{{ item.item_code }}</span>
                    </td>
                    <td class="px-4 py-3">
                      <div class="font-medium text-gray-900 text-sm">{{ item.catalog_item?.item_name || '-' }}</div>
                      <div class="text-xs text-gray-500">{{ item.catalog_item?.item_type === 'toner' ? 'Toner' : 'Refacción' }}</div>
                    </td>
                    <td class="px-4 py-3 text-sm text-gray-500">{{ sectionLabels[item.section] }}</td>
                    <td class="px-4 py-3 text-sm text-gray-500">{{ item.shelf?.name || '-' }}</td>
                    <td class="px-4 py-3">
                      <span :class="['px-2 py-1 text-xs font-medium rounded', qualityClasses[item.quality]]">
                        {{ qualityLabels[item.quality] }}
                      </span>
                    </td>
                    <td class="px-4 py-3 text-center">
                      <span :class="['px-2 py-1 text-xs font-medium rounded-full', item.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                        {{ item.is_available ? 'Disponible' : 'No disponible' }}
                      </span>
                    </td>
                    <td class="px-4 py-3 text-right text-sm">{{ item.cost ? `$${Number(item.cost).toFixed(2)}` : '-' }}</td>
                    <td class="px-4 py-3 text-sm font-medium">
                      <button @click="openStockModal(item)" class="text-emerald-600 hover:text-emerald-900 mr-2">Editar</button>
                      <button @click="toggleStockAvailability(item)" :class="item.is_available ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'">
                        {{ item.is_available ? 'Desactivar' : 'Activar' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Estantes Tab -->
        <div v-if="activeTab === 'estantes'" class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200 flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-900">Estantes por Sección</h2>
            <button @click="openShelfModal()" class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700 flex items-center text-sm">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Estante
            </button>
          </div>
          <div class="p-6">
            <div v-if="loadingShelves" class="text-center py-8">
              <p class="text-gray-500">Cargando estantes...</p>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="shelf in shelves" :key="shelf.shelf_id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ shelf.name }}</h3>
                    <span :class="['px-2 py-1 text-xs font-medium rounded mt-2 inline-block', shelfSectionClasses[shelf.section]]">
                      {{ sectionLabels[shelf.section] }}
                    </span>
                    <p v-if="shelf.description" class="text-sm text-gray-500 mt-2">{{ shelf.description }}</p>
                  </div>
                  <div class="flex gap-2">
                    <button @click="openShelfModal(shelf)" class="text-amber-600 hover:text-amber-900">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="deleteShelf(shelf)" class="text-red-600 hover:text-red-900">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="shelves.length === 0" class="col-span-full text-center py-8 text-gray-500">
                No hay estantes registrados
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ showCreateModal ? 'Agregar Equipo' : 'Editar Equipo' }}</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <form @submit.prevent="showCreateModal ? createEquipment() : updateEquipment()" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label>
              <select v-model="equipmentForm.brand_id" required class="input-field">
                <option :value="null">Seleccionar marca...</option>
                <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                  {{ brand.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modelo *</label>
              <input v-model="equipmentForm.model" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Serie *</label>
              <input v-model="equipmentForm.serie" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modelo de Toner *</label>
              <input v-model="equipmentForm.model_toner" type="text" required class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
              <select v-model="equipmentForm.type" required class="input-field">
                <option value="monocromo">Monocromo</option>
                <option value="color">Color</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor *</label>
              <select v-model="equipmentForm.supplier_id" required class="input-field">
                <option :value="null">Seleccionar proveedor...</option>
                <option v-for="supplier in suppliers" :key="supplier.supplier_id" :value="supplier.supplier_id">
                  {{ supplier.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
              <input v-model="equipmentForm.invoice" type="text" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
              <input v-model="equipmentForm.cost" type="number" step="0.01" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado de Ubicación *</label>
              <select v-model="equipmentForm.location_status" required class="input-field">
                <option value="bodega">Bodega</option>
                <option value="asignado">Asignado</option>
                <option value="vendido">Vendido</option>
                <option value="taller">Taller</option>
                <option value="desconocido">Desconocido</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
              <textarea v-model="equipmentForm.comments" rows="3" class="input-field"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
              {{ showCreateModal ? 'Crear Equipo' : 'Actualizar Equipo' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Brand Modal -->
    <div v-if="showBrandModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">Gestión de Marcas</h3>
            <button @click="closeBrandModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <!-- Lista de Marcas -->
          <div class="mb-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Marcas Registradas</h4>
            <div v-if="loadingBrands" class="text-center py-4">
              <p class="text-gray-500">Cargando marcas...</p>
            </div>
            <div v-else-if="brands.length === 0" class="text-center py-8 bg-gray-50 rounded-lg">
              <p class="text-gray-500">No hay marcas registradas</p>
            </div>
            <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div v-for="brand in brands" :key="brand.brand_id" 
                   class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                <span class="text-sm font-medium text-gray-900">{{ brand.name }}</span>
                <button @click="deleteBrand(brand.brand_id)" 
                        class="text-red-500 hover:text-red-700">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Formulario para Nueva Marca -->
          <div class="border-t pt-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Registrar Nueva Marca</h4>
            <form @submit.prevent="createBrand" class="grid grid-cols-2 gap-3">
              <input v-model="brandForm.name" 
                     type="text" 
                     required 
                     placeholder="Nombre de la marca (Ej: Canon, HP, Xerox...)" 
                     class="input-field">
              <input v-model="brandForm.prefix" 
                     type="text" 
                     required 
                     placeholder="Prefijo (Ej: CAN, HP, XER...)" 
                     class="input-field">
              <button type="submit" 
                      class="col-span-2 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 whitespace-nowrap">\n                Agregar Marca
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Agregar
                </span>
              </button>
            </form>
          </div>
        </div>

        <div class="p-6 border-t flex justify-end">
          <button @click="closeBrandModal" class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cerrar
          </button>
        </div>
      </div>
    </div>

    <!-- Sparepart Modal -->
    <div v-if="showSparepartModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ editingSparepartId ? 'Editar Refacción' : 'Nueva Refacción' }}</h3>
            <button @click="closeSparepartModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <form @submit.prevent="editingSparepartId ? updateSparepart() : createSparepart()" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código</label>
              <input v-model="sparepartForm.code" type="text" class="input-field" placeholder="REF-001">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
              <input v-model="sparepartForm.name" type="text" required class="input-field" placeholder="Toner HP 85A">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Marca</label>
              <input v-model="sparepartForm.brand" type="text" class="input-field" placeholder="HP">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Color</label>
              <select v-model="sparepartForm.color" class="input-field">
                <option value="">Seleccionar...</option>
                <option value="K">Negro (K)</option>
                <option value="C">Cyan (C)</option>
                <option value="M">Magenta (M)</option>
                <option value="Y">Amarillo (Y)</option>
                <option value="COLOR">Color</option>
                <option value="NA">N/A</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Equipo Compatible</label>
              <input v-model="sparepartForm.equipment" type="text" class="input-field" placeholder="LaserJet Pro M404">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
              <input v-model="sparepartForm.supplier" type="text" class="input-field" placeholder="KONICA">
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea v-model="sparepartForm.description" rows="3" class="input-field" placeholder="Descripción de la refacción..."></textarea>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button type="button" @click="closeSparepartModal" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button type="submit" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
              {{ editingSparepartId ? 'Actualizar' : 'Crear' }} Refacción
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Catálogo Modal -->
    <div v-if="showCatalogModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <h3 class="text-xl font-semibold text-gray-900">{{ catalogForm.catalog_id ? 'Editar' : 'Nuevo' }} Item del Catálogo</h3>
        </div>
        <form @submit.prevent="saveCatalogItem" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
            <input v-model="catalogForm.item_name" type="text" required class="input-field" placeholder="Ej: TK-410, CF283A">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
            <select v-model="catalogForm.item_type" required class="input-field">
              <option value="toner">Toner</option>
              <option value="refaccion">Refacción</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Marca</label>
            <select v-model="catalogForm.brand_id" class="input-field">
              <option :value="null">Sin marca</option>
              <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">{{ brand.name }}</option>
            </select>
          </div>
          <div v-if="catalogForm.item_type === 'toner'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Color</label>
            <select v-model="catalogForm.color" class="input-field">
              <option :value="null">N/A</option>
              <option value="k">Negro (K)</option>
              <option value="c">Cyan (C)</option>
              <option value="m">Magenta (M)</option>
              <option value="y">Amarillo (Y)</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
            <textarea v-model="catalogForm.description" rows="2" class="input-field"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Stock Mínimo</label>
              <input v-model.number="catalogForm.stock_min" type="number" min="0" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Stock Máximo</label>
              <input v-model.number="catalogForm.stock_max" type="number" min="0" class="input-field">
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showCatalogModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">Guardar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Stock Modal -->
    <div v-if="showStockModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <h3 class="text-xl font-semibold text-gray-900">{{ stockForm.inventory_id ? 'Editar' : 'Nueva' }} Entrada de Stock</h3>
        </div>
        <form @submit.prevent="saveStockItem" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Item del Catálogo *</label>
            <select v-model="stockForm.catalog_id" required class="input-field">
              <option :value="null" disabled>Seleccionar item...</option>
              <option v-for="cat in catalogItems" :key="cat.catalog_id" :value="cat.catalog_id">{{ cat.item_name }} ({{ cat.item_type }})</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Sección *</label>
              <select v-model="stockForm.section" required class="input-field">
                <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Calidad *</label>
              <select v-model="stockForm.quality" required class="input-field">
                <option v-for="q in qualities" :key="q.value" :value="q.value">{{ q.label }}</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Estante</label>
            <select v-model="stockForm.shelf_id" class="input-field">
              <option :value="null">Sin asignar</option>
              <option v-for="shelf in filteredShelvesForStock" :key="shelf.shelf_id" :value="shelf.shelf_id">{{ shelf.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
            <select v-model="stockForm.supplier_id" class="input-field">
              <option :value="null">Sin proveedor</option>
              <option v-for="sup in suppliers" :key="sup.supplier_id" :value="sup.supplier_id">{{ sup.name }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
              <input v-model="stockForm.invoice" type="text" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
              <input v-model.number="stockForm.cost" type="number" step="0.01" min="0" class="input-field">
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showStockModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">Guardar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Bulk Stock Modal -->
    <div v-if="showBulkStockModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <h3 class="text-xl font-semibold text-gray-900">Entrada Masiva de Stock</h3>
        </div>
        <form @submit.prevent="saveBulkStock" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Item del Catálogo *</label>
            <select v-model="bulkStockForm.catalog_id" required class="input-field">
              <option :value="null" disabled>Seleccionar item...</option>
              <option v-for="cat in catalogItems" :key="cat.catalog_id" :value="cat.catalog_id">{{ cat.item_name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad *</label>
            <input v-model.number="bulkStockForm.quantity" type="number" min="1" required class="input-field">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Sección *</label>
              <select v-model="bulkStockForm.section" required class="input-field">
                <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Calidad *</label>
              <select v-model="bulkStockForm.quality" required class="input-field">
                <option v-for="q in qualities" :key="q.value" :value="q.value">{{ q.label }}</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
            <select v-model="bulkStockForm.supplier_id" class="input-field">
              <option :value="null">Sin proveedor</option>
              <option v-for="sup in suppliers" :key="sup.supplier_id" :value="sup.supplier_id">{{ sup.name }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
              <input v-model="bulkStockForm.invoice" type="text" class="input-field">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo (c/u)</label>
              <input v-model.number="bulkStockForm.cost" type="number" step="0.01" min="0" class="input-field">
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showBulkStockModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">Crear {{ bulkStockForm.quantity }} entrada(s)</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Shelf Modal -->
    <div v-if="showShelfModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6 border-b border-gray-200">
          <h3 class="text-xl font-semibold text-gray-900">{{ shelfForm.shelf_id ? 'Editar' : 'Nuevo' }} Estante</h3>
        </div>
        <form @submit.prevent="saveShelf" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
            <input v-model="shelfForm.name" type="text" required class="input-field" placeholder="Ej: Estante A-1">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sección *</label>
            <select v-model="shelfForm.section" required class="input-field">
              <option v-for="s in sections" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
            <textarea v-model="shelfForm.description" rows="2" class="input-field"></textarea>
          </div>
          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showShelfModal = false" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavigation from '@/components/AppNavigation.vue'
import { equipmentService } from '@/services/equipmentService'
import { sparepartService } from '@/services/sparepartService'
import { catalogService, inventoryService, shelfService } from '@/services/inventoryService'
import { useModalBus } from '@/composables/useModalBus'

export default {
  name: 'InventarioView',
  components: {
    AppNavigation
  },
  data() {
    return {
      activeTab: 'equipos',
      equipment: [],
      brands: [],
      spareparts: [],
      catalogItems: [],
      stockItems: [],
      shelves: [],
      loading: false,
      loadingBrands: false,
      loadingSpareparts: false,
      loadingCatalog: false,
      loadingStock: false,
      loadingShelves: false,
      error: null,
      errorSpareparts: null,
      showCreateModal: false,
      showEditModal: false,
      showBrandModal: false,
      showSparepartModal: false,
      showCatalogModal: false,
      showStockModal: false,
      showBulkStockModal: false,
      showShelfModal: false,
      filterCategory: '',
      filterStatus: '',
      sparepartSearch: '',
      // Lookups para inventory
      sections: [
        { value: 'seccion_1', label: 'Sección 1' },
        { value: 'seccion_2', label: 'Sección 2' },
        { value: 'seccion_3', label: 'Sección 3' },
        { value: 'seccion_4', label: 'Sección 4' },
        { value: 'seccion_5', label: 'Sección 5' },
        { value: 'seccion_6', label: 'Sección 6' }
      ],
      qualities: [
        { value: 'original', label: 'Original' },
        { value: 'generico', label: 'Genérico' },
        { value: 'reparado', label: 'Reparado' },
        { value: 'nueva', label: 'Nueva' },
        { value: 'usado', label: 'Usado' },
        { value: 'n/a', label: 'N/A' }
      ],
      sectionLabels: {
        seccion_1: 'Sección 1', seccion_2: 'Sección 2', seccion_3: 'Sección 3',
        seccion_4: 'Sección 4', seccion_5: 'Sección 5', seccion_6: 'Sección 6'
      },
      qualityLabels: {
        original: 'Original', generico: 'Genérico', reparado: 'Reparado',
        nueva: 'Nueva', usado: 'Usado', 'n/a': 'N/A'
      },
      qualityClasses: {
        original: 'bg-green-100 text-green-800', generico: 'bg-blue-100 text-blue-800',
        reparado: 'bg-yellow-100 text-yellow-800', nueva: 'bg-purple-100 text-purple-800',
        usado: 'bg-gray-100 text-gray-800', 'n/a': 'bg-gray-100 text-gray-500'
      },
      colorLabels: { k: 'Negro', c: 'Cyan', m: 'Magenta', y: 'Amarillo' },
      colorClasses: {
        k: 'bg-gray-800 text-white', c: 'bg-cyan-500 text-white',
        m: 'bg-pink-500 text-white', y: 'bg-yellow-400 text-gray-900'
      },
      shelfSectionClasses: {
        seccion_1: 'bg-red-100 text-red-800', seccion_2: 'bg-orange-100 text-orange-800',
        seccion_3: 'bg-yellow-100 text-yellow-800', seccion_4: 'bg-green-100 text-green-800',
        seccion_5: 'bg-blue-100 text-blue-800', seccion_6: 'bg-purple-100 text-purple-800'
      },
      // Forms
      catalogForm: {
        catalog_id: null, item_name: '', item_type: 'toner', brand_id: null,
        color: null, description: '', stock_min: 0, stock_max: 0
      },
      stockForm: {
        inventory_id: null, catalog_id: null, section: 'seccion_1', shelf_id: null,
        quality: 'original', supplier_id: null, invoice: '', cost: null
      },
      bulkStockForm: {
        catalog_id: null, quantity: 1, section: 'seccion_1', quality: 'original',
        supplier_id: null, invoice: '', cost: null
      },
      shelfForm: { shelf_id: null, name: '', section: 'seccion_1', description: '' },
      equipmentForm: {
        brand_id: null,
        model: '',
        serie: '',
        model_toner: '',
        type: 'monocromo',
        supplier_id: null,
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: ''
      },
      brandForm: {
        name: '',
        prefix: ''
      },
      sparepartForm: {
        code: '',
        name: '',
        description: '',
        color: '',
        brand: '',
        equipment: '',
        supplier: ''
      },
      suppliers: [],
      editingEquipmentId: null,
      editingSparepartId: null
    }
  },
  computed: {
    filteredEquipment() {
      return this.equipment.filter(item => {
        const matchesCategory = !this.filterCategory || item.category === this.filterCategory
        const matchesStatus = !this.filterStatus || item.status === this.filterStatus
        return matchesCategory && matchesStatus
      })
    },
    filteredSpareparts() {
      if (!this.sparepartSearch) return this.spareparts
      const search = this.sparepartSearch.toLowerCase()
      return this.spareparts.filter(part => 
        part.code?.toLowerCase().includes(search) || 
        part.name?.toLowerCase().includes(search)
      )
    },
    filteredShelvesForStock() {
      return this.shelves.filter(s => s.section === this.stockForm.section)
    },
    stats() {
      return {
        total: this.equipment.length,
        available: this.equipment.filter(e => e.location_status === 'bodega').length,
        rented: this.equipment.filter(e => e.location_status === 'asignado').length,
        sold: this.equipment.filter(e => e.location_status === 'vendido').length
      }
    }
  },
  async mounted() {
    await this.loadEquipment()
    await this.loadBrands()
    await this.loadSpareparts()
    await this.loadSuppliers()
  },
  methods: {
    ...(() => {
      const { success, error, info } = useModalBus()
      return { showSuccess: success, showError: error, showInfo: info }
    })(),
    async loadEquipment() {
      this.loading = true
      this.error = null
      try {
        const response = await equipmentService.getEquipment()
        // Si la respuesta es paginada, usar items; si no, usar directamente
        this.equipment = response.items || response || []
      } catch (err) {
        this.error = 'Error al cargar equipos: ' + err.message
        console.error('Error loading equipment:', err)
      } finally {
        this.loading = false
      }
    },
    
    async loadSuppliers() {
      try {
        this.suppliers = await equipmentService.getSuppliers()
      } catch (err) {
        console.error('Error loading suppliers:', err)
      }
    },
    
    async createEquipment() {
      try {
        await equipmentService.createEquipment(this.equipmentForm)
        await this.loadEquipment()
        this.closeModal()
        this.showSuccess('Equipo creado exitosamente')
      } catch (err) {
        this.showError('Error al crear equipo: ' + err.message)
      }
    },
    
    editEquipment(item) {
      this.editingEquipmentId = item.item_id
      this.equipmentForm = { ...item }
      this.showEditModal = true
    },
    
    async updateEquipment() {
      try {
        await equipmentService.updateEquipment(this.editingEquipmentId, this.equipmentForm)
        await this.loadEquipment()
        this.closeModal()
        this.showSuccess('Equipo actualizado exitosamente')
      } catch (err) {
        console.error('Update error:', err)
        this.showError('Error al actualizar equipo: ' + err.message)
      }
    },
    
    async deleteEquipment(equipmentId) {
      if (!confirm('¿Está seguro de eliminar este equipo?')) return
      
      try {
        await equipmentService.deleteEquipment(equipmentId)
        await this.loadEquipment()
        this.showSuccess('Equipo eliminado exitosamente')
      } catch (err) {
        this.showError('Error al eliminar equipo: ' + err.message)
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingEquipmentId = null
      this.equipmentForm = {
        brand_id: null,
        model: '',
        serie: '',
        model_toner: '',
        type: 'monocromo',
        supplier_id: null,
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: ''
      }
    },
    
    getStatusClass(status) {
      const classes = {
        'bodega': 'bg-green-100 text-green-800',
        'asignado': 'bg-blue-100 text-blue-800',
        'vendido': 'bg-gray-100 text-gray-800',
        'taller': 'bg-yellow-100 text-yellow-800',
        'desconocido': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    
    getBrandName(brandId) {
      const brand = this.brands.find(b => b.brand_id === brandId)
      return brand ? brand.name : '-'
    },
    
    async createBrand() {
      try {
        await equipmentService.createBrand(this.brandForm)
        this.brandForm = { name: '', prefix: '' }
        await this.loadBrands()
        this.showSuccess('Marca registrada exitosamente')
      } catch (err) {
        this.showError('Error al registrar marca: ' + err.message)
      }
    },
    
    async loadBrands() {
      this.loadingBrands = true
      try {
        this.brands = await equipmentService.getBrands()
      } catch (err) {
        console.error('Error loading brands:', err)
      } finally {
        this.loadingBrands = false
      }
    },
    
    async deleteBrand(brandId) {
      if (!confirm('¿Está seguro de eliminar esta marca?')) return
      
      try {
        await equipmentService.deleteBrand(brandId)
        await this.loadBrands()
        this.showSuccess('Marca eliminada exitosamente')
      } catch (err) {
        this.showError('Error al eliminar marca: ' + err.message)
      }
    },
    
    async openBrandModal() {
      this.showBrandModal = true
      await this.loadBrands()
    },
    
    closeBrandModal() {
      this.showBrandModal = false
      this.brandForm = { name: '' }
    },

    // Spareparts methods
    async loadSpareparts() {
      this.loadingSpareparts = true
      this.errorSpareparts = null
      try {
        const response = await sparepartService.getSpareparts({ pageSize: 100 })
        this.spareparts = response.items || []
      } catch (err) {
        this.errorSpareparts = 'Error al cargar refacciones: ' + err.message
        console.error('Error loading spareparts:', err)
      } finally {
        this.loadingSpareparts = false
      }
    },

    async createSparepart() {
      try {
        await sparepartService.createSparepart(this.sparepartForm)
        await this.loadSpareparts()
        this.closeSparepartModal()
        this.showSuccess('Refacción creada exitosamente')
      } catch (err) {
        this.showError('Error al crear refacción: ' + err.message)
      }
    },

    editSparepart(sparepart) {
      this.editingSparepartId = sparepart.sparepart_id
      this.sparepartForm = { ...sparepart }
      this.showSparepartModal = true
    },

    async updateSparepart() {
      try {
        await sparepartService.updateSparepart(this.editingSparepartId, this.sparepartForm)
        await this.loadSpareparts()
        this.closeSparepartModal()
        this.showSuccess('Refacción actualizada exitosamente')
      } catch (err) {
        this.showError('Error al actualizar refacción: ' + err.message)
      }
    },

    async deleteSparepart(sparepartId) {
      if (!confirm('¿Está seguro de eliminar esta refacción?')) return
      
      try {
        await sparepartService.deleteSparepart(sparepartId)
        await this.loadSpareparts()
        this.showSuccess('Refacción eliminada exitosamente')
      } catch (err) {
        this.showError('Error al eliminar refacción: ' + err.message)
      }
    },

    closeSparepartModal() {
      this.showSparepartModal = false
      this.editingSparepartId = null
      this.sparepartForm = {
        code: '',
        name: '',
        description: '',
        color: '',
        brand: '',
        equipment: '',
        supplier: ''
      }
    },
    
    showError(message) {
      this.error = message
      setTimeout(() => {
        this.error = null
      }, 5000)
    },
    
    success(message) {
      // Aquí puedes agregar una notificación toast si lo deseas
    },

    // Métodos de navegación para Equipos
    goToNewEquipment() {
      this.$router.push('/administracion/equipos/nuevo')
    },

    goToEquipmentDetail(itemId) {
      this.$router.push(`/administracion/equipos/${itemId}`)
    },

    goToEditEquipment(itemId) {
      this.$router.push(`/administracion/equipos/editar/${itemId}`)
    },

    // Métodos de navegación para Refacciones
    goToNewSparepart() {
      this.$router.push('/administracion/refacciones/nueva')
    },

    goToSparepartDetail(sparepartId) {
      this.$router.push(`/administracion/refacciones/${sparepartId}`)
    },

    goToEditSparepart(sparepartId) {
      this.$router.push(`/administracion/refacciones/editar/${sparepartId}`)
    },

    // ========== CATÁLOGO ==========
    async loadCatalog() {
      this.loadingCatalog = true
      try {
        this.catalogItems = await catalogService.getCatalogItems({ is_active: true })
      } catch (err) {
        console.error('Error cargando catálogo:', err)
      } finally {
        this.loadingCatalog = false
      }
    },
    openCatalogModal(item = null) {
      if (item) {
        this.catalogForm = {
          catalog_id: item.catalog_id, item_name: item.item_name, item_type: item.item_type,
          brand_id: item.brand_id || null, color: item.color || null,
          description: item.description || '', stock_min: item.stock_min, stock_max: item.stock_max
        }
      } else {
        this.catalogForm = {
          catalog_id: null, item_name: '', item_type: 'toner', brand_id: null,
          color: null, description: '', stock_min: 0, stock_max: 0
        }
      }
      this.showCatalogModal = true
    },
    async saveCatalogItem() {
      try {
        const data = {
          item_name: this.catalogForm.item_name, item_type: this.catalogForm.item_type,
          brand_id: this.catalogForm.brand_id || undefined,
          color: this.catalogForm.item_type === 'toner' ? this.catalogForm.color || undefined : undefined,
          description: this.catalogForm.description || undefined,
          stock_min: this.catalogForm.stock_min, stock_max: this.catalogForm.stock_max
        }
        if (this.catalogForm.catalog_id) {
          await catalogService.updateCatalogItem(this.catalogForm.catalog_id, data)
          await catalogService.updateStockLevels(this.catalogForm.catalog_id, {
            stock_min: this.catalogForm.stock_min, stock_max: this.catalogForm.stock_max
          })
        } else {
          await catalogService.createCatalogItem(data)
        }
        this.showCatalogModal = false
        await this.loadCatalog()
      } catch (err) {
        console.error('Error guardando item del catálogo:', err)
        alert(err.message || 'Error al guardar')
      }
    },

    // ========== STOCK ==========
    async loadStock() {
      this.loadingStock = true
      try {
        this.stockItems = await inventoryService.getInventoryItems({ is_active: true })
        if (this.catalogItems.length === 0) await this.loadCatalog()
        if (this.shelves.length === 0) await this.loadShelves()
      } catch (err) {
        console.error('Error cargando stock:', err)
      } finally {
        this.loadingStock = false
      }
    },
    openStockModal(item = null) {
      if (item) {
        this.stockForm = {
          inventory_id: item.inventory_id, catalog_id: item.catalog_id, section: item.section,
          shelf_id: item.shelf_id || null, quality: item.quality,
          supplier_id: item.supplier_id || null, invoice: item.invoice || '', cost: item.cost ? Number(item.cost) : null
        }
      } else {
        this.stockForm = {
          inventory_id: null, catalog_id: null, section: 'seccion_1', shelf_id: null,
          quality: 'original', supplier_id: null, invoice: '', cost: null
        }
      }
      this.showStockModal = true
    },
    openBulkStockModal() {
      this.bulkStockForm = {
        catalog_id: null, quantity: 1, section: 'seccion_1', quality: 'original',
        supplier_id: null, invoice: '', cost: null
      }
      this.showBulkStockModal = true
    },
    async saveStockItem() {
      if (!this.stockForm.catalog_id) return
      try {
        const data = {
          catalog_id: this.stockForm.catalog_id, section: this.stockForm.section,
          shelf_id: this.stockForm.shelf_id || undefined, quality: this.stockForm.quality,
          supplier_id: this.stockForm.supplier_id || undefined,
          invoice: this.stockForm.invoice || undefined, cost: this.stockForm.cost || undefined
        }
        if (this.stockForm.inventory_id) {
          await inventoryService.updateInventoryItem(this.stockForm.inventory_id, data)
        } else {
          await inventoryService.createInventoryItem(data)
        }
        this.showStockModal = false
        await this.loadStock()
      } catch (err) {
        console.error('Error guardando stock:', err)
        alert(err.message || 'Error al guardar')
      }
    },
    async saveBulkStock() {
      if (!this.bulkStockForm.catalog_id) return
      try {
        await inventoryService.createBulkInventory({
          catalog_id: this.bulkStockForm.catalog_id, quantity: this.bulkStockForm.quantity,
          section: this.bulkStockForm.section, quality: this.bulkStockForm.quality,
          supplier_id: this.bulkStockForm.supplier_id || undefined,
          invoice: this.bulkStockForm.invoice || undefined, cost: this.bulkStockForm.cost || undefined
        })
        this.showBulkStockModal = false
        await this.loadStock()
      } catch (err) {
        console.error('Error en entrada masiva:', err)
        alert(err.message || 'Error al crear entradas')
      }
    },
    async toggleStockAvailability(item) {
      try {
        await inventoryService.updateInventoryItem(item.inventory_id, { is_available: !item.is_available })
        await this.loadStock()
      } catch (err) {
        console.error('Error actualizando disponibilidad:', err)
      }
    },

    // ========== ESTANTES ==========
    async loadShelves() {
      this.loadingShelves = true
      try {
        this.shelves = await shelfService.getShelves()
      } catch (err) {
        console.error('Error cargando estantes:', err)
      } finally {
        this.loadingShelves = false
      }
    },
    openShelfModal(shelf = null) {
      if (shelf) {
        this.shelfForm = {
          shelf_id: shelf.shelf_id, name: shelf.name,
          section: shelf.section, description: shelf.description || ''
        }
      } else {
        this.shelfForm = { shelf_id: null, name: '', section: 'seccion_1', description: '' }
      }
      this.showShelfModal = true
    },
    async saveShelf() {
      try {
        const data = {
          name: this.shelfForm.name, section: this.shelfForm.section,
          description: this.shelfForm.description || undefined
        }
        if (this.shelfForm.shelf_id) {
          await shelfService.updateShelf(this.shelfForm.shelf_id, data)
        } else {
          await shelfService.createShelf(data)
        }
        this.showShelfModal = false
        await this.loadShelves()
      } catch (err) {
        console.error('Error guardando estante:', err)
        alert(err.message || 'Error al guardar')
      }
    },
    async deleteShelf(shelf) {
      if (!confirm(`¿Eliminar el estante "${shelf.name}"?`)) return
      try {
        await shelfService.deleteShelf(shelf.shelf_id)
        await this.loadShelves()
      } catch (err) {
        console.error('Error eliminando estante:', err)
        alert(err.message || 'Error al eliminar')
      }
    }
  }
}
</script>
