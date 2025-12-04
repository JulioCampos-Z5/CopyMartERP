<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
      <!-- Header -->
      <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-purple-800 mb-2">Control de Almacén - Equipos</h1>
            <p class="text-purple-600">Gestiona el inventario de equipos (impresoras, copiadoras, multifuncionales)</p>
          </div>
          <div class="flex gap-2">
            <button @click="showBrandModal = true" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              Marcas
            </button>
            <button @click="showSupplierModal = true" class="btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Proveedores
            </button>
            <button @click="showCreateModal = true" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Equipo
            </button>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-xs font-medium text-gray-500">Total Equipos</h3>
              <p class="text-xl font-semibold text-gray-900">{{ stats.total }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-xs font-medium text-gray-500">En Bodega</h3>
              <p class="text-xl font-semibold text-blue-600">{{ stats.bodega }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-xs font-medium text-gray-500">Asignados</h3>
              <p class="text-xl font-semibold text-green-600">{{ stats.asignado }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-xs font-medium text-gray-500">En Taller</h3>
              <p class="text-xl font-semibold text-yellow-600">{{ stats.taller }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-4 rounded-lg shadow border">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-xs font-medium text-gray-500">Vendidos</h3>
              <p class="text-xl font-semibold text-emerald-600">{{ stats.vendido }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="bg-white p-4 rounded-lg shadow border">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Modelo, serie, SKU..."
              class="input-field"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Marca</label>
            <select v-model="selectedBrand" class="input-field">
              <option value="">Todas las marcas</option>
              <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                {{ brand.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ubicación</label>
            <select v-model="selectedStatus" class="input-field">
              <option value="">Todas</option>
              <option value="bodega">En Bodega</option>
              <option value="asignado">Asignado</option>
              <option value="taller">En Taller</option>
              <option value="vendido">Vendido</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
            <select v-model="selectedType" class="input-field">
              <option value="">Todos</option>
              <option value="monocromo">Monocromo</option>
              <option value="color">Color</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tabla de Equipos -->
      <div class="bg-white rounded-lg shadow border overflow-hidden">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-lg font-semibold text-gray-900">Inventario de Equipos</h2>
          <span class="text-sm text-gray-500">{{ filteredEquipment.length }} equipos encontrados</span>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Equipo</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serie</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tóner</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ubicación</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Costo</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoading">
                <td colspan="8" class="px-4 py-8 text-center">
                  <div class="flex items-center justify-center">
                    <svg class="animate-spin h-6 w-6 text-purple-600 mr-3" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Cargando equipos...
                  </div>
                </td>
              </tr>
              <tr v-else-if="filteredEquipment.length === 0">
                <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                  No se encontraron equipos
                </td>
              </tr>
              <tr v-for="equip in filteredEquipment" :key="equip.item_id" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap">
                  <span class="text-xs font-mono bg-gray-100 px-2 py-1 rounded">{{ equip.sku }}</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-8 w-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                      <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ equip.model }}</p>
                      <p class="text-xs text-gray-500">{{ getBrandName(equip.brand_id) }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900 font-mono">
                  {{ equip.serie }}
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    equip.type === 'color' ? 'bg-pink-100 text-pink-800' : 'bg-gray-100 text-gray-800'
                  ]">
                    {{ equip.type === 'color' ? 'Color' : 'Mono' }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                  {{ equip.model_toner }}
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="getStatusClass(equip.location_status)">
                    {{ getStatusLabel(equip.location_status) }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                  {{ equip.cost ? '$' + Number(equip.cost).toLocaleString() : '-' }}
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm">
                  <div class="flex space-x-1">
                    <button @click="editEquipment(equip)" class="p-1 text-blue-600 hover:bg-blue-50 rounded" title="Editar">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="changeStatus(equip)" class="p-1 text-yellow-600 hover:bg-yellow-50 rounded" title="Cambiar ubicación">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                      </svg>
                    </button>
                    <button @click="viewDetails(equip)" class="p-1 text-gray-600 hover:bg-gray-50 rounded" title="Ver detalles">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    </div>

    <!-- Modal Crear/Editar Equipo -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ showEditModal ? 'Editar Equipo' : 'Registrar Nuevo Equipo' }}
          </h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="saveEquipment">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label>
              <select v-model="equipmentForm.brand_id" required class="input-field">
                <option value="">Seleccionar</option>
                <option v-for="brand in brands" :key="brand.brand_id" :value="brand.brand_id">
                  {{ brand.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modelo *</label>
              <input v-model="equipmentForm.model" type="text" required class="input-field" placeholder="Ej: LaserJet Pro M404">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Serie *</label>
              <input v-model="equipmentForm.serie" type="text" required class="input-field" placeholder="Ej: VNC3X12345">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Modelo de Tóner *</label>
              <input v-model="equipmentForm.model_toner" type="text" required class="input-field" placeholder="Ej: CF258A">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
              <select v-model="equipmentForm.type" required class="input-field">
                <option value="">Seleccionar</option>
                <option value="monocromo">Monocromo</option>
                <option value="color">Color</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor *</label>
              <select v-model="equipmentForm.supplier_id" required class="input-field">
                <option value="">Seleccionar</option>
                <option v-for="supplier in suppliers" :key="supplier.supplier_id" :value="supplier.supplier_id">
                  {{ supplier.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Factura</label>
              <input v-model="equipmentForm.invoice" type="text" class="input-field" placeholder="Número de factura">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Costo</label>
              <input v-model="equipmentForm.cost" type="number" step="0.01" class="input-field" placeholder="0.00">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ubicación *</label>
              <select v-model="equipmentForm.location_status" required class="input-field">
                <option value="bodega">En Bodega</option>
                <option value="asignado">Asignado</option>
                <option value="taller">En Taller</option>
                <option value="vendido">Vendido</option>
                <option value="desconocido">Desconocido</option>
              </select>
            </div>
            <div>
              <label class="flex items-center mt-6">
                <input type="checkbox" v-model="equipmentForm.is_active" class="h-4 w-4 text-purple-600 rounded">
                <span class="ml-2 text-sm text-gray-700">Equipo activo</span>
              </label>
            </div>
          </div>
          
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios</label>
            <textarea v-model="equipmentForm.comments" rows="2" class="input-field" placeholder="Notas adicionales..."></textarea>
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="closeModal" class="btn-secondary">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSaving">
              {{ isSaving ? 'Guardando...' : (showEditModal ? 'Actualizar' : 'Registrar') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Cambiar Estado -->
    <div v-if="showStatusModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Cambiar Ubicación del Equipo</h3>
        <p class="text-sm text-gray-600 mb-4">{{ selectedEquipment?.model }} - {{ selectedEquipment?.serie }}</p>
        
        <div class="space-y-2">
          <button 
            v-for="status in ['bodega', 'asignado', 'taller', 'vendido']" 
            :key="status"
            @click="updateStatus(status)"
            :class="[
              'w-full text-left px-4 py-3 rounded-lg border transition-colors',
              selectedEquipment?.location_status === status 
                ? 'bg-purple-50 border-purple-300' 
                : 'hover:bg-gray-50 border-gray-200'
            ]"
          >
            <span :class="getStatusClass(status)">{{ getStatusLabel(status) }}</span>
          </button>
        </div>
        
        <div class="flex justify-end mt-6">
          <button @click="showStatusModal = false" class="btn-secondary">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Modal Registrar Marca -->
    <div v-if="showBrandModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Registrar Nueva Marca</h3>
          <button @click="closeBrandModal" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="saveBrand">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de la Marca *</label>
              <input 
                v-model="brandForm.name" 
                type="text" 
                required 
                class="input-field" 
                placeholder="Ej: HP, Canon, Xerox, Ricoh..."
              >
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Prefijo (para SKU) *</label>
              <input 
                v-model="brandForm.prefix" 
                type="text" 
                required 
                maxlength="5"
                class="input-field uppercase"
                placeholder="Ej: HP, CAN, XER, RIC..."
                @input="brandForm.prefix = brandForm.prefix.toUpperCase()"
              >
              <p class="text-xs text-gray-500 mt-1">Se usa para generar el SKU del equipo (máx. 5 caracteres)</p>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="closeBrandModal" class="btn-secondary">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSavingBrand">
              {{ isSavingBrand ? 'Guardando...' : 'Registrar Marca' }}
            </button>
          </div>
        </form>

        <!-- Lista de marcas existentes -->
        <div class="mt-6 pt-4 border-t border-gray-200">
          <h4 class="text-sm font-medium text-gray-700 mb-2">Marcas Registradas ({{ brands.length }})</h4>
          <div class="max-h-40 overflow-y-auto">
            <div v-if="brands.length === 0" class="text-sm text-gray-500">No hay marcas registradas</div>
            <div v-else class="space-y-1">
              <div v-for="brand in brands" :key="brand.brand_id" class="flex items-center justify-between py-1 px-2 bg-gray-50 rounded text-sm">
                <span>{{ brand.name }}</span>
                <span class="text-xs text-gray-400">{{ brand.prefix }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Registrar Proveedor -->
    <div v-if="showSupplierModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Registrar Nuevo Proveedor</h3>
          <button @click="closeSupplierModal" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="saveSupplier">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Proveedor *</label>
              <input 
                v-model="supplierForm.name" 
                type="text" 
                required 
                class="input-field" 
                placeholder="Ej: Distribuidora XYZ, Tecnología ABC..."
              >
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="closeSupplierModal" class="btn-secondary">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSavingSupplier">
              {{ isSavingSupplier ? 'Guardando...' : 'Registrar Proveedor' }}
            </button>
          </div>
        </form>

        <!-- Lista de proveedores existentes -->
        <div class="mt-6 pt-4 border-t border-gray-200">
          <h4 class="text-sm font-medium text-gray-700 mb-2">Proveedores Registrados ({{ suppliers.length }})</h4>
          <div class="max-h-40 overflow-y-auto">
            <div v-if="suppliers.length === 0" class="text-sm text-gray-500">No hay proveedores registrados</div>
            <div v-else class="space-y-1">
              <div v-for="supplier in suppliers" :key="supplier.supplier_id" class="flex items-center justify-between py-1 px-2 bg-gray-50 rounded text-sm">
                <span>{{ supplier.name }}</span>
                <span class="text-xs text-gray-400">#{{ supplier.supplier_id }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Detalles -->
    <div v-if="showDetailsModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-full max-w-lg shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Detalles del Equipo</h3>
          <button @click="showDetailsModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div v-if="selectedEquipment" class="space-y-3">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-xs text-gray-500">SKU</p>
              <p class="font-mono font-medium">{{ selectedEquipment.sku }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Serie</p>
              <p class="font-mono font-medium">{{ selectedEquipment.serie }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Marca</p>
              <p class="font-medium">{{ getBrandName(selectedEquipment.brand_id) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Modelo</p>
              <p class="font-medium">{{ selectedEquipment.model }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Tipo</p>
              <p class="font-medium">{{ selectedEquipment.type === 'color' ? 'Color' : 'Monocromo' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Modelo Tóner</p>
              <p class="font-medium">{{ selectedEquipment.model_toner }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Proveedor</p>
              <p class="font-medium">{{ getSupplierName(selectedEquipment.supplier_id) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Factura</p>
              <p class="font-medium">{{ selectedEquipment.invoice || '-' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Costo</p>
              <p class="font-medium">{{ selectedEquipment.cost ? '$' + Number(selectedEquipment.cost).toLocaleString() : '-' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Ubicación</p>
              <span :class="getStatusClass(selectedEquipment.location_status)">
                {{ getStatusLabel(selectedEquipment.location_status) }}
              </span>
            </div>
          </div>
          <div v-if="selectedEquipment.comments">
            <p class="text-xs text-gray-500">Comentarios</p>
            <p class="text-sm text-gray-700">{{ selectedEquipment.comments }}</p>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/BaseLayout.vue'
import { equipmentService } from '@/services/equipmentService'

export default {
  name: 'AlmacenView',
  components: {
    BaseLayout
  },
  data() {
    return {
      equipment: [],
      brands: [],
      suppliers: [],
      isLoading: false,
      isSaving: false,
      searchQuery: '',
      selectedBrand: '',
      selectedStatus: '',
      selectedType: '',
      showCreateModal: false,
      showEditModal: false,
      showStatusModal: false,
      showDetailsModal: false,
      showBrandModal: false,
      showSupplierModal: false,
      isSavingBrand: false,
      isSavingSupplier: false,
      selectedEquipment: null,
      brandForm: {
        name: '',
        prefix: ''
      },
      supplierForm: {
        name: ''
      },
      equipmentForm: {
        brand_id: '',
        model: '',
        serie: '',
        model_toner: '',
        type: '',
        supplier_id: '',
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: '',
        is_active: true
      }
    }
  },
  computed: {
    stats() {
      return {
        total: this.equipment.length,
        bodega: this.equipment.filter(e => e.location_status === 'bodega').length,
        asignado: this.equipment.filter(e => e.location_status === 'asignado').length,
        taller: this.equipment.filter(e => e.location_status === 'taller').length,
        vendido: this.equipment.filter(e => e.location_status === 'vendido').length
      }
    },
    filteredEquipment() {
      return this.equipment.filter(e => {
        const matchSearch = !this.searchQuery || 
          e.model?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          e.serie?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          e.sku?.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchBrand = !this.selectedBrand || e.brand_id == this.selectedBrand
        const matchStatus = !this.selectedStatus || e.location_status === this.selectedStatus
        const matchType = !this.selectedType || e.type === this.selectedType
        
        return matchSearch && matchBrand && matchStatus && matchType
      })
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.isLoading = true
      try {
        const [equipmentData, brandsData, suppliersData] = await Promise.all([
          equipmentService.getEquipment(),
          equipmentService.getBrands(),
          equipmentService.getSuppliers()
        ])
        this.equipment = equipmentData || []
        this.brands = brandsData || []
        this.suppliers = suppliersData || []
      } catch (error) {
        console.error('Error cargando datos:', error)
        this.showNotification('Error al cargar los equipos', 'error')
      } finally {
        this.isLoading = false
      }
    },

    getBrandName(brandId) {
      const brand = this.brands.find(b => b.brand_id === brandId)
      return brand ? brand.name : '-'
    },

    getSupplierName(supplierId) {
      const supplier = this.suppliers.find(s => s.supplier_id === supplierId)
      return supplier ? supplier.name : '-'
    },

    getStatusLabel(status) {
      const labels = {
        'bodega': 'En Bodega',
        'asignado': 'Asignado',
        'vendido': 'Vendido',
        'taller': 'En Taller',
        'desconocido': 'Desconocido'
      }
      return labels[status] || status
    },

    getStatusClass(status) {
      const classes = {
        'bodega': 'px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full',
        'asignado': 'px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full',
        'vendido': 'px-2 py-1 text-xs font-medium bg-emerald-100 text-emerald-800 rounded-full',
        'taller': 'px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full',
        'desconocido': 'px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full'
      }
      return classes[status] || classes['desconocido']
    },

    editEquipment(equip) {
      this.selectedEquipment = equip
      this.equipmentForm = {
        brand_id: equip.brand_id,
        model: equip.model,
        serie: equip.serie,
        model_toner: equip.model_toner,
        type: equip.type,
        supplier_id: equip.supplier_id,
        invoice: equip.invoice || '',
        cost: equip.cost,
        location_status: equip.location_status,
        comments: equip.comments || '',
        is_active: equip.is_active
      }
      this.showEditModal = true
    },

    changeStatus(equip) {
      this.selectedEquipment = equip
      this.showStatusModal = true
    },

    viewDetails(equip) {
      this.selectedEquipment = equip
      this.showDetailsModal = true
    },

    async updateStatus(newStatus) {
      try {
        await equipmentService.updateEquipmentStatus(this.selectedEquipment.item_id, newStatus)
        await this.loadData()
        this.showStatusModal = false
        this.showNotification('Ubicación actualizada', 'success')
      } catch (error) {
        console.error('Error actualizando estado:', error)
        this.showNotification('Error al actualizar ubicación', 'error')
      }
    },

    async saveEquipment() {
      this.isSaving = true
      try {
        const data = {
          brand_id: parseInt(this.equipmentForm.brand_id),
          model: this.equipmentForm.model,
          serie: this.equipmentForm.serie,
          model_toner: this.equipmentForm.model_toner,
          type: this.equipmentForm.type,
          supplier_id: parseInt(this.equipmentForm.supplier_id),
          invoice: this.equipmentForm.invoice || null,
          cost: this.equipmentForm.cost ? parseFloat(this.equipmentForm.cost) : null,
          location_status: this.equipmentForm.location_status,
          comments: this.equipmentForm.comments || null,
          is_active: this.equipmentForm.is_active
        }

        if (this.showEditModal) {
          await equipmentService.updateEquipment(this.selectedEquipment.item_id, data)
          this.showNotification('Equipo actualizado', 'success')
        } else {
          await equipmentService.createEquipment(data)
          this.showNotification('Equipo registrado', 'success')
        }
        
        await this.loadData()
        this.closeModal()
      } catch (error) {
        console.error('Error guardando equipo:', error)
        this.showNotification('Error: ' + error.message, 'error')
      } finally {
        this.isSaving = false
      }
    },

    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.selectedEquipment = null
      this.equipmentForm = {
        brand_id: '',
        model: '',
        serie: '',
        model_toner: '',
        type: '',
        supplier_id: '',
        invoice: '',
        cost: null,
        location_status: 'bodega',
        comments: '',
        is_active: true
      }
    },

    showNotification(message, type) {
      if (type === 'error') {
        alert('❌ ' + message)
      } else {
        alert('✅ ' + message)
      }
    },

    async saveBrand() {
      if (!this.brandForm.name.trim() || !this.brandForm.prefix.trim()) {
        this.showNotification('El nombre y el prefijo son requeridos', 'error')
        return
      }

      this.isSavingBrand = true
      try {
        await equipmentService.createBrand({
          name: this.brandForm.name.trim(),
          prefix: this.brandForm.prefix.trim().toUpperCase()
        })
        await this.loadData()
        this.closeBrandModal()
        this.showNotification('Marca registrada exitosamente', 'success')
      } catch (error) {
        console.error('Error registrando marca:', error)
        this.showNotification('Error al registrar la marca: ' + error.message, 'error')
      } finally {
        this.isSavingBrand = false
      }
    },

    closeBrandModal() {
      this.showBrandModal = false
      this.brandForm = {
        name: '',
        prefix: ''
      }
    },

    async saveSupplier() {
      if (!this.supplierForm.name.trim()) {
        this.showNotification('El nombre del proveedor es requerido', 'error')
        return
      }

      this.isSavingSupplier = true
      try {
        await equipmentService.createSupplier({
          name: this.supplierForm.name.trim()
        })
        await this.loadData()
        this.closeSupplierModal()
        this.showNotification('Proveedor registrado exitosamente', 'success')
      } catch (error) {
        console.error('Error registrando proveedor:', error)
        this.showNotification('Error al registrar el proveedor: ' + error.message, 'error')
      } finally {
        this.isSavingSupplier = false
      }
    },

    closeSupplierModal() {
      this.showSupplierModal = false
      this.supplierForm = {
        name: ''
      }
    }
  }
}
</script>