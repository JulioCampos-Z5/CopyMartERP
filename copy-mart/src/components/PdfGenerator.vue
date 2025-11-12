<template>
  <div class="card">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Generar PDFs</h3>
    
    <div class="space-y-4">
      <!-- Botones para generar diferentes tipos de PDF -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <button 
          @click="generateSalesPdf"
          class="btn-primary text-sm"
          :disabled="generating"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Reporte de Ventas
        </button>
        
        <button 
          @click="generateInventoryPdf"
          class="btn-primary text-sm"
          :disabled="generating"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Reporte Inventario
        </button>
        
        <button 
          @click="generateUsersPdf"
          class="btn-primary text-sm"
          :disabled="generating"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          Reporte Usuarios
        </button>
        
        <button 
          @click="generateInvoice"
          class="btn-primary text-sm"
          :disabled="generating"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Factura Ejemplo
        </button>
      </div>
      
      <!-- Sección para PDF desde elemento HTML -->
      <div class="border-t pt-4">
        <h4 class="text-md font-medium text-gray-900 mb-3">Generar PDF desde elemento HTML</h4>
        
        <!-- Elemento de ejemplo para convertir a PDF -->
        <div id="pdf-content" class="bg-white p-6 border border-gray-200 rounded-lg mb-4">
          <h2 class="text-xl font-bold text-gray-900 mb-4">Ejemplo de Contenido para PDF</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 class="font-semibold text-gray-800 mb-2">Información de la Empresa</h3>
              <p class="text-gray-600">CopyMart ERP</p>
              <p class="text-gray-600">Servicios de Copiado e Impresión</p>
              <p class="text-gray-600">RFC: COPY123456789</p>
              <p class="text-gray-600">Tel: +52 55 1234-5678</p>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 mb-2">Estadísticas del Día</h3>
              <div class="space-y-1">
                <p class="text-gray-600">Ventas realizadas: 25</p>
                <p class="text-gray-600">Total del día: $4,250.00</p>
                <p class="text-gray-600">Clientes atendidos: 18</p>
                <p class="text-gray-600">Productos vendidos: 67</p>
              </div>
            </div>
          </div>
          
          <div class="mt-6">
            <h3 class="font-semibold text-gray-800 mb-2">Productos Más Vendidos</h3>
            <div class="bg-gray-50 p-4 rounded">
              <div class="flex justify-between items-center mb-2">
                <span class="text-gray-700">Papel A4 - 500 hojas</span>
                <span class="font-medium">45 unidades</span>
              </div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-gray-700">Copias B/N</span>
                <span class="font-medium">320 copias</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-700">Tinta HP 662</span>
                <span class="font-medium">12 unidades</span>
              </div>
            </div>
          </div>
        </div>
        
        <button 
          @click="generatePdfFromHtml"
          class="btn-secondary"
          :disabled="generating"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
          </svg>
          Generar PDF desde Contenido HTML
        </button>
      </div>
      
      <!-- Indicador de carga -->
      <div v-if="generating" class="flex items-center justify-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span class="ml-2 text-gray-600">Generando PDF...</span>
      </div>
      
      <!-- Mensaje de estado -->
      <div v-if="message" :class="[
        'p-3 rounded-md text-sm',
        messageType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      ]">
        {{ message }}
      </div>
    </div>
  </div>
  
  <!-- Modal de vista previa del PDF -->
  <div v-if="showPreviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-11/12 h-5/6 max-w-6xl flex flex-col">
      <!-- Header del modal -->
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-800">Vista Previa del PDF</h3>
        <div class="flex space-x-3">
          <button 
            @click="downloadCurrentPdf"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Descargar
          </button>
          <button 
            @click="closePreview"
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Cerrar
          </button>
        </div>
      </div>
      
      <!-- Contenido del PDF -->
      <div class="flex-1 overflow-hidden rounded border">
        <iframe 
          v-if="previewUrl" 
          :src="previewUrl" 
          class="w-full h-full"
          title="Vista previa del PDF"
        ></iframe>
        <div v-else class="flex items-center justify-center h-full text-gray-500">
          <p>No se pudo cargar la vista previa del PDF</p>
        </div>
      </div>
      
      <!-- Footer del modal -->
      <div class="mt-4 text-sm text-gray-600 text-center">
        <p>{{ currentFilename }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { usePdfGenerator } from '../composables/usePdfGenerator.js'

export default {
  name: 'PdfGenerator',
  data() {
    return {
      generating: false,
      message: '',
      messageType: 'success',
      showPreviewModal: false,
      previewUrl: '',
      currentPdf: null,
      currentFilename: ''
    }
  },
  setup() {
    const { generatePdfFromElement, generateReportPdf, generateInvoicePdf, downloadPdf } = usePdfGenerator()
    
    return {
      generatePdfFromElement,
      generateReportPdf,
      generateInvoicePdf,
      downloadPdf
    }
  },
  methods: {
    async showMessage(message, type = 'success') {
      this.message = message
      this.messageType = type
      setTimeout(() => {
        this.message = ''
      }, 3000)
    },
    
    async generateSalesPdf() {
      this.generating = true
      
      // Datos de ejemplo para el reporte de ventas
      const salesData = [
        {
          fecha: '06/11/2025',
          cliente: 'María González',
          producto: 'Papel A4 - 500 hojas',
          cantidad: 2,
          total: 250
        },
        {
          fecha: '06/11/2025',
          cliente: 'José Ramírez',
          producto: 'Tinta HP 662',
          cantidad: 1,
          total: 890
        },
        {
          fecha: '05/11/2025',
          cliente: 'Ana Martínez',
          producto: 'Copias B/N - 1000 unid.',
          cantidad: 1,
          total: 450
        },
        {
          fecha: '05/11/2025',
          cliente: 'Luis Torres',
          producto: 'Encuadernación',
          cantidad: 3,
          total: 960
        }
      ]
      
      const result = this.generateReportPdf(salesData, 'ventas', 'reporte-ventas.pdf', true)
      
      this.generating = false
      
      if (result.success) {
        this.showPreview(result.previewUrl, result.pdf, result.filename)
      } else {
        this.showMessage(result.message, 'error')
      }
    },
    
    async generateInventoryPdf() {
      this.generating = true
      
      // Datos de ejemplo para el inventario
      const inventoryData = [
        {
          nombre: 'Papel A4 - 500 hojas',
          sku: 'PPL-A4-500',
          stock: 45,
          stockMinimo: 20
        },
        {
          nombre: 'Tinta HP 662 Negro',
          sku: 'TNT-HP-662-N',
          stock: 8,
          stockMinimo: 10
        },
        {
          nombre: 'Papel Fotográfico A4',
          sku: 'PPL-FOTO-A4',
          stock: 15,
          stockMinimo: 15
        },
        {
          nombre: 'Copias B/N',
          sku: 'COP-BN',
          stock: 1000,
          stockMinimo: 500
        }
      ]
      
      const result = this.generateReportPdf(inventoryData, 'inventario', 'reporte-inventario.pdf', true)
      
      this.generating = false
      
      if (result.success) {
        this.showPreview(result.previewUrl, result.pdf, result.filename)
      } else {
        this.showMessage(result.message, 'error')
      }
    },
    
    async generateUsersPdf() {
      this.generating = true
      
      // Datos de ejemplo de usuarios
      const usersData = [
        {
          name: 'Juan Pérez García',
          email: 'juan.perez@copymart.com',
          role: 'Administrador',
          status: 'Activo'
        },
        {
          name: 'María González López',
          email: 'maria.gonzalez@copymart.com',
          role: 'Gerente',
          status: 'Activo'
        },
        {
          name: 'Carlos Rodríguez',
          email: 'carlos.rodriguez@copymart.com',
          role: 'Empleado',
          status: 'Activo'
        },
        {
          name: 'Ana Martínez',
          email: 'ana.martinez@copymart.com',
          role: 'Empleado',
          status: 'Inactivo'
        }
      ]
      
      const result = this.generateReportPdf(usersData, 'usuarios', 'reporte-usuarios.pdf', true)
      
      this.generating = false
      
      if (result.success) {
        this.showPreview(result.previewUrl, result.pdf, result.filename)
      } else {
        this.showMessage(result.message, 'error')
      }
    },
    
    async generateInvoice() {
      this.generating = true
      
      // Datos de ejemplo para la factura
      const invoiceData = {
        folio: 'F-001234',
        fecha: new Date().toLocaleDateString('es-ES'),
        cliente: {
          nombre: 'María González López',
          email: 'maria.gonzalez@email.com',
          telefono: '+52 55 1234-5678'
        },
        items: [
          {
            descripcion: 'Papel A4 - 500 hojas',
            cantidad: 2,
            precio: 125.00
          },
          {
            descripcion: 'Copias B/N',
            cantidad: 500,
            precio: 0.90
          },
          {
            descripcion: 'Encuadernación',
            cantidad: 1,
            precio: 85.00
          }
        ],
        metodoPago: 'Efectivo'
      }
      
      const result = this.generateInvoicePdf(invoiceData, 'factura-ejemplo.pdf', true)
      
      this.generating = false
      
      if (result.success) {
        this.showPreview(result.previewUrl, result.pdf, result.filename)
      } else {
        this.showMessage(result.message, 'error')
      }
    },
    
    async generatePdfFromHtml() {
      this.generating = true
      
      const result = await this.generatePdfFromElement('pdf-content', 'contenido-ejemplo.pdf', {}, true)
      
      this.generating = false
      
      if (result.success) {
        this.showPreview(result.previewUrl, result.pdf, result.filename)
      } else {
        this.showMessage(result.message, 'error')
      }
    },
    
    showPreview(previewUrl, pdf, filename) {
      this.previewUrl = previewUrl
      this.currentPdf = pdf
      this.currentFilename = filename
      this.showPreviewModal = true
    },
    
    closePreview() {
      this.showPreviewModal = false
      this.previewUrl = ''
      this.currentPdf = null
      this.currentFilename = ''
      
      // Limpiar URL del blob para evitar memory leaks
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl)
      }
    },
    
    downloadCurrentPdf() {
      if (this.currentPdf && this.currentFilename) {
        const result = this.downloadPdf(this.currentPdf, this.currentFilename)
        this.showMessage(result.message, result.success ? 'success' : 'error')
        this.closePreview()
      }
    }
  }
}
</script>