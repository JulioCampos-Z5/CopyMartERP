/**
 * Composable: PDF Generator (TypeScript)
 * =======================================
 * Generación de PDFs desde elementos HTML
 */

import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

interface PdfOptions {
  scale?: number
  useCORS?: boolean
  allowTaint?: boolean
  backgroundColor?: string
}

interface Html2CanvasOptions extends PdfOptions {
  [key: string]: any
}

export const usePdfGenerator = () => {
  
  // Función para generar PDF desde un elemento HTML con opción de vista previa
  const generatePdfFromElement = async (
    elementId: string, 
    filename: string = 'documento.pdf', 
    options: PdfOptions = {}, 
    showPreview: boolean = false
  ): Promise<void> => {
    try {
      const element = document.getElementById(elementId)
      if (!element) {
        throw new Error(`Elemento con ID "${elementId}" no encontrado`)
      }

      // Configuraciones por defecto
      const defaultOptions: Html2CanvasOptions = {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        ...options
      }

      // Capturar el elemento como imagen
      const canvas = await html2canvas(element, defaultOptions)
      const imgData = canvas.toDataURL('image/png')
      
      // Crear el PDF
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      })

      const imgWidth = 210 // A4 ancho en mm
      const pageHeight = 295 // A4 alto en mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      let heightLeft = imgHeight

      let position = 0

      // Agregar la primera página
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight

      // Agregar páginas adicionales si es necesario
      while (heightLeft >= 0) {
        position = heightLeft - imgHeight
        pdf.addPage()
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
        heightLeft -= pageHeight
      }

      // Si se solicita vista previa, abrir en nueva pestaña
      if (showPreview) {
        const pdfBlob = pdf.output('blob')
        const pdfUrl = URL.createObjectURL(pdfBlob)
        window.open(pdfUrl, '_blank')
      } else {
        // Descargar directamente
        pdf.save(filename)
      }

    } catch (error) {
      console.error('Error generando PDF:', error)
      throw error
    }
  }

  // Función simplificada para generar y descargar PDF
  const downloadPdf = async (elementId: string, filename: string = 'documento.pdf'): Promise<void> => {
    return generatePdfFromElement(elementId, filename, {}, false)
  }

  // Función para vista previa sin descargar
  const previewPdf = async (elementId: string): Promise<void> => {
    return generatePdfFromElement(elementId, 'preview.pdf', {}, true)
  }

  return {
    generatePdfFromElement,
    // Genera un reporte genérico a partir de datos (lista u objeto)
    generateReportPdf: (data: any, title: string, filename: string, showPreview: boolean = true) => {
      try {
        const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
        let y = 20
        pdf.setFontSize(16)
        pdf.text(`Reporte: ${title}`, 20, y)
        y += 15

        const drawArray = (arr: any[]) => {
          arr.forEach((item, index) => {
            pdf.setFontSize(10)
            pdf.text(`${index + 1}. ${JSON.stringify(item)}`, 20, y)
            y += 8
            if (y > 280) { pdf.addPage(); y = 20 }
          })
        }

        if (Array.isArray(data)) {
          drawArray(data)
        } else {
          pdf.setFontSize(10)
          const text = JSON.stringify(data, null, 2)
          const lines = pdf.splitTextToSize(text, 170)
          lines.forEach((line: string) => {
            pdf.text(line, 20, y)
            y += 6
            if (y > 280) { pdf.addPage(); y = 20 }
          })
        }

        if (showPreview) {
          const blob = pdf.output('blob')
          const url = URL.createObjectURL(blob)
          return { success: true, previewUrl: url, pdf, filename }
        } else {
          pdf.save(filename)
          return { success: true, previewUrl: '', pdf, filename }
        }
      } catch (error: any) {
        return { success: false, message: error?.message || 'Error generando reporte' }
      }
    },

    // Genera una factura con estructura básica (cliente, items, totales)
    generateInvoicePdf: (invoiceData: any, filename: string, showPreview: boolean = true) => {
      try {
        const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
        
        // Header con logo/empresa
        pdf.setFillColor(255, 140, 0) // Naranja
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.setTextColor(255, 255, 255)
        pdf.setFontSize(24)
        pdf.setFont('helvetica', 'bold')
        pdf.text('CopyMart ERP', 20, 20)
        pdf.setFontSize(10)
        pdf.setFont('helvetica', 'normal')
        pdf.text('Sistema de Gestión Empresarial', 20, 28)
        
        // Información de factura (derecha)
        pdf.setFontSize(12)
        pdf.text('FACTURA', 150, 15, { align: 'right' })
        pdf.setFontSize(9)
        pdf.text(`No. ${invoiceData.invoice_number || invoiceData.billing_id || 'N/A'}`, 150, 22, { align: 'right' })
        pdf.text(`Fecha: ${invoiceData.target_date || new Date().toLocaleDateString('es-MX')}`, 150, 28, { align: 'right' })
        pdf.text(`Vencimiento: ${invoiceData.due_date || '-'}`, 150, 34, { align: 'right' })
        
        // Restaurar color de texto
        pdf.setTextColor(0, 0, 0)
        let y = 55
        
        // Cliente
        pdf.setFontSize(14)
        pdf.setFont('helvetica', 'bold')
        pdf.text('CLIENTE', 20, y)
        y += 8
        pdf.setFontSize(10)
        pdf.setFont('helvetica', 'normal')
        pdf.text(`${invoiceData.client_name || 'N/A'}`, 20, y)
        y += 6
        if (invoiceData.branch_name) {
          pdf.text(`Sucursal: ${invoiceData.branch_name}`, 20, y)
          y += 6
        }
        y += 5
        
        // Estado
        pdf.setFontSize(10)
        pdf.setFont('helvetica', 'bold')
        const statusColors: any = {
          'pendiente': [255, 193, 7],
          'pagado': [76, 175, 80],
          'vencido': [244, 67, 54],
          'cancelado': [158, 158, 158]
        }
        const statusColor = statusColors[String(invoiceData.status).toLowerCase()] || [158, 158, 158]
        pdf.setFillColor(statusColor[0], statusColor[1], statusColor[2])
        pdf.setTextColor(255, 255, 255)
        pdf.rect(20, y - 4, 30, 7, 'F')
        pdf.text(String(invoiceData.status).toUpperCase(), 35, y, { align: 'center' })
        pdf.setTextColor(0, 0, 0)
        y += 12
        
        // Detalles de la transacción
        pdf.setFontSize(14)
        pdf.setFont('helvetica', 'bold')
        pdf.text('DETALLES', 20, y)
        y += 8
        pdf.setFontSize(10)
        pdf.setFont('helvetica', 'normal')
        
        // Tipo de factura
        pdf.text(`Tipo: ${invoiceData.billing_type || 'N/A'}`, 20, y)
        y += 6
        
        // Información de venta o renta
        if (invoiceData.sale_info) {
          pdf.setFont('helvetica', 'bold')
          pdf.text('Venta Asociada:', 20, y)
          y += 6
          pdf.setFont('helvetica', 'normal')
          pdf.text(`  Factura: ${invoiceData.sale_info.invoice_number}`, 20, y)
          y += 6
          pdf.text(`  Monto: $${Number(invoiceData.sale_info.amount).toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`, 20, y)
          y += 6
        } else if (invoiceData.rent_info) {
          pdf.setFont('helvetica', 'bold')
          pdf.text('Renta Asociada:', 20, y)
          y += 6
          pdf.setFont('helvetica', 'normal')
          pdf.text(`  Contrato: ${invoiceData.rent_info.contract_number}`, 20, y)
          y += 6
          pdf.text(`  Renta Mensual: $${Number(invoiceData.rent_info.amount).toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`, 20, y)
          y += 6
        }
        y += 8
        
        // Tabla de montos
        pdf.setFillColor(240, 240, 240)
        pdf.rect(20, y - 2, 170, 8, 'F')
        pdf.setFont('helvetica', 'bold')
        pdf.text('CONCEPTO', 25, y + 3)
        pdf.text('IMPORTE', 170, y + 3, { align: 'right' })
        y += 10
        
        pdf.setFont('helvetica', 'normal')
        const subtotal = Number(invoiceData.amount_subtotal || 0)
        const tax = Number(invoiceData.amount_tax || 0)
        const total = Number(invoiceData.amount_total || 0)
        
        // Subtotal
        pdf.text('Subtotal', 25, y)
        pdf.text(`$${subtotal.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`, 185, y, { align: 'right' })
        y += 7
        
        // IVA
        pdf.text('IVA (16%)', 25, y)
        pdf.text(`$${tax.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`, 185, y, { align: 'right' })
        y += 10
        
        // Total
        pdf.setFillColor(255, 140, 0)
        pdf.rect(20, y - 4, 170, 10, 'F')
        pdf.setTextColor(255, 255, 255)
        pdf.setFont('helvetica', 'bold')
        pdf.setFontSize(12)
        pdf.text('TOTAL', 25, y + 2)
        pdf.text(`$${total.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`, 185, y + 2, { align: 'right' })
        pdf.setTextColor(0, 0, 0)
        pdf.setFontSize(10)
        y += 15
        
        // Fechas
        if (invoiceData.payment_date) {
          pdf.setFont('helvetica', 'normal')
          pdf.text(`Fecha de Pago: ${invoiceData.payment_date}`, 20, y)
          y += 6
        }
        
        // Comentarios
        if (invoiceData.comment) {
          y += 5
          pdf.setFont('helvetica', 'bold')
          pdf.text('COMENTARIOS:', 20, y)
          y += 6
          pdf.setFont('helvetica', 'normal')
          const commentLines = pdf.splitTextToSize(invoiceData.comment, 170)
          commentLines.forEach((line: string) => {
            pdf.text(line, 20, y)
            y += 5
            if (y > 270) { pdf.addPage(); y = 20 }
          })
        }
        
        // Footer
        pdf.setFontSize(8)
        pdf.setTextColor(128, 128, 128)
        pdf.text('Gracias por su preferencia - CopyMart ERP', 105, 285, { align: 'center' })

        if (showPreview) {
          const blob = pdf.output('blob')
          const url = URL.createObjectURL(blob)
          return { success: true, previewUrl: url, pdf, filename }
        } else {
          pdf.save(filename)
          return { success: true, previewUrl: '', pdf, filename }
        }
      } catch (error: any) {
        console.error('Error generando factura:', error)
        return { success: false, message: error?.message || 'Error generando factura' }
      }
    },

    downloadPdf,
    previewPdf
  }
}
