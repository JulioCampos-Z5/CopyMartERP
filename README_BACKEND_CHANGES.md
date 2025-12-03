# CopyMart ERP - Documentación de Cambios Backend

## Resumen de Cambios (Diciembre 2025)

Este documento describe los cambios realizados en el backend del sistema CopyMart ERP para sincronizar los modelos de SQLAlchemy con la estructura existente de la base de datos MySQL/MariaDB.

---

## 📁 Archivos Modificados

### 1. `app/auth/models.py` - Modelo de Usuario

**Cambios realizados:**
- Renombrado campo `password` → `hashed_password`
- Renombrado campo `rol` → `role`
- Eliminado `DepartmentEnum` (no existía en la BD)
- Agregado campo `updated_at`

**Estructura actual:**
```python
class RolEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    EMPLEADO = "EMPLEADO"

class User(Base):
    user_id          # PK
    username         # Único, requerido
    email            # Único, requerido
    full_name        # Nombre completo
    hashed_password  # Contraseña hasheada con bcrypt
    role             # RolEnum (ADMIN, GERENTE, EMPLEADO)
    is_active        # Estado del usuario
    created_at       # Fecha de creación
    updated_at       # Fecha de última actualización
```

---

### 2. `app/auth/schemas.py` - Esquemas de Autenticación

**Cambios realizados:**
- Actualizado `UserCreate` para usar `role` en lugar de `rol`
- Actualizado `UserResponse` para coincidir con el modelo
- `TokenData` ahora usa `role` (RolEnum) en lugar de `rol`

---

### 3. `app/auth/services.py` - Servicios de Autenticación

**Cambios realizados:**
- `create_user()` ahora usa `hashed_password` en lugar de `password`
- `authenticate_user()` verifica contra `hashed_password`

---

### 4. `app/auth/security.py` - Seguridad

**Cambios realizados:**
- Eliminada referencia a `DepartmentEnum`
- `decode_token()` retorna `TokenData` con `role` (no `rol`)
- Configuración de bcrypt compatible con versión 4.3.0

---

### 5. `app/auth/permissions.py` - Permisos

**Cambios realizados:**
- Todas las funciones ahora usan `user.role` en lugar de `user.rol`
- Permisos basados en roles: ADMIN > GERENTE > EMPLEADO

---

### 6. `app/client/models.py` - Modelo de Cliente

**Cambios realizados:**
- Agregados campos: `email`, `phone`, `website`, `industry`, `updated_at`
- Cambiado `rfc` de String(50) a String(20) para coincidir con BD
- Removido `ForeignKey` de `contact_id` para evitar dependencia circular
- Cambiada relación de `contact` (singular) a `contacts` (plural)

**Estructura actual:**
```python
class Client(Base):
    client_id        # PK
    name             # Razón social (requerido)
    comercial_name   # Nombre comercial
    rfc              # RFC (único)
    address          # Dirección
    colonia          # Colonia
    zip_code         # Código postal
    city             # Ciudad
    contact_id       # Referencia al contacto principal (sin FK)
    user_id          # FK → users.user_id
    email            # Email de la empresa
    phone            # Teléfono
    website          # Sitio web
    industry         # Industria/giro
    is_active        # Estado
    created_at       # Fecha de creación
    updated_at       # Fecha de actualización
    
    # Relaciones
    branches         # One-to-Many → Branch
    contacts         # One-to-Many → Contact
    creator          # Many-to-One → User
```

---

### 7. `app/contact/models.py` - Modelo de Contacto

**Cambios realizados:**
- `client_id` ahora es obligatorio (NOT NULL en BD)
- Agregados campos: `branch_id`, `area_id` para granularidad
- Renombrado `rol` → `position`
- Renombrado `is_client` → `is_primary`
- Eliminados campos: `company`, `is_client`
- Corregido `back_populates` de `"contact"` a `"contacts"`

