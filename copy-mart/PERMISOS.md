# Sistema de Permisos - CopyMart ERP

## 🎯 Descripción General

El sistema implementa control de acceso basado en **roles y departamentos**, permitiendo que diferentes usuarios vean y accedan solo a los módulos autorizados.

## 👥 Jerarquía de Roles

### 1. **Administrador** (Acceso Total)
- ✅ Puede ver TODOS los módulos
- ✅ Puede crear, editar y eliminar
- **Módulos disponibles:**
  - Dashboard
  - Ventas
  - Inventario
  - Clientes
  - Reportes
  - Usuarios

### 2. **Gerencia** (Acceso Limitado)
- ✅ Puede ver TODO menos Inventario
- ✅ Puede crear y editar
- ❌ No puede eliminar
- **Módulos disponibles:**
  - Dashboard
  - Ventas
  - Clientes
  - Reportes
  - Usuarios

### 3. **Usuario** (Acceso por Departamento)
- ❌ No puede crear, editar o eliminar
- ✅ Solo lectura
- **Módulos según departamento:**

#### 📋 Departamento: RH
- Dashboard
- Usuarios

#### 💼 Departamento: Administración
- Dashboard
- Ventas
- Inventario
- Reportes

#### 🛍️ Departamento: Comercial
- Dashboard
- Ventas
- Clientes
- Reportes

#### ⚙️ Departamento: Operaciones
- Dashboard
- Inventario

## 🔐 Usuarios de Prueba

Para probar el sistema, usa estas credenciales:

| Usuario | Email | Contraseña | Rol | Departamento | Módulos Visibles |
|---------|-------|------------|-----|--------------|------------------|
| Admin | `admin@copymart.com` | `admin123` | Administrador | Administración | Todos (6) |
| Gerente | `gerente@copymart.com` | `gerente123` | Gerencia | Comercial | 5 (sin Inventario) |
| Vendedor | `vendedor@copymart.com` | `vendedor123` | Usuario | Comercial | 4 módulos |
| Operador | `operador@copymart.com` | `operador123` | Usuario | Operaciones | 2 módulos |
| RH | `rh@copymart.com` | `rh123` | Usuario | RH | 2 módulos |

## 🛠️ Implementación Técnica

### Archivos Clave

1. **`composables/usePermissions.js`**
   - Gestiona la lógica de permisos
   - Define módulos accesibles por rol/departamento
   - Proporciona funciones para verificar accesos

2. **`router/index.js`**
   - Guards de navegación
   - Protege rutas según permisos
   - Redirige si no hay acceso

3. **`components/AppNavigation.vue`**
   - Muestra solo módulos permitidos
   - Se adapta dinámicamente al usuario

4. **`components/LoginForm.vue`**
   - Guarda datos del usuario
   - Establece permisos en el login

### Uso en Componentes

```javascript
import { usePermissions } from '@/composables/usePermissions'

export default {
  setup() {
    const { 
      canCreate,      // Permiso para crear
      canEdit,        // Permiso para editar
      canDelete,      // Permiso para eliminar
      isAdmin,        // Es administrador?
      isManager,      // Es gerente?
      userInfo        // Info del usuario actual
    } = usePermissions()
    
    return { canCreate, canEdit, canDelete, isAdmin, userInfo }
  }
}
```

### Ejemplo de Uso

```vue
<template>
  <!-- Mostrar botón solo si puede crear -->
  <button v-if="canCreate" @click="crearNuevo">
    Crear Nuevo
  </button>
  
  <!-- Mostrar info del usuario -->
  <div>{{ userInfo.name }} - {{ userInfo.rol }}</div>
</template>
```

## 🔄 Flujo de Autenticación

1. Usuario inicia sesión
2. Sistema valida credenciales
3. Se guarda información del usuario (rol y departamento)
4. Sistema calcula módulos accesibles
5. Navegación muestra solo módulos permitidos
6. Router bloquea acceso a rutas no autorizadas

## 🚀 Próximas Mejoras

- [ ] Integrar con API backend real
- [ ] Agregar más niveles de permisos granulares
- [ ] Implementar permisos a nivel de registro (solo ver propios datos)
- [ ] Agregar logs de auditoría de accesos
- [ ] Implementar tokens JWT con expiración

## 📝 Notas Importantes

- Los permisos se validan tanto en frontend como backend (cuando esté integrado)
- El menú de navegación se adapta automáticamente
- Las rutas están protegidas con guards
- El sistema es extensible para agregar más roles/departamentos
