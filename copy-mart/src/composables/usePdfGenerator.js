import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

export const usePdfGenerator = () => {
  
  // Función para generar PDF desde un elemento HTML con opción de vista previa
  const generatePdfFromElement = async (elementId, filename = 'documento.pdf', options = {}, showPreview = false) => {
    try {
      const element = document.getElementById(elementId)
      if (!element) {
        throw new Error(`Elemento con ID "${elementId}" no encontrado`)
      }

      // Configuraciones por defecto
      const defaultOptions = {
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

      if (showPreview) {
        // Mostrar vista previa en una nueva ventana
        const pdfBlob = pdf.output('blob')
        const pdfUrl = URL.createObjectURL(pdfBlob)
        return {
          success: true,
          message: 'Vista previa generada',
          previewUrl: pdfUrl,
          pdf: pdf,
          filename: filename
        }
      } else {
        // Descargar el PDF directamente
        pdf.save(filename)
        return {
          success: true,
          message: 'PDF generado exitosamente'
        }
      }
    } catch (error) {
      console.error('Error al generar PDF:', error)
      return {
        success: false,
        message: 'Error al generar el PDF: ' + error.message
      }
    }
  }

  // Función para generar PDF de reportes con vista previa
  const generateReportPdf = (data, reportType = 'general', filename = 'reporte.pdf', showPreview = false) => {
    try {
      const pdf = new jsPDF()
      
      // Configurar fuentes y colores
      pdf.setFont('helvetica')
      
      // Header del documento
      pdf.setFontSize(20)
      pdf.setTextColor(40, 40, 40)
      pdf.text('CopyMart ERP', 20, 30)
      
      pdf.setFontSize(16)
      pdf.text(`Reporte de ${getReportTitle(reportType)}`, 20, 45)
      
      // Fecha del reporte
      pdf.setFontSize(10)
      pdf.setTextColor(100, 100, 100)
      pdf.text(`Generado el: ${new Date().toLocaleDateString('es-ES')}`, 20, 55)
      
      // Línea separadora
      pdf.setDrawColor(200, 200, 200)
      pdf.line(20, 60, 190, 60)
      
      let yPosition = 75
      
      switch (reportType) {
        case 'ventas':
          yPosition = generateSalesReport(pdf, data, yPosition)
          break
        case 'inventario':
          yPosition = generateInventoryReport(pdf, data, yPosition)
          break
        case 'usuarios':
          yPosition = generateUsersReport(pdf, data, yPosition)
          break
        case 'clientes':
          yPosition = generateClientsReport(pdf, data, yPosition)
          break
        default:
          yPosition = generateGeneralReport(pdf, data, yPosition)
      }
      
      // Footer
      const pageCount = pdf.internal.getNumberOfPages()
      for (let i = 1; i <= pageCount; i++) {
        pdf.setPage(i)
        pdf.setFontSize(8)
        pdf.setTextColor(150, 150, 150)
        pdf.text(`Página ${i} de ${pageCount}`, 170, 285)
        pdf.text('CopyMart ERP - Sistema de Gestión', 20, 285)
      }
      
      if (showPreview) {
        // Mostrar vista previa
        const pdfBlob = pdf.output('blob')
        const pdfUrl = URL.createObjectURL(pdfBlob)
        return {
          success: true,
          message: 'Vista previa del reporte generada',
          previewUrl: pdfUrl,
          pdf: pdf,
          filename: filename
        }
      } else {
        // Descargar el PDF directamente
        pdf.save(filename)
        return {
          success: true,
          message: 'Reporte PDF generado exitosamente'
        }
      }
    } catch (error) {
      console.error('Error al generar reporte PDF:', error)
      return {
        success: false,
        message: 'Error al generar el reporte: ' + error.message
      }
    }
  }

  // Función para generar facturas/recibos con vista previa
  const generateInvoicePdf = (invoiceData, filename = 'factura.pdf', showPreview = false) => {
    try {
      const pdf = new jsPDF()
      
      // Header de la empresa
      pdf.setFontSize(18)
      pdf.setTextColor(40, 40, 40)
      pdf.text('CopyMart', 20, 30)
      
      pdf.setFontSize(10)
      pdf.text('Servicios de Copiado e Impresión', 20, 38)
      pdf.text('RFC: COPY123456789', 20, 45)
      pdf.text('Tel: +52 55 1234-5678', 20, 52)
      
      // Datos de la factura
      pdf.setFontSize(14)
      pdf.text('FACTURA', 150, 30)
      
      pdf.setFontSize(10)
      pdf.text(`Folio: ${invoiceData.folio || 'F-' + Date.now()}`, 150, 40)
      pdf.text(`Fecha: ${invoiceData.fecha || new Date().toLocaleDateString('es-ES')}`, 150, 47)
      
      // Datos del cliente
      pdf.setFontSize(12)
      pdf.text('FACTURAR A:', 20, 70)
      pdf.setFontSize(10)
      pdf.text(invoiceData.cliente.nombre, 20, 80)
      pdf.text(invoiceData.cliente.email, 20, 87)
      if (invoiceData.cliente.telefono) {
        pdf.text(invoiceData.cliente.telefono, 20, 94)
      }
      
      // Tabla de productos/servicios
      let yPos = 110
      
      // Headers de la tabla
      pdf.setFillColor(240, 240, 240)
      pdf.rect(20, yPos, 170, 10, 'F')
      
      pdf.setFontSize(9)
      pdf.setTextColor(40, 40, 40)
      pdf.text('Descripción', 25, yPos + 7)
      pdf.text('Cantidad', 110, yPos + 7)
      pdf.text('Precio Unit.', 135, yPos + 7)
      pdf.text('Total', 165, yPos + 7)
      
      yPos += 15
      
      // Items
      let subtotal = 0
      invoiceData.items.forEach((item, index) => {
        const total = item.cantidad * item.precio
        subtotal += total
        
        pdf.text(item.descripcion, 25, yPos)
        pdf.text(item.cantidad.toString(), 115, yPos)
        pdf.text(`$${item.precio.toFixed(2)}`, 140, yPos)
        pdf.text(`$${total.toFixed(2)}`, 165, yPos)
        
        yPos += 10
        
        // Nueva página si es necesario
        if (yPos > 250) {
          pdf.addPage()
          yPos = 30
        }
      })
      
      // Totales
      yPos += 10
      pdf.line(20, yPos, 190, yPos)
      yPos += 10
      
      const iva = subtotal * 0.16
      const total = subtotal + iva
      
      pdf.setFontSize(10)
      pdf.text(`Subtotal: $${subtotal.toFixed(2)}`, 140, yPos)
      pdf.text(`IVA (16%): $${iva.toFixed(2)}`, 140, yPos + 7)
      
      pdf.setFontSize(12)
      pdf.setFont('helvetica', 'bold')
      pdf.text(`Total: $${total.toFixed(2)}`, 140, yPos + 17)
      
      // Método de pago
      if (invoiceData.metodoPago) {
        pdf.setFont('helvetica', 'normal')
        pdf.setFontSize(9)
        pdf.text(`Método de pago: ${invoiceData.metodoPago}`, 20, yPos + 20)
      }
      
      if (showPreview) {
        // Mostrar vista previa
        const pdfBlob = pdf.output('blob')
        const pdfUrl = URL.createObjectURL(pdfBlob)
        return {
          success: true,
          message: 'Vista previa de factura generada',
          previewUrl: pdfUrl,
          pdf: pdf,
          filename: filename
        }
      } else {
        // Descargar el PDF directamente
        pdf.save(filename)
        return {
          success: true,
          message: 'Factura generada exitosamente'
        }
      }
    } catch (error) {
      console.error('Error al generar factura:', error)
      return {
        success: false,
        message: 'Error al generar la factura: ' + error.message
      }
    }
  }

  // Función para descargar un PDF desde su objeto
  const downloadPdf = (pdf, filename) => {
    try {
      pdf.save(filename)
      return {
        success: true,
        message: 'PDF descargado exitosamente'
      }
    } catch (error) {
      return {
        success: false,
        message: 'Error al descargar el PDF: ' + error.message
      }
    }
  }

  // Funciones auxiliares para diferentes tipos de reportes
  const getReportTitle = (reportType) => {
    const titles = {
      ventas: 'Ventas',
      inventario: 'Inventario',
      usuarios: 'Usuarios',
      clientes: 'Clientes',
      general: 'General'
    }
    return titles[reportType] || 'General'
  }

  const generateSalesReport = (pdf, data, yPosition) => {
    pdf.setFontSize(12)
    pdf.setTextColor(40, 40, 40)
    pdf.text('Resumen de Ventas', 20, yPosition)
    
    yPosition += 15
    
    // Headers de tabla
    pdf.setFontSize(9)
    pdf.text('Fecha', 25, yPosition)
    pdf.text('Cliente', 60, yPosition)
    pdf.text('Producto', 100, yPosition)
    pdf.text('Cantidad', 140, yPosition)
    pdf.text('Total', 170, yPosition)
    
    yPosition += 10
    pdf.line(20, yPosition, 190, yPosition)
    yPosition += 5
    
    // Datos
    data.forEach((venta, index) => {
      pdf.text(venta.fecha || '', 25, yPosition)
      pdf.text(venta.cliente || '', 60, yPosition)
      pdf.text(venta.producto || '', 100, yPosition)
      pdf.text(venta.cantidad?.toString() || '', 140, yPosition)
      pdf.text(`$${venta.total || 0}`, 170, yPosition)
      yPosition += 8
      
      if (yPosition > 250) {
        pdf.addPage()
        yPosition = 30
      }
    })
    
    return yPosition
  }

  const generateInventoryReport = (pdf, data, yPosition) => {
    pdf.setFontSize(12)
    pdf.text('Estado del Inventario', 20, yPosition)
    
    yPosition += 15
    
    pdf.setFontSize(9)
    pdf.text('Producto', 25, yPosition)
    pdf.text('SKU', 80, yPosition)
    pdf.text('Stock', 120, yPosition)
    pdf.text('Stock Mín.', 145, yPosition)
    pdf.text('Estado', 170, yPosition)
    
    yPosition += 10
    pdf.line(20, yPosition, 190, yPosition)
    yPosition += 5
    
    data.forEach((item, index) => {
      pdf.text(item.nombre || '', 25, yPosition)
      pdf.text(item.sku || '', 80, yPosition)
      pdf.text(item.stock?.toString() || '', 125, yPosition)
      pdf.text(item.stockMinimo?.toString() || '', 150, yPosition)
      
      const estado = item.stock <= item.stockMinimo ? 'Bajo' : 'OK'
      pdf.setTextColor(item.stock <= item.stockMinimo ? 255 : 0, 0, 0)
      pdf.text(estado, 175, yPosition)
      pdf.setTextColor(40, 40, 40)
      
      yPosition += 8
      
      if (yPosition > 250) {
        pdf.addPage()
        yPosition = 30
      }
    })
    
    return yPosition
  }

  const generateUsersReport = (pdf, data, yPosition) => {
    pdf.setFontSize(12)
    pdf.text('Lista de Usuarios', 20, yPosition)
    
    yPosition += 15
    
    pdf.setFontSize(9)
    pdf.text('Nombre', 25, yPosition)
    pdf.text('Email', 80, yPosition)
    pdf.text('Rol', 130, yPosition)
    pdf.text('Estado', 160, yPosition)
    
    yPosition += 10
    pdf.line(20, yPosition, 190, yPosition)
    yPosition += 5
    
    data.forEach((user, index) => {
      pdf.text(user.name || '', 25, yPosition)
      pdf.text(user.email || '', 80, yPosition)
      pdf.text(user.role || '', 130, yPosition)
      pdf.text(user.status || '', 160, yPosition)
      yPosition += 8
      
      if (yPosition > 250) {
        pdf.addPage()
        yPosition = 30
      }
    })
    
    return yPosition
  }

  const generateClientsReport = (pdf, data, yPosition) => {
    pdf.setFontSize(12)
    pdf.text('Lista de Clientes', 20, yPosition)
    
    yPosition += 15
    
    pdf.setFontSize(9)
    pdf.text('Nombre', 25, yPosition)
    pdf.text('Email', 80, yPosition)
    pdf.text('Teléfono', 130, yPosition)
    pdf.text('Total Compras', 165, yPosition)
    
    yPosition += 10
    pdf.line(20, yPosition, 190, yPosition)
    yPosition += 5
    
    data.forEach((cliente, index) => {
      pdf.text(cliente.nombre || '', 25, yPosition)
      pdf.text(cliente.email || '', 80, yPosition)
      pdf.text(cliente.telefono || '', 130, yPosition)
      pdf.text(`$${cliente.totalCompras || 0}`, 165, yPosition)
      yPosition += 8
      
      if (yPosition > 250) {
        pdf.addPage()
        yPosition = 30
      }
    })
    
    return yPosition
  }

  const generateGeneralReport = (pdf, data, yPosition) => {
    pdf.setFontSize(12)
    pdf.text('Reporte General', 20, yPosition)
    
    yPosition += 15
    
    if (Array.isArray(data)) {
      data.forEach((item, index) => {
        pdf.setFontSize(9)
        pdf.text(`${index + 1}. ${JSON.stringify(item)}`, 25, yPosition)
        yPosition += 8
        
        if (yPosition > 250) {
          pdf.addPage()
          yPosition = 30
        }
      })
    } else {
      pdf.setFontSize(9)
      pdf.text(JSON.stringify(data, null, 2), 25, yPosition)
    }
    
    return yPosition
  }

  return {
    generatePdfFromElement,
    generateReportPdf,
    generateInvoicePdf,
    downloadPdf
  }
}