**Estructura actual:**
```python
class Contact(Base):
    contact_id       # PK
    client_id        # FK → clients.client_id (requerido)
    branch_id        # FK → branches.branch_id (opcional)
    area_id          # FK → areas.area_id (opcional)
    name             # Nombre del contacto
    position         # Cargo/puesto
    email            # Email
    phone            # Teléfono
    is_primary       # Es contacto principal
    is_active        # Estado
    created_at       # Fecha de creación
    updated_at       # Fecha de actualización
    
    # Relaciones
    client           # Many-to-One → Client
    branch           # Many-to-One → Branch
    area             # Many-to-One → Area
```

---

### 8. `app/client/services.py` - Servicios de Cliente

**Cambios realizados:**
- Simplificada la creación de contactos
- Removido uso de `hasattr()` y `getattr()` innecesarios
- El contacto se crea DESPUÉS del cliente (necesita `client_id`)
- Se actualiza `contact_id` en el cliente después de crear el contacto

**Flujo de creación de cliente con contacto:**
```python
1. Crear cliente → flush() → obtener client_id
2. Si hay contact_name:
   - Crear contacto con client_id
   - flush()
   - Actualizar cliente.contact_id
3. Crear sucursales si las hay
4. commit()
```

---

### 9. `app/client/routers.py` - Router de Clientes

**Nota importante:**
- El endpoint de actualización usa `PATCH`, NO `PUT`
- Todos los endpoints requieren autenticación Bearer token

**Endpoints disponibles:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/clients/` | Crear cliente |
| GET | `/api/clients/` | Listar clientes |
| GET | `/api/clients/{id}` | Obtener cliente |
| PATCH | `/api/clients/{id}` | Actualizar cliente |
| DELETE | `/api/clients/{id}` | Eliminar cliente |

---

### 10. `app/rent/models.py` - Modelo de Rentas

**Cambios realizados:**
- `contract_number` cambiado de String() sin longitud a String(50)

---

## 🔧 Dependencias Actualizadas

```
bcrypt==4.3.0  # Downgrade para compatibilidad con passlib
```

**Razón:** bcrypt 5.x eliminó el atributo `__about__.__version__` que passlib necesita.

---

## 🗄️ Estructura de Base de Datos

Las tablas existentes en la BD son:
- `users` - Usuarios del sistema
- `clients` - Clientes
- `branches` - Sucursales de clientes
- `areas` - Áreas dentro de sucursales
- `contacts` - Contactos de clientes
- `equipment` - Equipos
- `items` - Items/productos
- `brands` - Marcas
- `suppliers` - Proveedores
- `rents` - Contratos de renta

---

## 🔐 Autenticación

**Sistema de autenticación JWT:**
- Endpoint de login: `POST /users/login`
- Token expira en 480 minutos (8 horas)
- Header requerido: `Authorization: Bearer <token>`

**Usuarios de prueba:**
| Email | Contraseña | Rol |
|-------|------------|-----|
| admin@copymart.com | admin123 | ADMIN |
| gerente@copymart.com | gerente123 | GERENTE |
| empleado@copymart.com | empleado123 | EMPLEADO |

---

## 🚀 Ejecución del Backend

```bash
# Activar entorno virtual
cd C:\Users\SISTEMAS\Desktop\CopyMartERP
.\.venv\Scripts\Activate.ps1

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**URL de la API:** http://localhost:8000

**Documentación automática:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ⚠️ Notas Importantes

1. **CORS:** Configurado para aceptar requests desde `localhost:5173`, `5174` y `3000`

2. **Soft Delete:** Los clientes no se eliminan físicamente, solo se desactivan (`is_active = False`)

3. **Relación Contact-Client:** 
   - Un contacto DEBE pertenecer a un cliente (`client_id` obligatorio)
   - Un cliente puede tener múltiples contactos
   - `contact_id` en `clients` es una referencia rápida al contacto principal

4. **Validaciones Pydantic:** El warning sobre `orm_mode` → `from_attributes` es solo informativo, no afecta el funcionamiento

---

## 📝 Changelog

### v1.1.0 (Diciembre 2025)
- ✅ Sincronizados modelos con estructura de BD existente
- ✅ Corregido sistema de autenticación
- ✅ Agregado módulo de Rentas
- ✅ Corregidas relaciones entre Client y Contact
- ✅ Downgrade de bcrypt para compatibilidad
- ✅ Agregada documentación en código

