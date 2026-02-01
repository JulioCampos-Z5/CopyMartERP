<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200 mb-6">
        <h1 class="text-3xl font-bold text-green-800 mb-2">Gestión de Compras</h1>
        <p class="text-green-600">Administra las órdenes de compra de refacciones y equipos</p>
      </div>

      <BaseTable
        :columns="columns"
        :data="purchases"
        :loading="loading"
        :error="error"
        :pagination="pagination"
        :searchable="true"
        search-placeholder="Buscar por nombre, código de envío..."
        empty-text="No hay compras registradas"
        @search="handleSearch"
        @page-change="handlePageChange"
      >
        <!-- Filtros -->
        <template #filters>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="filters.status" @change="filtersStore.setFilter('purchases', 'status', filters.status); loadPurchases()" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                <option value="">Todos</option>
                <option value="En Curso">En Curso</option>
                <option value="En Tránsito">En Tránsito</option>
                <option value="Solicitud Guía Almacén">Solicitud Guía</option>
                <option value="Falta Pago Proveedor">Falta Pago</option>
                <option value="Falta Factura">Falta Factura</option>
                <option value="Por Revisar">Por Revisar</option>
                <option value="Pausado Back Orders">Pausado</option>
                <option value="Concluido">Concluido</option>
                <option value="Rechazado">Rechazado</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="filters.type" @change="filtersStore.setFilter('purchases', 'type', filters.type); loadPurchases()" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                <option value="">Todos</option>
                <option value="Interna">Interna</option>
                <option value="Venta">Venta</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Desde</label>
              <input v-model="filters.startDate" @change="filtersStore.setFilter('purchases', 'startDate', filters.startDate); loadPurchases()" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Hasta</label>
              <input v-model="filters.endDate" @change="filtersStore.setFilter('purchases', 'endDate', filters.endDate); loadPurchases()" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
            </div>
          </div>
        </template>

        <!-- Estadísticas -->
        <template #stats>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">Total Compras</div>
            <div class="text-2xl font-bold text-gray-900">{{ stats.total || 0 }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">En Curso</div>
            <div class="text-2xl font-bold text-yellow-600">{{ stats.inProgress || 0 }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">En Tránsito</div>
            <div class="text-2xl font-bold text-blue-600">{{ stats.inTransit || 0 }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg shadow border">
            <div class="text-sm text-gray-500 mb-1">Concluidas</div>
            <div class="text-2xl font-bold text-green-600">{{ stats.completed || 0 }}</div>
          </div>
        </template>

        <!-- Acciones principales -->
        <template #actions>
          <button @click="goToCreate" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Nueva Compra
          </button>
          <button @click="openSupplierModal" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Gestionar Proveedores
          </button>
          <button @click="loadPurchases" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar
          </button>
        </template>

        <!-- Celda de estado personalizada -->
        <template #cell-status="{ value }">
          <span :class="getStatusBadgeClass(value)">
            {{ value }}
          </span>
        </template>

        <!-- Celda de tipo personalizada -->
        <template #cell-type="{ value }">
          <span :class="value === 'Interna' ? 'px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full' : 'px-2 py-1 bg-purple-100 text-purple-800 text-xs font-semibold rounded-full'">
            {{ value }}
          </span>
        </template>

        <!-- Acciones por fila -->
        <template #row-actions="{ row }">
          <div class="flex gap-2 justify-end">
            <button @click="viewDetails(row)" class="text-blue-600 hover:text-blue-800" title="Ver detalles">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
            <button v-if="canEdit(row)" @click="editPurchase(row)" class="text-green-600 hover:text-green-800" title="Editar">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button v-if="canChangeStatus(row)" @click="updateStatus(row)" class="text-indigo-600 hover:text-indigo-800" title="Cambiar estado">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
        </template>
      </BaseTable>

      <!-- Modal crear/editar compra -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg max-w-4xl w-full p-6 max-h-[90vh] overflow-y-auto">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">{{ editingPurchase ? 'Editar' : 'Nueva' }} Compra</h2>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="savePurchase" class="space-y-6">
            <!-- Información básica -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Información Básica</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de la compra *</label>
                  <input v-model="purchaseForm.name" type="text" required 
                         placeholder="Ej: Tóner HP 58A, Kit de mantenimiento..."
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Refacción *</label>
                  <select v-model="purchaseForm.sparepart_id" required 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <option value="">Seleccionar refacción...</option>
                    <option v-for="sp in spareparts" :key="sp.sparepart_id" :value="sp.sparepart_id">
                      {{ sp.name }} - {{ sp.brand || 'Sin marca' }}
                    </option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Cantidad *</label>
                  <input v-model.number="purchaseForm.amount" type="number" min="1" required 
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
                  <select v-model="purchaseForm.type" required 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <option value="Interna">Interna (uso interno)</option>
                    <option value="Venta">Venta (para cliente)</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Calidad</label>
                  <select v-model="purchaseForm.quality" 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <option value="">Sin especificar</option>
                    <option value="Original">Original</option>
                    <option value="Compatible">Compatible</option>
                    <option value="Remanufacturado">Remanufacturado</option>
                  </select>
                </div>
              </div>
            </div>
            
            <!-- Proveedores y cotizaciones -->
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Proveedores y Cotizaciones</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">Proveedor 1</label>
                  <select v-model="purchaseForm.supplier1_name" 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Seleccionar...</option>
                    <option v-for="s in suppliers" :key="s.supplier_id" :value="s.name">{{ s.name }}</option>
                  </select>
                  <input v-model.number="purchaseForm.supplier1_cost" type="number" step="0.01" min="0" 
                         placeholder="Costo $" 
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                </div>
                
                <div class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">Proveedor 2</label>
                  <select v-model="purchaseForm.supplier2_name" 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Seleccionar...</option>
                    <option v-for="s in suppliers" :key="s.supplier_id" :value="s.name">{{ s.name }}</option>
                  </select>
                  <input v-model.number="purchaseForm.supplier2_cost" type="number" step="0.01" min="0" 
                         placeholder="Costo $" 
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                </div>
                
                <div class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">Proveedor 3</label>
                  <select v-model="purchaseForm.supplier3_name" 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Seleccionar...</option>
                    <option v-for="s in suppliers" :key="s.supplier_id" :value="s.name">{{ s.name }}</option>
                  </select>
                  <input v-model.number="purchaseForm.supplier3_cost" type="number" step="0.01" min="0" 
                         placeholder="Costo $" 
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                </div>
              </div>
            </div>
            
            <!-- Información de envío -->
            <div class="bg-purple-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Información de Envío</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Método de envío</label>
                  <select v-model="purchaseForm.shipping_method" 
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                    <option value="">Sin especificar</option>
                    <option value="Paquetería">Paquetería</option>
                    <option value="Estafeta">Estafeta</option>
                    <option value="DHL">DHL</option>
                    <option value="FedEx">FedEx</option>
                    <option value="Redpack">Redpack</option>
                    <option value="Entrega directa">Entrega directa</option>
                    <option value="Recolección">Recolección en tienda</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Código de rastreo</label>
                  <input v-model="purchaseForm.shipping_code" type="text" 
                         placeholder="Número de guía..."
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Costo de envío</label>
                  <input v-model.number="purchaseForm.shipping_cost" type="number" step="0.01" min="0" 
                         placeholder="$0.00"
                         class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" />
                </div>
              </div>
            </div>
            
            <!-- Justificación y comentarios -->
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Justificación</label>
                <textarea v-model="purchaseForm.justification" rows="2" 
                          placeholder="Razón de la compra..."
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"></textarea>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Comentarios adicionales</label>
                <textarea v-model="purchaseForm.comments" rows="2" 
                          placeholder="Notas adicionales..."
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"></textarea>
              </div>
            </div>
            
            <!-- Acciones -->
            <div class="flex justify-end gap-3 pt-4 border-t">
              <button type="button" @click="closeModal" 
                      class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                Cancelar
              </button>
              <button type="submit" :disabled="savingPurchase"
                      class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2 transition-colors">
                <svg v-if="savingPurchase" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ editingPurchase ? 'Actualizar' : 'Crear' }} Compra
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal detalle -->
      <div v-if="selectedPurchase" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg max-w-3xl w-full p-6 max-h-[90vh] overflow-y-auto">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Detalle de Compra</h2>
            <button @click="selectedPurchase = null" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">Nombre</label>
                <p class="text-gray-900">{{ selectedPurchase.name }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Estado</label>
                <p><span :class="getStatusBadgeClass(selectedPurchase.status)">{{ selectedPurchase.status }}</span></p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Tipo</label>
                <p class="text-gray-900">{{ selectedPurchase.type }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Cantidad</label>
                <p class="text-gray-900">{{ selectedPurchase.amount }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Método de envío</label>
                <p class="text-gray-900">{{ selectedPurchase.shipping_method || '-' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Código de envío</label>
                <p class="text-gray-900 font-mono">{{ selectedPurchase.shipping_code || '-' }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Costo de envío</label>
                <p class="text-gray-900">{{ formatCurrency(selectedPurchase.shipping_cost) }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Calidad</label>
                <p class="text-gray-900">{{ selectedPurchase.quality || '-' }}</p>
              </div>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Justificación</label>
              <p class="text-gray-900">{{ selectedPurchase.justification || '-' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Comentarios</label>
              <p class="text-gray-900">{{ selectedPurchase.comments || '-' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Fecha de creación</label>
              <p class="text-gray-900">{{ formatDate(selectedPurchase.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de Proveedores -->
      <div v-if="showSupplierModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-semibold text-gray-900">Gestión de Proveedores</h3>
              <button @click="closeSupplierModal" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="p-6">
            <!-- Lista de Proveedores -->
            <div class="mb-6">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Proveedores Registrados</h4>
              <div v-if="loadingSuppliers" class="text-center py-4">
                <p class="text-gray-500">Cargando proveedores...</p>
              </div>
              <div v-else-if="suppliers.length === 0" class="text-center py-8 bg-gray-50 rounded-lg">
                <p class="text-gray-500">No hay proveedores registrados</p>
              </div>
              <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="supplier in suppliers" :key="supplier.supplier_id" 
                     class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                  <span class="text-sm font-medium text-gray-900">{{ supplier.name }}</span>
                  <button @click="deleteSupplier(supplier.supplier_id)" 
                          class="text-red-500 hover:text-red-700">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Formulario para Nuevo Proveedor -->
            <div class="border-t pt-6">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Registrar Nuevo Proveedor</h4>
              <form @submit.prevent="createSupplier" class="flex gap-3">
                <input v-model="supplierForm.name" 
                       type="text" 
                       required 
                       placeholder="Nombre del proveedor (Ej: Distribuidora XYZ, TecnoOffice...)" 
                       class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                <button type="submit" 
                        class="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 whitespace-nowrap flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Agregar
                </button>
              </form>
            </div>
          </div>

          <div class="p-6 border-t flex justify-end">
            <button @click="closeSupplierModal" class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseTable from '@/components/BaseTable.vue'
import { purchaseService } from '@/services/purchaseService.ts'
import { equipmentService } from '@/services/equipmentService.ts'
import { sparepartService } from '@/services/sparepartService.ts'
import { useAuthStore } from '@/stores/auth.ts'
import { useFiltersStore } from '@/stores/filters.ts'
import type { Purchase, Supplier, Sparepart, PurchaseCreate } from '@/types'

// Router
const router = useRouter()

// Stores
const authStore = useAuthStore()
const filtersStore = useFiltersStore()

// Estado local
const purchases = ref<Purchase[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showCreateModal = ref(false)
const editingPurchase = ref<Purchase | null>(null)
const selectedPurchase = ref<Purchase | null>(null)

// Estado de proveedores
const showSupplierModal = ref(false)
const suppliers = ref<Supplier[]>([])
const loadingSuppliers = ref(false)
const supplierForm = ref({ name: '' })

// Estado de refacciones
const spareparts = ref<Sparepart[]>([])
const savingPurchase = ref(false)

// Formulario de compra
const purchaseForm = ref<PurchaseCreate>({
  name: '',
  sparepart_id: 0,
  user_id: 0,
  amount: 1,
  type: 'Interna',
  quality: '',
  justification: '',
  comments: '',
  supplier1_name: '',
  supplier1_cost: undefined,
  supplier2_name: '',
  supplier2_cost: undefined,
  supplier3_name: '',
  supplier3_cost: undefined,
  shipping_method: '',
  shipping_code: '',
  shipping_cost: undefined
})

// Computados desde stores
const filters = computed(() => filtersStore.filters.purchases || {})
const pagination = computed(() => filtersStore.pagination.purchases || { page: 1, page_size: 10, total: 0, total_pages: 0 })

const stats = ref({
  total: 0,
  inProgress: 0,
  inTransit: 0,
  completed: 0
})

const columns = [
  {
    key: 'name',
    label: 'Nombre',
    cellClass: 'text-sm font-medium text-gray-900'
  },
  {
    key: 'amount',
    label: 'Cantidad',
    format: (row) => row.amount || 0,
    cellClass: 'text-sm text-gray-900'
  },
  {
    key: 'type',
    label: 'Tipo',
    cellClass: 'text-sm'
  },
  {
    key: 'status',
    label: 'Estado',
    badge: true,
    cellClass: 'text-sm'
  },
  {
    key: 'shipping_code',
    label: 'Código Envío',
    format: (row) => row.shipping_code || '-',
    cellClass: 'text-sm text-gray-600 font-mono'
  },
  {
    key: 'shipping_method',
    label: 'Método',
    format: (row) => row.shipping_method || '-',
    cellClass: 'text-sm text-gray-600'
  },
  {
    key: 'created_at',
    label: 'Fecha',
    format: (row) => formatDate(row.created_at),
    cellClass: 'text-sm text-gray-600'
  }
]

const loadPurchases = async () => {
  loading.value = true
  error.value = null
  try {
    const options = filtersStore.getRequestConfig('purchases')
    const response = await purchaseService.getPurchases(options)
    
    purchases.value = response.items || []
    filtersStore.setPagination('purchases', {
      page: response.page || 1,
      page_size: response.page_size || 10,
      total: response.total || 0,
      total_pages: response.total_pages || 0
    })
    
    calculateStats()
  } catch (err: any) {
    error.value = err.message || 'Error al cargar las compras'
    console.error('Error loading purchases:', err)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.value.total = pagination.value.total
  stats.value.inProgress = purchases.value.filter(p => p.status === 'En Curso').length
  stats.value.inTransit = purchases.value.filter(p => p.status === 'En Tránsito').length
  stats.value.completed = purchases.value.filter(p => p.status === 'Concluido').length
}

const handleSearch = (query: string) => {
  filtersStore.setFilter('purchases', 'search', query)
  filtersStore.setPage('purchases', 1)
  loadPurchases()
}

const handlePageChange = (page: number) => {
  filtersStore.setPage('purchases', page)
  loadPurchases()
}

const getStatusBadgeClass = (status: string): string => {
  const statusColors: Record<string, string> = {
    'En Curso': 'bg-yellow-100 text-yellow-800',
    'En Tránsito': 'bg-blue-100 text-blue-800',
    'Concluido': 'bg-green-100 text-green-800',
    'Pausado Back Orders': 'bg-orange-100 text-orange-800',
    'Falta Pago Proveedor': 'bg-red-100 text-red-800',
    'Falta Factura': 'bg-pink-100 text-pink-800',
    'Por Revisar': 'bg-purple-100 text-purple-800',
    'Solicitud Guía Almacén': 'bg-indigo-100 text-indigo-800',
    'Rechazado': 'bg-gray-100 text-gray-800',
    'Falta Autorización': 'bg-amber-100 text-amber-800',
    'Falta Orden de Servicio': 'bg-teal-100 text-teal-800'
  }
  return `px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${statusColors[status] || 'bg-gray-100 text-gray-800'}`
}

const viewDetails = (purchase: Purchase) => {
  router.push({ name: 'CompraDetalle', params: { id: purchase.purchase_id } })
}

const editPurchase = async (purchase: Purchase) => {
  editingPurchase.value = purchase
  await loadFormData()
  // Llenar el formulario con los datos existentes
  purchaseForm.value = {
    name: purchase.name,
    sparepart_id: purchase.sparepart_id,
    user_id: purchase.user_id,
    amount: purchase.amount,
    type: purchase.type,
    quality: purchase.quality || '',
    justification: purchase.justification || '',
    comments: purchase.comments || '',
    supplier1_name: purchase.supplier1_name || '',
    supplier1_cost: purchase.supplier1_cost,
    supplier2_name: purchase.supplier2_name || '',
    supplier2_cost: purchase.supplier2_cost,
    supplier3_name: purchase.supplier3_name || '',
    supplier3_cost: purchase.supplier3_cost,
    shipping_method: purchase.shipping_method || '',
    shipping_code: purchase.shipping_code || '',
    shipping_cost: purchase.shipping_cost
  }
  showCreateModal.value = true
}

const goToCreate = () => {
  openCreateModal()
}

const updateStatus = async (purchase: Purchase) => {
  // Implementar cambio de estado
  console.log('Update status:', purchase)
}

const canEdit = (purchase: Purchase): boolean => {
  if (!authStore.hasPermission('update_purchase')) return false
  return purchase.status !== 'Concluido' && purchase.status !== 'Rechazado'
}

const canChangeStatus = (purchase: Purchase): boolean => {
  if (!authStore.hasPermission('update_purchase')) return false
  return purchase.status !== 'Concluido' && purchase.status !== 'Rechazado'
}

const closeModal = () => {
  showCreateModal.value = false
  editingPurchase.value = null
  resetPurchaseForm()
}

const resetPurchaseForm = () => {
  purchaseForm.value = {
    name: '',
    sparepart_id: 0,
    user_id: authStore.user?.contact_id || 0,
    amount: 1,
    type: 'Interna',
    quality: '',
    justification: '',
    comments: '',
    supplier1_name: '',
    supplier1_cost: undefined,
    supplier2_name: '',
    supplier2_cost: undefined,
    supplier3_name: '',
    supplier3_cost: undefined,
    shipping_method: '',
    shipping_code: '',
    shipping_cost: undefined
  }
}

const openCreateModal = async () => {
  resetPurchaseForm()
  editingPurchase.value = null
  showCreateModal.value = true
  await loadFormData()
}

const loadFormData = async () => {
  try {
    // Cargar refacciones y proveedores en paralelo
    const [sparepartsRes, suppliersRes] = await Promise.all([
      sparepartService.getSpareparts({ pageSize: 500 }),
      equipmentService.getSuppliers()
    ])
    spareparts.value = sparepartsRes.items || []
    suppliers.value = suppliersRes || []
  } catch (err: any) {
    console.error('Error loading form data:', err)
  }
}

const savePurchase = async () => {
  if (!purchaseForm.value.name || !purchaseForm.value.sparepart_id || !purchaseForm.value.amount) {
    alert('Por favor completa los campos obligatorios')
    return
  }
  
  savingPurchase.value = true
  try {
    // Asegurar user_id
    purchaseForm.value.user_id = authStore.user?.contact_id || 0
    
    if (editingPurchase.value) {
      await purchaseService.updatePurchase(editingPurchase.value.purchase_id, purchaseForm.value)
      alert('Compra actualizada exitosamente')
    } else {
      await purchaseService.createPurchase(purchaseForm.value)
      alert('Compra creada exitosamente')
    }
    closeModal()
    await loadPurchases()
  } catch (err: any) {
    console.error('Error saving purchase:', err)
    alert('Error al guardar la compra: ' + (err.message || err))
  } finally {
    savingPurchase.value = false
  }
}

const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' })
// Funciones de proveedores
const openSupplierModal = async () => {
  showSupplierModal.value = true
  await loadSuppliers()
}

const closeSupplierModal = () => {
  showSupplierModal.value = false
  supplierForm.value = { name: '' }
}

const loadSuppliers = async () => {
  loadingSuppliers.value = true
  try {
    suppliers.value = await equipmentService.getSuppliers()
  } catch (err: any) {
    console.error('Error loading suppliers:', err)
    alert('Error al cargar proveedores: ' + err.message)
  } finally {
    loadingSuppliers.value = false
  }
}

const createSupplier = async () => {
  if (!supplierForm.value.name.trim()) return
  
  try {
    await equipmentService.createSupplier(supplierForm.value)
    supplierForm.value = { name: '' }
    await loadSuppliers()
    alert('Proveedor registrado exitosamente')
  } catch (err: any) {
    console.error('Error creating supplier:', err)
    alert('Error al registrar proveedor: ' + err.message)
  }
}

const deleteSupplier = async (supplierId: number) => {
  if (!confirm('¿Está seguro de eliminar este proveedor?')) return
  
  try {
    await equipmentService.deleteSupplier(supplierId)
    await loadSuppliers()
    alert('Proveedor eliminado exitosamente')
  } catch (err: any) {
    console.error('Error deleting supplier:', err)
    alert('Error al eliminar proveedor: ' + err.message)
  }
}

}

const formatCurrency = (amount: number | null | undefined): string => {
  if (!amount) return '-'
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount)
}

onMounted(() => {
  // Inicializar filtros desde store (si hay guardados)
  filtersStore.initialize()
  loadPurchases()
})
</script>
