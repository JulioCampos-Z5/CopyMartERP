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
    return new Promise((resolve, reject) => {
      try {
        // Crear elemento HTML para la factura
        const invoiceHtml = document.createElement('div')
        invoiceHtml.id = 'invoice-html-temp'
        invoiceHtml.style.cssText = 'width: 210mm; height: 297mm; padding: 15mm; background: white; font-family: Arial, sans-serif; position: absolute; left: -9999px; box-sizing: border-box;'
        
        const iva = invoiceData.items.reduce((sum, item) => sum + (item.cantidad * item.precio), 0) * 0.16
        const subtotal = invoiceData.items.reduce((sum, item) => sum + (item.cantidad * item.precio), 0)
        const total = subtotal + iva
        
        invoiceHtml.innerHTML = `
          <style>
            body { margin: 0; padding: 0; }
            .invoice-container { font-size: 11px; color: #333; }
            .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
            .company-info h1 { margin: 0; font-size: 24px; color: #1f4e0e; font-weight: bold; }
            .company-info p { margin: 2px 0; font-size: 9px; color: #666; }
            .factura-title { text-align: right; }
            .factura-title h2 { margin: 0; font-size: 16px; color: #1f4e0e; }
            .factura-number { background: #1f4e0e; color: white; padding: 5px 10px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 5px; }
            
            .section-title { background: #1f4e0e; color: white; padding: 6px 8px; font-weight: bold; font-size: 10px; margin-top: 12px; margin-bottom: 8px; }
            
            .emisor-receptor { display: flex; gap: 20px; margin-bottom: 15px; }
            .emisor, .receptor { flex: 1; font-size: 9px; line-height: 1.5; }
            .emisor-title, .receptor-title { background: #1f4e0e; color: white; padding: 4px 6px; font-weight: bold; font-size: 10px; margin-bottom: 6px; }
            .field-label { font-weight: bold; color: #333; margin-top: 4px; }
            .field-value { color: #555; margin-left: 0; }
            
            .datos-table { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
            .datos-table td { padding: 4px 6px; font-size: 9px; border: none; }
            .datos-label { font-weight: bold; width: 30%; }
            .datos-value { color: #555; }
            
            .items-table { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
            .items-table thead tr { background: #1f4e0e; color: white; }
            .items-table th { padding: 6px 4px; text-align: left; font-weight: bold; font-size: 9px; border: 1px solid #1f4e0e; }
            .items-table td { padding: 5px 4px; font-size: 9px; border: 1px solid #ddd; }
            .items-table th:last-child, .items-table td:last-child { text-align: right; }
            
            .objeto-impuesto { font-size: 9px; color: #666; margin-bottom: 10px; }
            
            .totales { text-align: right; margin-top: 15px; }
            .total-line { font-size: 9px; margin-bottom: 4px; }
            .total-line-label { display: inline-block; width: 120px; text-align: left; }
            .total-line-value { display: inline-block; width: 80px; text-align: right; font-weight: normal; }
            .total-box { background: #1f4e0e; color: white; padding: 7px 10px; font-weight: bold; font-size: 11px; display: inline-block; min-width: 180px; text-align: center; margin-top: 6px; }
          </style>
          
          <div class="invoice-container">
            <!-- HEADER -->
            <div class="header">
              <div class="company-info">
                <h1>COPYMART</h1>
                <p>Servicios de Copiado e Impresión</p>
              </div>
              <div class="factura-title">
                <h2>Factura</h2>
                <div class="factura-number">- ${invoiceData.folio || 'F-001'}</div>
              </div>
            </div>
            
            <!-- EMISOR Y RECEPTOR -->
            <div class="emisor-receptor">
              <div class="emisor">
                <div class="emisor-title">EMISOR</div>
                <div>
                  <div class="field-label">Razón Social:</div>
                  <div class="field-value">COPYMART SOLUTIONS</div>
                  <div class="field-label" style="margin-top: 6px;">RFC:</div>
                  <div class="field-value">CCS161115L51</div>
                  <div class="field-label" style="margin-top: 6px;">Domicilio:</div>
                  <div class="field-value">Paseo Solares 555, Col. Solares</div>
                </div>
              </div>
              <div class="receptor">
                <div class="receptor-title">RECEPTOR</div>
                <div>
                  <div class="field-label">Razón Social:</div>
                  <div class="field-value">${invoiceData.cliente?.nombre || 'Cliente'}</div>
                  <div class="field-label" style="margin-top: 6px;">RFC:</div>
                  <div class="field-value">${invoiceData.cliente?.rfc || 'N/A'}</div>
                  <div class="field-label" style="margin-top: 6px;">Domicilio:</div>
                  <div class="field-value">${invoiceData.cliente?.domicilio || 'N/A'}</div>
                </div>
              </div>
            </div>
            
            <!-- DATOS GENERALES -->
            <div class="section-title">DATOS GENERALES</div>
            <table class="datos-table">
              <tr>
                <td class="datos-label">Fecha de Expedición:</td>
                <td class="datos-value">${invoiceData.fecha || new Date().toLocaleDateString('es-MX')}</td>
                <td class="datos-label" style="text-align: right; padding-right: 40px;">Moneda:</td>
                <td class="datos-value">MXN</td>
              </tr>
              <tr>
                <td class="datos-label">Folio Interno:</td>
                <td class="datos-value">${invoiceData.folio || 'F-001'}</td>
                <td class="datos-label" style="text-align: right; padding-right: 40px;">Método de Pago:</td>
                <td class="datos-value">${invoiceData.metodoPago || 'Por definir'}</td>
              </tr>
            </table>
            
            <!-- TABLA DE DETALLES -->
            <div class="section-title">DETALLES</div>
            <table class="items-table">
              <thead>
                <tr>
                  <th>Cantidad</th>
                  <th>Descripción</th>
                  <th>C. Prod/Serv</th>
                  <th>Unidad</th>
                  <th>P. Unitario</th>
                  <th>Importe</th>
                </tr>
              </thead>
              <tbody>
                ${invoiceData.items.map(item => `
                  <tr>
                    <td style="text-align: center;">${item.cantidad || 1}</td>
                    <td>${(item.descripcion || 'Equipo').substring(0, 35)}</td>
                    <td style="text-align: center;">${item.cProds || '84721900'}</td>
                    <td style="text-align: center;">${item.unidad || 'Pieza'}</td>
                    <td style="text-align: right;">$ ${(item.precio || 0).toFixed(2)}</td>
                    <td style="text-align: right;">$ ${((item.cantidad || 1) * (item.precio || 0)).toFixed(2)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
            
            <div class="objeto-impuesto">Si objeto de impuesto.</div>
            
            <!-- TOTALES -->
            <div class="totales">
              <div class="total-line">
                <span class="total-line-label">SUBTOTAL:</span>
                <span class="total-line-value">$ ${subtotal.toFixed(2)}</span>
              </div>
              <div class="total-line">
                <span class="total-line-label">+ IVA (16%):</span>
                <span class="total-line-value">$ ${iva.toFixed(2)}</span>
              </div>
              <div class="total-box">
                TOTAL: $ ${total.toFixed(2)}
              </div>
            </div>
          </div>
        `
        
        document.body.appendChild(invoiceHtml)
        
        // Convertir a PDF usando html2canvas
        html2canvas(invoiceHtml, {
          scale: 2,
          useCORS: true,
          allowTaint: true,
          backgroundColor: '#ffffff'
        }).then(canvas => {
          const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
          const imgData = canvas.toDataURL('image/png')
          const imgWidth = 210
          const pageHeight = 295
          const imgHeight = (canvas.height * imgWidth) / canvas.width
          
          let heightLeft = imgHeight
          let position = 0
          
          pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
          heightLeft -= pageHeight
          
          while (heightLeft >= 0) {
            position = heightLeft - imgHeight
            pdf.addPage()
            pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
            heightLeft -= pageHeight
          }
          
          document.body.removeChild(invoiceHtml)
          
          if (showPreview) {
            const pdfBlob = pdf.output('blob')
            const pdfUrl = URL.createObjectURL(pdfBlob)
            resolve({
              success: true,
              message: 'Vista previa de factura generada',
              previewUrl: pdfUrl,
              pdf: pdf,
              filename: filename
            })
          } else {
            pdf.save(filename)
            resolve({
              success: true,
              message: 'Factura generada exitosamente'
            })
          }
        }).catch(error => {
          if (document.body.contains(invoiceHtml)) {
            document.body.removeChild(invoiceHtml)
          }
          console.error('Error al generar factura:', error)
          reject({
            success: false,
            message: 'Error al generar la factura: ' + error.message
          })
        })
      } catch (error) {
        console.error('Error al generar factura:', error)
        reject({
          success: false,
          message: 'Error al generar la factura: ' + error.message
        })
      }
    })
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