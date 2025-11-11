import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import { usePermissions } from '../composables/usePermissions'

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
      component: () => import('../views/VentasView.vue'),
      meta: { 
        requiresAuth: true,
        requiredModule: 'ventas',
        title: 'Ventas - CopyMart ERP'
      }
    },
    {
      path: '/inventario',
      name: 'Inventario',
      component: () => import('../views/InventarioView.vue'),
      meta: { 
        requiresAuth: true,
        requiredModule: 'inventario',
        title: 'Inventario - CopyMart ERP'
      }
    },
    {
      path: '/clientes',
      name: 'Clientes',
      component: () => import('../views/ClientesView.vue'),
      meta: { 
        requiresAuth: true,
        requiredModule: 'clientes',
        title: 'Clientes - CopyMart ERP'
      }
    },
    {
      path: '/usuarios',
      name: 'Usuarios',
      component: () => import('../views/UsuariosView.vue'),
      meta: { 
        requiresAuth: true,
        requiredModule: 'usuarios',
        title: 'Usuarios - CopyMart ERP'
      }
    },
    {
      path: '/reportes',
      name: 'Reportes',
      component: () => import('../views/ReportesView.vue'),
      meta: { 
        requiresAuth: true,
        requiredModule: 'reportes',
        title: 'Reportes - CopyMart ERP'
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

// Guard de navegación para autenticación y permisos
router.beforeEach((to, from, next) => {
  // Cambiar el título de la página
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Verificar autenticación
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  
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
})

export default router
