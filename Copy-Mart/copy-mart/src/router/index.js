import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

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
        title: 'Ventas - CopyMart ERP'
      }
    },
    {
      path: '/inventario',
      name: 'Inventario',
      component: () => import('../views/InventarioView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Inventario - CopyMart ERP'
      }
    },
    {
      path: '/clientes',
      name: 'Clientes',
      component: () => import('../views/ClientesView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Clientes - CopyMart ERP'
      }
    },
    {
      path: '/reportes',
      name: 'Reportes',
      component: () => import('../views/ReportesView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Reportes - CopyMart ERP'
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
  
  // Verificar autenticación (en una app real, verificarías el token/estado de auth)
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirigir al login si la ruta requiere autenticación
    next('/login')
  } else if (to.name === 'Login' && isAuthenticated) {
    // Redirigir al dashboard si ya está autenticado
    next('/dashboard')
  } else {
    next()
  }
})

export default router
