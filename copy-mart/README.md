# CopyMart ERP - Sistema de Gestión Empresarial

Sistema ERP desarrollado con Vue 3 + Vite para el frontend y FastAPI para el backend, diseñado para la gestión integral de clientes, inventario, usuarios y operaciones comerciales.

## 📋 Tabla de Contenidos

- [Características Principales](#características-principales)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración e Instalación](#configuración-e-instalación)
- [Módulos Implementados](#módulos-implementados)
- [Changelog de Actualizaciones](#changelog-de-actualizaciones)

## 🚀 Características Principales

- **Autenticación JWT**: Sistema completo de login/logout con tokens de seguridad
- **Gestión de Clientes**: CRUD completo con información de contacto integrada
- **Gestión de Usuarios**: Perfiles editables con cambio de contraseña y email
- **Navegación Adaptativa**: Sidebar colapsable con navegación intuitiva
- **Base de Datos**: MariaDB con 9 tablas relacionales
- **API RESTful**: Backend robusto con FastAPI
- **UI/UX Moderna**: Interfaz responsiva con Tailwind CSS

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Vue 3** (Composition API)
- **Vue Router** - Navegación SPA
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Framework de estilos
- **Font Awesome** - Iconografía

### Backend
- **FastAPI** - Framework web Python
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **JWT** - Autenticación basada en tokens
- **Uvicorn** - Servidor ASGI

### Base de Datos
- **MariaDB** - Sistema de gestión de bases de datos

## 📁 Estructura del Proyecto

```
CopyMartERP/
├── app/                          # Backend FastAPI
│   ├── auth/                     # Módulo de autenticación
│   │   ├── models.py            # Modelo User, RolEnum, DepartmentEnum
│   │   ├── routers.py           # Endpoints: login, /users/me, cambio de contraseña/email
│   │   ├── schemas.py           # UserCreate, UserUpdate, UserResponse, Token
│   │   ├── security.py          # JWT, hashing de contraseñas
│   │   └── services.py          # Lógica de negocio de usuarios
│   ├── client/                   # Módulo de clientes
│   │   ├── models.py            # Client, Branch, Area
│   │   ├── routers.py           # CRUD de clientes con contactos integrados
│   │   ├── schemas.py           # ClientCreate con campos de contacto
│   │   └── services.py          # Creación automática de contactos
│   ├── contact/                  # Módulo de contactos
│   │   ├── models.py            # Contact (name, phone, email, rol)
│   │   ├── routers.py           # CRUD de contactos
│   │   └── schemas.py           # ContactCreate, ContactResponse
│   ├── equipment/                # Módulo de equipos (preparado)
│   ├── core/                     # Configuración central
│   │   └── database.py          # Conexión SQLAlchemy
│   └── main.py                   # Aplicación principal, CORS, routers
│
├── copy-mart/                    # Frontend Vue 3
│   ├── src/
│   │   ├── components/
│   │   │   ├── AppNavigation.vue      # Sidebar con perfil clicable
│   │   │   ├── BaseLayout.vue         # Layout principal
│   │   │   └── LoginForm.vue          # Formulario de autenticación
│   │   ├── views/
│   │   │   ├── LoginView.vue          # Vista de login
│   │   │   ├── DashboardView.vue      # Dashboard principal
│   │   │   ├── ClientesView.vue       # Gestión de clientes con contactos
│   │   │   ├── PerfilView.vue         # Edición de perfil de usuario
│   │   │   └── UsuariosView.vue       # Gestión de usuarios
│   │   ├── services/
│   │   │   ├── userService.js         # API de usuarios y autenticación
│   │   │   ├── clientService.js       # API de clientes y sucursales
│   │   │   └── contactService.js      # API de contactos
│   │   ├── router/
│   │   │   └── index.js               # Rutas y guards de navegación
│   │   └── assets/
│   │       └── main.css               # Estilos personalizados Tailwind
│   └── package.json
│
└── README.md                     # Este archivo
```

## ⚙️ Configuración e Instalación

### Prerrequisitos

- Node.js (v16 o superior)
- Python 3.9+
- MariaDB 10.5+

### Instalación del Backend

```bash
# Navegar a la carpeta del proyecto
cd CopyMartERP

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos en app/core/database.py
# DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/copymart"

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

### Instalación del Frontend

```bash
# Navegar a la carpeta del frontend
cd copy-mart

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173` o `http://localhost:5174`

## 📦 Módulos Implementados

### 1. Autenticación y Usuarios

**Funcionalidades:**
- Login con email y contraseña
- Generación de tokens JWT
- Endpoint `/users/me` para obtener usuario actual
- Cambio de contraseña con validación de contraseña actual
- Cambio de email con verificación de duplicados
- Actualización de perfil (nombre completo)
- Logout con limpieza de localStorage

**Archivos clave:**
- Backend: `app/auth/routers.py`, `app/auth/security.py`
- Frontend: `copy-mart/src/services/userService.js`, `copy-mart/src/views/PerfilView.vue`

**Base de datos:**
- Tabla `users`: user_id, email, full_name, password, rol, department, is_active

### 2. Gestión de Clientes

**Funcionalidades:**
- CRUD completo de clientes
- Creación automática de contacto al crear cliente
- Información de contacto integrada en el formulario de cliente
- Activar/Desactivar clientes
- Visualización de sucursales asociadas
- Búsqueda y filtros

**Formulario de Cliente incluye:**

*Información General:*
- Nombre de la Empresa (requerido)
- Nombre Comercial
- RFC
- Dirección completa (calle, colonia, CP, ciudad)

*Información de Contacto:*
- Nombre del Contacto
- Cargo/Puesto
- Teléfono
- Email

**Archivos clave:**
- Backend: `app/client/routers.py`, `app/client/services.py`, `app/client/schemas.py`
- Frontend: `copy-mart/src/views/ClientesView.vue`, `copy-mart/src/services/clientService.js`

**Base de datos:**
- Tabla `clients`: client_id, name, comercial_name, rfc, address, colonia, zip_code, city, contact_id, is_active
- Tabla `contacts`: contact_id, name, phone, email, company, rol, is_client
- Tabla `branches`: branch_id, client_id, name, address, is_main
- Tabla `areas`: area_id, branch_id, name

### 3. Navegación y Perfil

**Funcionalidades:**
- Sidebar colapsable con todas las secciones del ERP
- Avatar de usuario en el footer del sidebar
- Click en avatar/nombre navega a vista de perfil
- Botón de logout independiente
- Títulos dinámicos por ruta
- Carga de datos del usuario desde el backend

**Archivos clave:**
- `copy-mart/src/components/AppNavigation.vue`
- `copy-mart/src/components/BaseLayout.vue`

## 📝 Changelog de Actualizaciones

### Versión 1.0.0 - Implementación Inicial del Sistema

#### Backend - Autenticación y Usuarios

**1. Endpoint `/users/me` (Nuevo)**
- **Archivo**: `app/auth/routers.py`
- **Función**: Obtiene información del usuario autenticado actual
- **Método**: GET
- **Respuesta**: UserResponse con todos los datos del usuario
- **Uso**: Carga automática de datos al entrar a la vista de perfil

**2. Endpoint `PUT /users/{user_id}` (Nuevo)**
- **Archivo**: `app/auth/routers.py`
- **Función**: Actualiza información del usuario
- **Schema**: UserUpdate (full_name, email, department, rol)
- **Validación**: Verifica que el email no esté en uso por otro usuario
- **Uso**: Actualización de perfil desde el frontend

**3. Mejoras en Login**
- **Archivo**: `copy-mart/src/services/userService.js`
- **Cambio**: Ahora obtiene datos completos del usuario desde `/users/me` después del login
- **Beneficio**: localStorage se llena con el objeto de usuario completo incluyendo `user_id`
- **Impacto**: Permite todas las operaciones de perfil sin recargar

**4. Unificación de Tokens**
- **Cambio**: Todos los servicios ahora usan `localStorage.getItem('token')` en lugar de `auth_token`
- **Archivos afectados**: 
  - `userService.js`
  - `clientService.js`
  - `contactService.js`
  - `equipmentService.js`
- **Beneficio**: Consistencia en toda la aplicación

#### Backend - Clientes y Contactos

**5. Integración de Contactos en Clientes**
- **Archivo**: `app/client/schemas.py`
- **Cambio**: ClientCreate ahora incluye campos opcionales de contacto:
  - `contact_name`
  - `contact_phone`
  - `contact_email`
  - `contact_rol`
- **Beneficio**: Crear cliente y contacto en una sola operación

**6. Servicio de Creación Automática de Contactos**
- **Archivo**: `app/client/services.py`
- **Función**: `create_client()` modificada
- **Lógica**: 
  ```python
  # Si vienen datos de contacto, crea automáticamente un Contact
  # y lo vincula al cliente
  if client_data.contact_name:
      new_contact = Contact(...)
      db.add(new_contact)
      contact_id = new_contact.contact_id
  ```
- **Beneficio**: Usuario no necesita crear contactos por separado

**7. Corrección de Prefijos de Router**
- **Archivo**: `app/client/routers.py`
- **Cambio**: Eliminado `prefix="/clients"` del APIRouter
- **Razón**: El prefijo ya se añade en `main.py`
- **Resultado**: Rutas correctas `/api/clients` en lugar de `/api/clients/clients`

#### Frontend - Vista de Perfil

**8. Vista de Perfil Completa**
- **Archivo**: `copy-mart/src/views/PerfilView.vue`
- **Cambios**:
  - Usa BaseLayout en lugar de incluir AppNavigation
  - Carga datos del usuario con `loadUserData()` desde `/users/me`
  - Actualización de información personal con backend
  - Cambio de contraseña con validación
  - Modal de cambio de email
  - Exportación de datos del usuario
- **Datos mostrados**:
  - Nombre completo (editable)
  - Email (con botón de cambio)
  - Rol (solo lectura)
  - Departamento (solo lectura)
  - Estadísticas de usuario

**9. Método `loadUserData()` Mejorado**
- **Prioridad**: Intenta obtener datos desde backend (`/users/me`)
- **Fallback**: Si falla, usa datos de localStorage
- **Actualización**: Guarda los datos obtenidos en localStorage
- **Beneficio**: Siempre tiene datos actualizados

**10. Método `updatePersonalInfo()` Funcional**
- **Antes**: Solo actualizaba localStorage (comentado)
- **Ahora**: Llama a `userService.updateUser(userId, data)`
- **Sincronización**: Actualiza backend y localStorage
- **UX**: Muestra confirmación antes de guardar

#### Frontend - Vista de Clientes

**11. Formulario de Cliente con Contactos**
- **Archivo**: `copy-mart/src/views/ClientesView.vue`
- **Estructura**: Dividido en dos secciones
  
  **Sección 1 - Información General:**
  - Nombre de la Empresa (required)
  - Nombre Comercial
  - RFC (max 13 caracteres)
  - Dirección
  - Colonia
  - Código Postal (max 5 caracteres)
  - Ciudad
  
  **Sección 2 - Información de Contacto:**
  - Nombre del Contacto
  - Cargo/Puesto
  - Teléfono
  - Email

**12. Objeto clientForm Actualizado**
```javascript
clientForm: {
  // Datos del cliente
  name: '',
  comercial_name: '',
  rfc: '',
  address: '',
  colonia: '',
  zip_code: '',
  city: '',
  // Datos del contacto
  contact_name: '',
  contact_phone: '',
  contact_email: '',
  contact_rol: ''
}
```

**13. Tabla de Clientes Mejorada**
- **Columnas actualizadas**:
  - Cliente (nombre + nombre comercial)
  - RFC
  - Dirección (con colonia en subtexto)
  - Ciudad
  - Estado (Activo/Inactivo)
  - Sucursales (contador)
  - Acciones
- **Key corregida**: `client.client_id` en lugar de `client.id`
- **Botones visibles**: "Editar" (azul) y "Desactivar/Activar" (rojo/verde)

**14. Método `editClient()` Mejorado**
```javascript
editClient(client) {
  this.clientForm = {
    ...client,
    // Extrae datos del contacto si existen
    contact_name: client.contact?.name || '',
    contact_phone: client.contact?.phone || '',
    contact_email: client.contact?.email || '',
    contact_rol: client.contact?.rol || ''
  }
}
```

#### Frontend - Navegación

**15. AppNavigation con Perfil Clicable**
- **Archivo**: `copy-mart/src/components/AppNavigation.vue`
- **Cambios**:
  - Sección de usuario ahora es `<router-link to="/perfil">`
  - Agregado `hover:bg-gray-50` para feedback visual
  - Tooltip con `title="Ver perfil"`
  - Logout como botón independiente
  - Corregido `loadCurrentUser()` para usar key `'user'` en lugar de `'user_data'`

**16. Títulos de Ruta**
- **Agregado**: `'/perfil': 'Mi Perfil'` en el objeto `routeTitles`
- **Beneficio**: Título correcto en la barra superior

#### Servicios del Frontend

**17. userService.js - Métodos Agregados**
```javascript
// Obtener usuario actual
async getCurrentUser() {
  return apiRequest('/users/me')
}

// Actualizar usuario
async updateUser(id, userData) {
  return apiRequest(`/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(userData)
  })
}

