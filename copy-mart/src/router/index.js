import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: to => {
        const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
        const hasToken = !!localStorage.getItem('token')
        return (isAuthenticated && hasToken) ? '/dashboard' : '/login'
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: { 
        requiresAuth: false,
        title: 'Iniciar Sesión - CopyMart ERP'
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: DashboardView,
      meta: { 
        requiresAuth: true,
        title: 'Dashboard - CopyMart ERP'
      }
    },
    // Rutas del área Comercial
    {
      path: '/ventas',
      name: 'Ventas',
      component: () => import('../views/Comercial/ventas/VentasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Ventas - CopyMart ERP'
      }
    },
    {
      path: '/comercial/ventas/nueva',
      name: 'VentaNueva',
      component: () => import('../views/Comercial/ventas/VentaFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nueva Venta - CopyMart ERP'
      }
    },
    {
      path: '/comercial/ventas/:id',
      name: 'VentaDetalle',
      component: () => import('../views/Comercial/ventas/VentaDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle de Venta - CopyMart ERP'
      }
    },
    {
      path: '/comercial/ventas/editar/:id',
      name: 'VentaEditar',
      component: () => import('../views/Comercial/ventas/VentaFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Venta - CopyMart ERP'
      }
    },
    {
      path: '/rentas',
      name: 'Rentas',
      component: () => import('../views/Comercial/rentas/RentasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Rentas - CopyMart ERP'
      }
    },
    {
      path: '/comercial/rentas/nueva',
      name: 'RentaNueva',
      component: () => import('../views/Comercial/rentas/RentaFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nueva Renta - CopyMart ERP'
      }
    },
    {
      path: '/comercial/rentas/:id',
      name: 'RentaDetalle',
      component: () => import('../views/Comercial/rentas/RentaDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle de Renta - CopyMart ERP'
      }
    },
    {
      path: '/comercial/rentas/editar/:id',
      name: 'RentaEditar',
      component: () => import('../views/Comercial/rentas/RentaFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Renta - CopyMart ERP'
      }
    },
    {
      path: '/atencion-clientes',
      name: 'AtencionClientes',
      component: () => import('../views/Comercial/AtencionClientesView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Atención a Clientes - CopyMart ERP'
      }
    },
    {
      path: '/clientes',
      name: 'Clientes',
      component: () => import('../views/Comercial/clientes/ClientesView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Clientes - CopyMart ERP'
      }
    },
    {
      path: '/comercial/clientes/nuevo',
      name: 'ClienteNuevo',
      component: () => import('../views/Comercial/clientes/ClienteFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nuevo Cliente - CopyMart ERP'
      }
    },
    {
      path: '/comercial/clientes/:id',
      name: 'ClienteDetalle',
      component: () => import('../views/Comercial/clientes/ClienteDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle del Cliente - CopyMart ERP'
      }
    },
    {
      path: '/comercial/clientes/editar/:id',
      name: 'ClienteEditar',
      component: () => import('../views/Comercial/clientes/ClienteFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Cliente - CopyMart ERP'
      }
    },
    {
      path: '/produccion',
      name: 'Produccion',
      component: () => import('../views/Comercial/ProduccionView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Producción - CopyMart ERP'
      }
    },
    // Rutas del área Administración
    {
      path: '/compras',
      name: 'Compras',
      component: () => import('../views/Administracion/compras/ComprasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Compras - CopyMart ERP'
      }
    },
    {
      path: '/administracion/compras/nueva',
      name: 'CompraNueva',
      component: () => import('../views/Administracion/compras/CompraFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nueva Compra - CopyMart ERP'
      }
    },
    {
      path: '/administracion/compras/:id',
      name: 'CompraDetalle',
      component: () => import('../views/Administracion/compras/CompraDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle de Compra - CopyMart ERP'
      }
    },
    {
      path: '/administracion/compras/editar/:id',
      name: 'CompraEditar',
      component: () => import('../views/Administracion/compras/CompraFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Compra - CopyMart ERP'
      }
    },
    {
      path: '/almacen',
      name: 'Almacen',
      component: () => import('../views/Administracion/AlmacenView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Control de Almacén - CopyMart ERP'
      }
    },
    {
      path: '/cobranza',
      name: 'Cobranza',
      component: () => import('../views/Administracion/CobranzaView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Cobranza - CopyMart ERP'
      }
    },
    {
      path: '/facturacion',
      name: 'Facturacion',
      component: () => import('../views/Administracion/facturacion/FacturacionView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Sistema de Facturación - CopyMart ERP'
      }
    },
    {
      path: '/administracion/facturacion/nueva',
      name: 'FacturacionNueva',
      component: () => import('../views/Administracion/facturacion/FacturacionFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nueva Factura - CopyMart ERP'
      }
    },
    {
      path: '/administracion/facturacion/:id',
      name: 'FacturacionDetalle',
      component: () => import('../views/Administracion/facturacion/FacturacionDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle de Factura - CopyMart ERP'
      }
    },
    {
      path: '/administracion/facturacion/editar/:id',
      name: 'FacturacionEditar',
      component: () => import('../views/Administracion/facturacion/FacturacionFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Factura - CopyMart ERP'
      }
    },
    {
      path: '/inventario',
      name: 'Inventario',
      component: () => import('../views/Administracion/equipos/InventarioView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Inventario - CopyMart ERP'
      }
    },
    {
      path: '/administracion/equipos/nuevo',
      name: 'EquipoNuevo',
      component: () => import('../views/Administracion/equipos/EquipoFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nuevo Equipo - CopyMart ERP'
      }
    },
    {
      path: '/administracion/equipos/:id',
      name: 'EquipoDetalle',
      component: () => import('../views/Administracion/equipos/EquipoDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle del Equipo - CopyMart ERP'
      }
    },
    {
      path: '/administracion/equipos/editar/:id',
      name: 'EquipoEditar',
      component: () => import('../views/Administracion/equipos/EquipoFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Equipo - CopyMart ERP'
      }
    },
    {
      path: '/administracion/refacciones/nueva',
      name: 'RefaccionNueva',
      component: () => import('../views/Administracion/refacciones/RefaccionFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nueva Refacción - CopyMart ERP'
      }
    },
    {
      path: '/administracion/refacciones/:id',
      name: 'RefaccionDetalle',
      component: () => import('../views/Administracion/refacciones/RefaccionDetailView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Detalle de Refacción - CopyMart ERP'
      }
    },
    {
      path: '/administracion/refacciones/editar/:id',
      name: 'RefaccionEditar',
      component: () => import('../views/Administracion/refacciones/RefaccionFormView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Editar Refacción - CopyMart ERP'
      }
    },
    // Ruta de Recursos Humanos
    {
      path: '/recursos-humanos',
      name: 'RecursosHumanos',
      component: () => import('../views/RecursosHumanos/RHView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Recursos Humanos - CopyMart ERP'
      }
    },
    {
      path: '/recursos-humanos/empleados',
      name: 'Empleados',
      component: () => import('../views/RecursosHumanos/EmpleadosView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Empleados - CopyMart ERP'
      }
    },
    {
      path: '/recursos-humanos/nominas',
      name: 'Nominas',
      component: () => import('../views/RecursosHumanos/NominasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Nóminas - CopyMart ERP'
      }
    },
    {
      path: '/recursos-humanos/vacaciones',
      name: 'Vacaciones',
      component: () => import('../views/RecursosHumanos/VacacionesView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Vacaciones - CopyMart ERP'
      }
    },
    {
      path: '/recursos-humanos/areas',
      name: 'Areas',
      component: () => import('../views/RecursosHumanos/AreasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Áreas - CopyMart ERP'
      }
    },    // Rutas del área Operaciones
    {
      path: '/rutas',
      name: 'Rutas',
      component: () => import('../views/Operaciones/RutasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Rutas - CopyMart ERP'
      }
    },
    {
      path: '/ordenes-servicio',
      name: 'OrdenesServicio',
      component: () => import('../views/Operaciones/OrdenesServicioView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Órdenes de Servicio - CopyMart ERP'
      }
    },
    // Ruta de Tecnologías de la Información
    {
      path: '/ti',
      name: 'TecnologiasInformacion',
      component: () => import('../views/TecnologiasInformacion/TIView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Tecnologías de la Información - CopyMart ERP'
      }
    },
    {
      path: '/perfil',
      name: 'Perfil',
      component: () => import('../views/PerfilView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Mi Perfil - CopyMart ERP'
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      redirect: '/dashboard'
    }
  ],
})

// Guard de navegación para autenticación
router.beforeEach((to, from, next) => {
  // Cambiar el título de la página
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Verificar autenticación
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  const hasToken = !!localStorage.getItem('token')
  
  // Usuario está autenticado si tiene ambos
  const userLoggedIn = isAuthenticated && hasToken
  
  // Si la ruta requiere autenticación y no está autenticado
  if (to.meta.requiresAuth && !userLoggedIn) {
    // Guardar la ruta a la que intentaba acceder
    sessionStorage.setItem('redirectAfterLogin', to.fullPath)
    // Redirigir al login
    next('/login')
  } 
  // Si intenta ir al login estando ya autenticado
  else if (to.path === '/login' && userLoggedIn) {
    // Redirigir al dashboard
    next('/dashboard')
  } 
  // Si no requiere autenticación o está autenticado
  else {
    next()
  }
})

export default router
