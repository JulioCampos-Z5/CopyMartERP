<template>
<<<<<<< HEAD
  <nav class="bg-white shadow-lg border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo y marca -->
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <svg class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h1 class="ml-2 text-xl font-bold text-gray-900">CopyMart ERP</h1>
          </div>
          
          <!-- Navegación principal (escritorio) -->
          <div class="hidden md:block ml-10">
            <div class="flex items-baseline space-x-4">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.to"
                :class="[
                  isActive(item.to) 
                    ? 'bg-primary-100 text-primary-700 border-primary-500' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'px-3 py-2 rounded-md text-sm font-medium border-b-2 border-transparent hover:border-gray-300 transition-colors duration-200'
                ]"
              >
                <svg class="h-4 w-4 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                </svg>
                {{ item.name }}
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Acciones de usuario -->
        <div class="hidden md:flex items-center space-x-4">
          <!-- Notificaciones -->
          <button class="relative p-2 text-gray-600 hover:text-gray-900 rounded-full hover:bg-gray-100 transition-colors duration-200">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-3.5-3.5a.5.5 0 010-.707L20 9.5V6a2 2 0 00-2-2h-4a2 2 0 00-2 2v3.5l3.5 3.5z" />
            </svg>
            <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
          </button>
          
          <!-- Menú de usuario -->
          <div class="relative" v-click-outside="closeUserMenu">
            <button 
              @click="toggleUserMenu"
              class="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors duration-200"
            >
              <div class="h-8 w-8 bg-primary-600 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-white">{{ userInitials }}</span>
              </div>
              <span class="text-sm font-medium">{{ userName }}</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <!-- Dropdown del usuario -->
            <div 
              v-show="showUserMenu"
              class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
            >
              <div class="py-1">
                <a 
                  v-for="item in userMenuItems"
                  :key="item.name"
                  :href="item.href"
                  @click="item.action && item.action(); closeUserMenu()"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                >
                  <svg class="h-4 w-4 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                  </svg>
                  {{ item.name }}
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Botón de menú móvil -->
        <div class="md:hidden">
          <button 
            @click="toggleMobileMenu"
            class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors duration-200"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Menú móvil -->
      <div v-show="showMobileMenu" class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1 bg-gray-50">
          <router-link
            v-for="item in navigation"
            :key="item.name"
            :to="item.to"
            @click="showMobileMenu = false"
            :class="[
              isActive(item.to) 
                ? 'bg-primary-100 text-primary-700' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
              'block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200'
            ]"
          >
            <svg class="h-5 w-5 inline-block mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
            </svg>
            {{ item.name }}
          </router-link>
        </div>
        
        <!-- Usuario móvil -->
        <div class="pt-4 pb-3 border-t border-gray-200">
          <div class="flex items-center px-4">
            <div class="h-10 w-10 bg-primary-600 rounded-full flex items-center justify-center">
              <span class="text-sm font-medium text-white">{{ userInitials }}</span>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ userName }}</div>
              <div class="text-sm text-gray-500">{{ userEmail }}</div>
            </div>
          </div>
          <div class="mt-3 px-2 space-y-1">
            <a 
              v-for="item in userMenuItems"
              :key="item.name"
              :href="item.href"
              @click="item.action && item.action(); showMobileMenu = false"
              class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors duration-200"
            >
              {{ item.name }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { usePermissions } from '../composables/usePermissions'
import { computed } from 'vue'
=======
  <!-- Sidebar -->
  <div :class="[isCollapsed ? 'w-16' : 'w-64', 'bg-white shadow-lg transition-all duration-300 h-screen flex flex-col']">
    <!-- Logo -->
    <div :class="[isCollapsed ? 'p-2' : 'p-4', 'border-b border-gray-200']">
      <div :class="[isCollapsed ? 'flex-col space-y-2' : 'flex items-center justify-between']">
        <div :class="[isCollapsed ? 'flex justify-center' : 'flex items-center']">
          <svg class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h1 v-if="!isCollapsed" class="ml-2 text-xl font-bold text-gray-900 transition-opacity duration-300">CopyMart ERP</h1>
        </div>
        <button
          @click="isCollapsed = !isCollapsed"
          :class="[isCollapsed ? 'mx-auto' : '', 'p-1 text-gray-500 hover:text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200']"
        >
          <svg :class="[isCollapsed ? 'rotate-180' : '', 'h-5 w-5 transition-transform duration-300']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Navegación -->
    <nav class="flex-1 overflow-y-auto">
      <div :class="[isCollapsed ? 'px-2 py-4' : 'px-4 py-4', 'space-y-2']">
          
          <!-- Dashboard -->
          <router-link
            to="/dashboard"
            :class="[
              isActive('/dashboard') 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
              'flex items-center text-sm font-medium rounded-md transition-colors duration-200',
              isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
            ]"
            :title="isCollapsed ? 'Dashboard' : ''"
          >
            <svg class="h-5 w-5 flex-shrink-0" :class="isCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
            </svg>
            <span v-if="!isCollapsed" class="transition-opacity duration-300">Dashboard</span>
          </router-link>

          <!-- Comercial -->
          <div class="space-y-1">
            <button
              @click="toggleSection('comercial')"
              :class="[
                openSections.comercial || isActive('/ventas') || isActive('/rentas') || isActive('/atencion-clientes') || isActive('/clientes') ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-100',
                isCollapsed ? 'flex items-center justify-center p-3' : 'flex items-center justify-between w-full px-3 py-2',
                'text-sm font-medium rounded-md transition-colors duration-200'
              ]"
              :title="isCollapsed ? 'Comercial' : ''"
            >
              <div :class="[isCollapsed ? '' : 'flex items-center']">
                <svg :class="[isCollapsed ? 'h-5 w-5' : 'h-5 w-5 flex-shrink-0 mr-3']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4l1-12z" />
                </svg>
                <span v-if="!isCollapsed">Comercial</span>
              </div>
              <svg
                v-if="!isCollapsed"
                :class="openSections.comercial ? 'rotate-90' : ''"
                class="h-4 w-4 transition-transform duration-200 flex-shrink-0"
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
            
            <div :class="[isCollapsed ? 'space-y-1' : 'ml-6 space-y-1']" v-show="openSections.comercial">
              <router-link
                to="/clientes"
                :class="[
                  isActive('/clientes') ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Gestión de Clientes' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span v-if="!isCollapsed">Gestión de Clientes</span>
              </router-link>
              <router-link
                to="/ventas"
                :class="[
                  isActive('/ventas') ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Ventas' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <span v-if="!isCollapsed">Ventas</span>
              </router-link>
              <router-link
                to="/rentas"
                :class="[
                  isActive('/rentas') ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Rentas' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span v-if="!isCollapsed">Rentas</span>
              </router-link>
              <router-link
                to="/atencion-clientes"
                :class="[
                  isActive('/atencion-clientes') ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Atención a Clientes' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <span v-if="!isCollapsed">Atención a Clientes</span>
              </router-link>
            </div>
          </div>

          <!-- Administración -->
          <div class="space-y-1">
            <button
              @click="toggleSection('administracion')"
              :class="[
                openSections.administracion || isActive('/compras') || isActive('/almacen') || isActive('/cobranza') || isActive('/facturacion') || isActive('/inventario') ? 'text-green-600 bg-green-50' : 'text-gray-700 hover:bg-gray-100',
                'flex items-center w-full rounded-md transition-colors duration-200',
                isCollapsed ? 'justify-center p-3' : 'justify-between px-3 py-2 text-sm font-medium'
              ]"
              :title="isCollapsed ? 'Administración' : ''"
            >
              <div class="flex items-center">
                <svg :class="[isCollapsed ? 'h-5 w-5' : 'h-5 w-5 flex-shrink-0 mr-3']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span v-if="!isCollapsed" class="transition-opacity duration-300">Administración</span>
              </div>
              <svg
                v-if="!isCollapsed"
                :class="openSections.administracion ? 'rotate-90' : ''"
                class="h-4 w-4 transition-transform duration-200 flex-shrink-0"
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
            
            <!-- Submenús de Administración -->
            <div :class="[isCollapsed ? 'space-y-1' : 'ml-6 space-y-1']" v-show="openSections.administracion">
              <router-link
                to="/inventario"
                :class="[
                  isActive('/inventario') ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Inventario de Equipos' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                <span v-if="!isCollapsed">Inventario de Equipos</span>
              </router-link>
              <router-link
                to="/compras"
                :class="[
                  isActive('/compras') ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Compras' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4l1-12z" />
                </svg>
                <span v-if="!isCollapsed">Compras</span>
              </router-link>
              <router-link
                to="/almacen"
                :class="[
                  isActive('/almacen') ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Almacén' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2h4a1 1 0 011 1v2a1 1 0 01-1 1h-1v12a2 2 0 01-2 2H6a2 2 0 01-2-2V8H3a1 1 0 01-1-1V5a1 1 0 011-1h4z" />
                </svg>
                <span v-if="!isCollapsed">Almacén</span>
              </router-link>
              <router-link
                to="/cobranza"
                :class="[
                  isActive('/cobranza') ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Cobranza' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
                <span v-if="!isCollapsed">Cobranza</span>
              </router-link>
              <router-link
                to="/facturacion"
                :class="[
                  isActive('/facturacion') ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Facturación' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span v-if="!isCollapsed">Facturación</span>
              </router-link>
            </div>
          </div>

          <!-- Recursos Humanos -->
          <router-link
            to="/recursos-humanos"
            :class="[
              isActive('/recursos-humanos') 
                ? 'bg-purple-100 text-purple-700' 
                : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
              'flex items-center text-sm font-medium rounded-md transition-colors duration-200',
              isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
            ]"
            :title="isCollapsed ? 'Recursos Humanos' : ''"
          >
            <svg class="h-5 w-5 flex-shrink-0" :class="isCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
            <span v-if="!isCollapsed" class="transition-opacity duration-300">Recursos Humanos</span>
          </router-link>

          <!-- Operaciones -->
          <div class="space-y-1">
            <button
              @click="toggleSection('operaciones')"
              :class="[
                openSections.operaciones || isActive('/rutas') || isActive('/ordenes-servicio') ? 'text-orange-600 bg-orange-50' : 'text-gray-700 hover:bg-gray-100',
                'flex items-center w-full rounded-md transition-colors duration-200',
                isCollapsed ? 'justify-center p-3' : 'justify-between px-3 py-2 text-sm font-medium'
              ]"
              :title="isCollapsed ? 'Operaciones' : ''"
            >
              <div class="flex items-center">
                <svg :class="[isCollapsed ? 'h-5 w-5' : 'h-5 w-5 flex-shrink-0 mr-3']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span v-if="!isCollapsed" class="transition-opacity duration-300">Operaciones</span>
              </div>
              <svg
                v-if="!isCollapsed"
                :class="openSections.operaciones ? 'rotate-90' : ''"
                class="h-4 w-4 transition-transform duration-200 flex-shrink-0"
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
            
            <!-- Submenús de Operaciones -->
            <div :class="[isCollapsed ? 'space-y-1' : 'ml-6 space-y-1']" v-show="openSections.operaciones">
              <router-link
                to="/rutas"
                :class="[
                  isActive('/rutas') ? 'bg-orange-100 text-orange-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Rutas' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
                <span v-if="!isCollapsed">Rutas</span>
              </router-link>
              <router-link
                to="/ordenes-servicio"
                :class="[
                  isActive('/ordenes-servicio') ? 'bg-orange-100 text-orange-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
                  'flex items-center text-sm rounded-md transition-colors duration-200',
                  isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
                ]"
                :title="isCollapsed ? 'Órdenes de Servicio' : ''"
              >
                <svg :class="[isCollapsed ? 'h-4 w-4' : 'mr-2 h-4 w-4']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
                <span v-if="!isCollapsed">Órdenes de Servicio</span>
              </router-link>
            </div>
          </div>

          <!-- Tecnologías de la Información -->
          <router-link
            to="/ti"
            :class="[
              isActive('/ti') 
                ? 'bg-indigo-100 text-indigo-700' 
                : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
              'flex items-center text-sm font-medium rounded-md transition-colors duration-200',
              isCollapsed ? 'justify-center p-3' : 'px-3 py-2'
            ]"
            :title="isCollapsed ? 'Tecnologías de Información' : ''"
          >
            <svg class="h-5 w-5 flex-shrink-0" :class="isCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <span v-if="!isCollapsed" class="transition-opacity duration-300">Tecnologías de Información</span>
          </router-link>

      </div>
    </nav>

    <!-- Footer del sidebar -->
    <div :class="[isCollapsed ? 'p-2' : 'p-4', 'border-t border-gray-200']">
      <div :class="[isCollapsed ? 'flex-col space-y-2' : 'flex items-center justify-between']">
        <!-- Botón de perfil -->
        <router-link 
          to="/perfil"
          :class="[
            isCollapsed ? 'flex justify-center w-full' : 'flex items-center flex-1',
            'hover:bg-gray-50 rounded-md transition-colors duration-200',
            isCollapsed ? 'p-2' : 'p-2'
          ]"
          :title="isCollapsed ? 'Ver mi perfil' : ''"
        >
          <div class="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
            <span class="text-white font-bold text-sm">{{ currentUser.name ? currentUser.name.charAt(0).toUpperCase() : 'U' }}</span>
          </div>
          <div v-if="!isCollapsed" class="ml-3 transition-opacity duration-300">
            <p class="text-sm font-medium text-gray-700">{{ currentUser.name || 'Usuario' }}</p>
            <p class="text-xs text-gray-500">{{ currentUser.email || 'usuario@copymart.com' }}</p>
          </div>
        </router-link>
        
        <!-- Botón de logout -->
        <button
          @click="logout"
          :class="[isCollapsed ? 'mx-auto w-full' : '', 'p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-md transition-colors duration-200']"
          :title="'Cerrar sesión'"
        >
          <svg class="h-5 w-5 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template><script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
