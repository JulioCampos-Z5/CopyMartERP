<template>
  <BaseLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div class="bg-green-50 p-6 rounded-lg border border-green-200">
          <h1 class="text-3xl font-bold text-green-800 mb-2">Gestión de Compras</h1>
          <p class="text-green-600">Administra las órdenes de compra de refacciones</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4l1-12z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Total de Compras</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Curso</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.inProgress }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">En Tránsito</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.inTransit }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow border">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-sm font-medium text-gray-500">Concluidas</h3>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.completed }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white p-6 rounded-lg shadow border">
          <div class="flex flex-wrap gap-4 items-center justify-between">
            <button @click="showCreateModal = true" class="btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nueva Orden de Compra
            </button>
            <button @click="loadPurchases" class="btn-outline">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
            <div class="flex gap-2">
              <select v-model="filterStatus" class="input-field">
                <option value="">Todos los estados</option>
                <option value="En Curso">En Curso</option>
                <option value="En Tránsito">En Tránsito</option>
                <option value="Concluido">Concluido</option>
                <option value="Pausado Back Orders">Pausado</option>
                <option value="Falta Pago Proveedor">Falta Pago</option>
              </select>
              <select v-model="filterType" class="input-field">
                <option value="">Todos los tipos</option>
                <option value="Interna">Interna</option>
                <option value="Venta">Venta</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Purchases Table -->
        <div class="bg-white rounded-lg shadow border">
          <div class="p-6 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900">Órdenes de Compra</h2>
          </div>
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <p class="text-gray-500">Cargando compras...</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full table-auto">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Refacción</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cantidad</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Envío</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredPurchases.length === 0">
                    <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                      No hay órdenes de compra registradas
                    </td>
                  </tr>
                  <tr v-for="purchase in filteredPurchases" :key="purchase.purchase_id">
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-green-600">#{{ purchase.purchase_id }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ purchase.name }}</td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ purchase.sparepart?.name || '-' }}
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{{ purchase.amount }}</td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="getTypeClass(purchase.type)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ purchase.type }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span :class="getStatusClass(purchase.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ purchase.status }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ purchase.shipping_code || '-' }}
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button @click="editPurchase(purchase)" class="text-blue-600 hover:text-blue-900">Editar</button>
                      <button @click="viewDetails(purchase)" class="text-purple-600 hover:text-purple-900">Ver</button>
                      <button @click="deletePurchase(purchase.purchase_id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Purchase Modal -->