// Cambiar contraseña
async changePassword(userId, currentPassword, newPassword) {
  return apiRequest(`/users/${userId}/password`, {
    method: 'PUT',
    body: JSON.stringify({
      old_password: currentPassword,
      new_password: newPassword
    })
  })
}

// Cambiar email
async changeEmail(userId, newEmail) {
  return apiRequest(`/users/${userId}/email`, {
    method: 'PUT',
    body: JSON.stringify({ new_email: newEmail })
  })
}
```

**18. Login Mejorado**
- **Antes**: Guardaba objeto básico hardcodeado
- **Ahora**: Obtiene datos completos desde `/users/me` después de autenticarse
- **Guardado**: Token + datos completos del usuario + flag isAuthenticated

#### Base de Datos

**19. Estructura Confirmada**
- 9 tablas creadas correctamente:
  - `users` - Usuarios del sistema
  - `clients` - Clientes empresariales
  - `contacts` - Contactos de clientes
  - `branches` - Sucursales de clientes
  - `areas` - Áreas dentro de sucursales
  - `items` - Productos/Equipos
  - `brands` - Marcas
  - `suppliers` - Proveedores
  - `information_schema` - Metadata del sistema

**20. Relaciones Implementadas**
- Client → Contact (Many-to-One)
- Client → Branches (One-to-Many)
- Branch → Areas (One-to-Many)
- Client → User (Many-to-One, creator)

### Flujos de Usuario Principales

#### Flujo de Login
1. Usuario ingresa email y contraseña
2. POST a `/users/login` → recibe `access_token`
3. GET a `/users/me` con el token → recibe datos completos del usuario
4. Guarda en localStorage: `token`, `user`, `isAuthenticated`
5. Redirige a `/dashboard`

#### Flujo de Edición de Perfil
1. Usuario hace click en avatar en el sidebar
2. Navega a `/perfil`
3. `loadUserData()` obtiene datos desde `/users/me`
4. Usuario edita nombre y hace click en "Guardar Cambios"
5. PUT a `/users/{id}` con los datos actualizados
6. Actualiza localStorage y muestra confirmación

#### Flujo de Creación de Cliente
1. Usuario hace click en "Nuevo Cliente"
2. Llena formulario con información general y de contacto
3. Click en "Crear"
4. Frontend envía POST a `/api/clients` con todos los datos
5. Backend crea el Contact automáticamente si `contact_name` existe
6. Backend crea el Client vinculado al Contact
7. Retorna el cliente creado con relaciones
8. Frontend recarga la lista de clientes

#### Flujo de Edición de Cliente
1. Usuario hace click en botón "Editar" en la tabla
2. Modal se abre con datos del cliente
3. Si el cliente tiene contacto, carga sus datos en los campos correspondientes
4. Usuario modifica datos y click en "Actualizar"
5. PUT a `/api/clients/{id}` actualiza el cliente
6. Tabla se refresca con datos actualizados

### Configuración CORS

**Puertos permitidos:**
- `http://localhost:5173` - Vite dev server (principal)
- `http://localhost:5174` - Vite dev server (alternativo)
- `http://localhost:3000` - Posible puerto de producción

### Credenciales por Defecto

```
Email: admin@copymart.com
Password: admin123
```


## 👥 Créditos

Desarrollado para CopyMart - Sistema de Gestión Empresarial

---

**Última actualización:** 21 de noviembre de 2025