>>>>>>> develop

export default {
  name: 'AppNavigation',
  setup() {
<<<<<<< HEAD
    const { getAccessibleModules, userInfo, canCreate, canEdit, canDelete } = usePermissions()
    
    // Mapeo de módulos a iconos SVG
    const moduleIcons = {
      'dashboard': 'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z',
      'ventas': 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
      'inventario': 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
      'clientes': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
      'reportes': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      'usuarios': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
    }
    
    // Construir navegación con módulos accesibles
    const navigation = computed(() => {
      return getAccessibleModules.value.map(module => ({
        name: module.name,
        to: module.route,
        icon: moduleIcons[module.key] || moduleIcons['dashboard']
      }))
    })
    
    return {
      navigation,
      userInfo,
      canCreate,
      canEdit,
      canDelete
    }
  },
  data() {
    return {
      showUserMenu: false,
      showMobileMenu: false,
      userMenuItems: [
        {
          name: 'Perfil',
          href: '#',
          icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
          action: () => this.$router.push('/perfil')
        },
        {
          name: 'Usuarios',
          href: '#',
          icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z',
          action: () => this.$router.push('/usuarios')
        },
        {
          name: 'Configuración',
          href: '#',
          icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'
        },
        {
          name: 'Cerrar Sesión',
          href: '#',
          icon: 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
          action: () => this.logout()
        }
      ]
    }
  },
  computed: {
    userName() {
      return this.userInfo.name
    },
    userEmail() {
      return this.userInfo.email
    },
    userInitials() {
      return this.userInfo.initials
    }
  },
  methods: {
    isActive(route) {
      return this.$route.path === route
    },
    
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
    },
    
    closeUserMenu() {
      this.showUserMenu = false
    },
    
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu
    },
    
    logout() {
      // Limpiar estado de autenticación
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('user')
      
      // Redirigir al login
      this.$router.push('/login')
    }
  },
  
  // Directiva personalizada para cerrar menús al hacer clic fuera
  directives: {
    'click-outside': {
      mounted(el, binding) {
        el.clickOutsideEvent = function (event) {
          if (!(el == event.target || el.contains(event.target))) {
            binding.value()
          }
        }
        document.addEventListener('click', el.clickOutsideEvent)
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
      }
    }
  }
}
</script>
=======
    const route = useRoute()
    const router = useRouter()

    // Estado de secciones expandibles
    const openSections = ref({
      comercial: false,
      administracion: false,
      operaciones: false
    })

    // Estado de colapso del sidebar
    const isCollapsed = ref(true)

    // Usuario actual
    const currentUser = ref({
      name: 'Usuario',
      email: 'cargando...'
    })

    // Cargar usuario actual
    const loadCurrentUser = () => {
      try {
        const userDataStr = localStorage.getItem('user')
        if (userDataStr) {
          const userData = JSON.parse(userDataStr)
          currentUser.value = {
            name: userData.name || userData.full_name || 'Usuario Demo',
            email: userData.email || 'usuario@copymart.com'
          }
        } else {
          // Datos por defecto si no hay usuario
          currentUser.value = {
            name: 'Usuario Demo',
            email: 'demo@copymart.com'
          }
        }
      } catch (error) {
        console.error('Error loading user:', error)
        currentUser.value = {
          name: 'Usuario Demo',
          email: 'demo@copymart.com'
        }
      }
    }

    // Título de página dinámico
    const pageTitle = computed(() => {
      const routeTitles = {
        '/': 'Inicio',
        '/dashboard': 'Dashboard',
        '/perfil': 'Mi Perfil',
        '/clientes': 'Gestión de Clientes',
        '/inventario': 'Inventario de Equipos',
        '/ventas': 'Ventas',
        '/rentas': 'Rentas',
        '/atencion-clientes': 'Atención a Clientes',
        '/compras': 'Compras',
        '/almacen': 'Almacén',
        '/cobranza': 'Cobranza',
        '/facturacion': 'Facturación',
        '/recursos-humanos': 'Recursos Humanos',
        '/rutas': 'Rutas',
        '/ordenes-servicio': 'Órdenes de Servicio',
        '/ti': 'Tecnologías de Información',
        '/reportes': 'Reportes',
        '/usuarios': 'Usuarios',
        '/perfil': 'Mi Perfil'
      }
      return routeTitles[route.path] || 'CopyMart ERP'
    })

    // Funciones
    const isActive = (path) => {
      return route.path === path || route.path.startsWith(path + '/')
    }

    const toggleSection = (section) => {
      openSections.value[section] = !openSections.value[section]
    }

    const toggleCollapse = () => {
      isCollapsed.value = !isCollapsed.value
    }

    const logout = async () => {
      try {
        // Limpiar localStorage
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('isAuthenticated')
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user_data')
        
        // Redirigir al login
        await router.push('/login')
      } catch (error) {
        console.error('Error durante logout:', error)
        // Asegurar limpieza y redirección incluso si hay error
        localStorage.clear()
        await router.push('/login')
      }
    }

    // Abrir secciones según la ruta actual
    const updateOpenSections = () => {
      // Comercial
      if (isActive('/ventas') || isActive('/rentas') || isActive('/atencion-clientes')) {
        openSections.value.comercial = true
      }
      // Administración
      if (isActive('/compras') || isActive('/almacen') || isActive('/cobranza') || isActive('/facturacion')) {
        openSections.value.administracion = true
      }
      // Operaciones
      if (isActive('/rutas') || isActive('/ordenes-servicio')) {
        openSections.value.operaciones = true
      }
    }

    onMounted(() => {
      // Cargar datos del usuario
      loadCurrentUser()
      // Abrir secciones según la ruta actual
      updateOpenSections()
    })

    // Observar cambios de ruta
    watch(() => route.path, () => {
      updateOpenSections()
    })

    return {
      openSections,
      isCollapsed,
      currentUser,
      isActive,
      toggleSection,
      toggleCollapse,
      logout
    }
  }
}
</script>

<style scoped>
/* Estilos adicionales si se necesitan */
</style>
>>>>>>> develop
