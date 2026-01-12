# Arquitectura TypeScript + Pinia Implementada

## ✅ Configuración Base

### 1. TypeScript
- ✅ `tsconfig.json` configurado con modo gradual
- ✅ `tsconfig.node.json` para Vite
- ✅ `env.d.ts` con declaraciones de módulos
- ✅ Vite configurado para soportar `.ts` files

### 2. Tipos Centralizados (`src/types/index.ts`)
- ✅ Tipos base: `PaginationParams`, `PaginatedResponse`, `ApiError`
- ✅ Tipos de dominio: `Purchase`, `Billing`, `Client`, `Sparepart`, `Equipment`, etc.
- ✅ Tipos de filtros: `PurchaseFilters`, `BillingFilters`, etc.
- ✅ Tipos de auth: `User`, `LoginCredentials`, `AuthResponse`

### 3. API Config TypeScript (`src/config/api.ts`)
- ✅ Cliente Axios tipado
- ✅ Interceptores con tipos
- ✅ Helpers tipados: `apiGet`, `apiPost`, `apiPut`, `apiPatch`, `apiDelete`
- ✅ `buildUrlWithParams` con tipos

### 4. Stores con Pinia

#### `auth.ts` - Autenticación
```typescript
const authStore = useAuthStore()

// Estado
authStore.user
authStore.isAuthenticated
authStore.token

// Getters
authStore.userName
authStore.userRole
authStore.userPermissions

// Actions
await authStore.login({ username, password })
authStore.logout()
authStore.hasPermission('compras:create')
authStore.hasAnyPermission(['compras:create', 'compras:edit'])
```

#### `filters.ts` - Filtros y Paginación
```typescript
const filtersStore = useFiltersStore()

// Obtener configuración para petición
const config = filtersStore.getRequestConfig('purchases')

// Actualizar filtros
filtersStore.setFilter('purchases', 'status', 'En Curso')
filtersStore.setFilters('purchases', { status: 'En Curso', type: 'Interna' })

// Paginación
filtersStore.setPage('purchases', 2)
filtersStore.setPageSize('purchases', 20)

// Limpiar
filtersStore.clearFilters('purchases')
```

### 5. Services TypeScript

#### `purchaseService.ts`
```typescript
import type { Purchase, PurchaseCreate, PurchaseFilters, PaginatedResponse } from '@/types'

const response = await purchaseService.getPurchases({
  page: 1,
  pageSize: 10,
  status: 'En Curso',
  startDate: '2026-01-01'
})
// response es tipo PaginatedResponse<Purchase>

const purchase = await purchaseService.getPurchaseById(1)
// purchase es tipo Purchase
```

#### `billingService.ts`
Similar a purchaseService con todos los métodos tipados

## 📋 Próximos Pasos

### 1. Refactorizar Vistas (Ejemplo: ComprasView)

**ANTES (sin stores):**
```vue
<script setup>
import { ref, onMounted } from 'vue'
import { purchaseService } from '@/services/purchaseService'

const filters = ref({ status: '', type: '' })
const pagination = ref({ page: 1, page_size: 10 })

const loadPurchases = async () => {
  const response = await purchaseService.getPurchases({
    ...filters.value,
    ...pagination.value
  })
  // ...
}
</script>
```

**DESPUÉS (con stores):**
```vue
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFiltersStore } from '@/stores/filters'
import { purchaseService } from '@/services/purchaseService.ts'
import type { Purchase } from '@/types'

const authStore = useAuthStore()
const filtersStore = useFiltersStore()

const purchases = ref<Purchase[]>([])
const loading = ref(false)

// Computed desde store
const filters = computed(() => filtersStore.getFilters('purchases'))
const pagination = computed(() => filtersStore.getPagination('purchases'))

const loadPurchases = async () => {
  loading.value = true
  try {
    const config = filtersStore.getRequestConfig('purchases')
    const response = await purchaseService.getPurchases(config)
    
    purchases.value = response.items
    filtersStore.setPagination('purchases', {
      total: response.total,
      total_pages: response.total_pages
    })
  } finally {
    loading.value = false
  }
}

// Permisos
const canCreate = computed(() => authStore.hasPermission('compras:create'))
</script>
```

### 2. Crear más services TypeScript
- `clientService.ts`
- `sparepartService.ts`
- `equipmentService.ts`
- `saleService.ts`
- `rentService.ts`

### 3. Crear componentes presentacionales vs contenedores

**Presentacional (Dumb):**
```vue
<!-- components/PurchaseCard.vue -->
<template>
  <div class="card">
    <h3>{{ purchase.name }}</h3>
    <span :class="statusClass">{{ purchase.status }}</span>
  </div>
</template>

<script setup lang="ts">
import type { Purchase } from '@/types'

defineProps<{
  purchase: Purchase
}>()
</script>
```

**Contenedor (Smart):**
```vue
<!-- views/Administracion/ComprasView.vue -->
<template>
  <PurchaseCard
    v-for="purchase in purchases"
    :key="purchase.purchase_id"
    :purchase="purchase"
    @click="handleView(purchase)"
  />
</template>

<script setup lang="ts">
// Lógica de estado, stores, peticiones
</script>
```

### 4. Migración Gradual
- ✅ `config/api.js` → `config/api.ts`
- ✅ `services/purchaseService.js` → `services/purchaseService.ts`
- ✅ `services/billingService.js` → `services/billingService.ts`
- ⏳ Otros services
- ⏳ Vistas con `<script setup lang="ts">`
- ⏳ Componentes reutilizables con props tipadas

## 🎯 Beneficios Inmediatos

1. **Autocompletado**: IDE sugiere propiedades correctas
2. **Type Safety**: Detecta errores antes de ejecutar
3. **Refactoring**: Cambios seguros en toda la app
4. **Documentación**: Tipos son documentación viva
5. **Estado Centralizado**: Filtros persisten automáticamente
6. **DX Mejorado**: Menos bugs, más productividad

## 📝 Convenciones

- Archivos TS: `.ts` (services, stores, config)
- Componentes con TS: `<script setup lang="ts">`
- Importar tipos: `import type { ... }`
- Props tipadas: `defineProps<{ ... }>()`
- Emits tipadas: `defineEmits<{ ... }>()`
