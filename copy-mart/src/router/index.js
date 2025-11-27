import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
<<<<<<< HEAD
import { usePermissions } from '../composables/usePermissions'
=======
>>>>>>> develop

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
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
    {
      path: '/ventas',
      name: 'Ventas',
<<<<<<< HEAD
      component: () => import('../views/VentasView.vue'),
      meta: { 
        requiresAuth: true,
        requiredModule: 'ventas',
=======
      component: () => import('../views/Comercial/VentasView.vue'),
      meta: { 
        requiresAuth: true,
>>>>>>> develop
        title: 'Ventas - CopyMart ERP'
      }
    },
    {
      path: '/inventario',
      name: 'Inventario',
      component: () => import('../views/InventarioView.vue'),
      meta: { 
        requiresAuth: true,
<<<<<<< HEAD
        requiredModule: 'inventario',
=======
>>>>>>> develop
        title: 'Inventario - CopyMart ERP'
      }
    },
    {
      path: '/clientes',
      name: 'Clientes',
      component: () => import('../views/ClientesView.vue'),
      meta: { 
        requiresAuth: true,
<<<<<<< HEAD
        requiredModule: 'clientes',
=======
>>>>>>> develop
        title: 'Clientes - CopyMart ERP'
      }
    },
    {
      path: '/usuarios',
      name: 'Usuarios',
      component: () => import('../views/UsuariosView.vue'),
      meta: { 
        requiresAuth: true,
<<<<<<< HEAD
        requiredModule: 'usuarios',
=======
>>>>>>> develop
        title: 'Usuarios - CopyMart ERP'
      }
    },
    {
      path: '/reportes',
      name: 'Reportes',
      component: () => import('../views/ReportesView.vue'),
      meta: { 
        requiresAuth: true,
<<<<<<< HEAD
        requiredModule: 'reportes',
        title: 'Reportes - CopyMart ERP'
      }
    },
=======
        title: 'Reportes - CopyMart ERP'
      }
    },
    // Rutas del área Comercial
    {
      path: '/rentas',
      name: 'Rentas',
      component: () => import('../views/Comercial/RentasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Rentas - CopyMart ERP'
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
    // Rutas del área Administración
    {
      path: '/compras',
      name: 'Compras',
      component: () => import('../views/Administracion/ComprasView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Gestión de Compras - CopyMart ERP'
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
      component: () => import('../views/Administracion/FacturacionView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Sistema de Facturación - CopyMart ERP'
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
    // Rutas del área Operaciones
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
>>>>>>> develop
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

<<<<<<< HEAD
// Guard de navegación para autenticación y permisos
=======
// Guard de navegación para autenticación
>>>>>>> develop
router.beforeEach((to, from, next) => {
  // Cambiar el título de la página
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Verificar autenticación
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
<<<<<<< HEAD
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirigir al login si la ruta requiere autenticación
    next('/login')
    return
  }
  
  if (to.name === 'Login' && isAuthenticated) {
    // Redirigir al dashboard si ya está autenticado
    next('/dashboard')
    return
  }
  
  // Verificar permisos de módulo si la ruta lo requiere
  if (to.meta.requiredModule && isAuthenticated) {
    const { canAccessModule } = usePermissions()
    
    if (!canAccessModule(to.meta.requiredModule)) {
      // Si no tiene permisos, redirigir al dashboard con mensaje
      console.warn(`Acceso denegado al módulo: ${to.meta.requiredModule}`)
      next('/dashboard')
      return
    }
  }
  
  next()
=======
  const hasToken = !!localStorage.getItem('token')
  
  // Usuario está autenticado si tiene ambos
  const userLoggedIn = isAuthenticated && hasToken
  
  if (to.meta.requiresAuth && !userLoggedIn) {
    // Redirigir al login si la ruta requiere autenticación y no está autenticado
    next('/login')
  } else if (to.path === '/login' && userLoggedIn) {
    // Redirigir al dashboard si intenta ir al login estando ya autenticado
    next('/dashboard')
  } else {
    next()
  }
>>>>>>> develop
})

export default router
