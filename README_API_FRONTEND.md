# Conexión API Backend (FastAPI) con Frontend (Vue.js) elimina el readme cuando termines de usarlo 👍

## Arquitectura General

```
Frontend (Vue.js)          Backend (FastAPI)           Base de Datos
Port: 5174           →     Port: 8000            →     MariaDB/PostgreSQL
```

## 1. Configuración del Backend (FastAPI)

### Base de Datos
El backend está configurado para conectarse a **MariaDB** por defecto, pero incluye configuración comentada para **PostgreSQL**.

**Archivo**: `app/core/database.py`

#### Configuración Actual (MariaDB)
```python
# MariaDB Connection (ACTUAL)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/copymart_erp"
```


### Dependencias del Backend
**Archivo**: `app/requirements.txt`
```txt
fastapi
uvicorn[standard]
sqlalchemy
pymysql          # Para MariaDB
# psycopg2-binary  # Descomentar para PostgreSQL
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

### Ejecución del Backend
```bash
# Desde la raíz del proyecto
uvicorn app.main:app --reload

# El servidor estará disponible en: http://localhost:8000
# Documentación automática: http://localhost:8000/docs
```

## 2. Configuración del Frontend (Vue.js)

### Estructura de Servicios
El frontend se comunica con la API mediante módulos organizados:

```
copy-mart/src/
├── services/
│   └── api.js          # Cliente Axios configurado
├── composables/
│   └── useAuth.js      # Lógica de autenticación
└── views/
    └── LoginView.vue   # Interfaz de login
```

### Configuración de Axios
**Archivo**: `copy-mart/src/services/api.js`

```javascript
import axios from 'axios'

// URL base de la API
const API_URL = 'http://localhost:8000'

// Cliente configurado
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token JWT
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

export default apiClient
```

### Ejecución del Frontend
```bash
# Desde la carpeta copy-mart
cd copy-mart
npm install
npm run dev

# El servidor estará disponible en: http://localhost:5174
```

## 3. Flujo de Autenticación

### 1. Login del Usuario
```
Usuario ingresa credenciales
         ↓
LoginView.vue captura datos
         ↓
POST /auth/login → Backend FastAPI
         ↓
Backend valida con base de datos
         ↓
Retorna JWT token + datos usuario
         ↓
Frontend guarda en localStorage
         ↓
Redirige a /dashboard
```

### 2. Peticiones Autenticadas
```
Frontend hace petición
         ↓
Interceptor agrega: Authorization: Bearer {token}
         ↓
Backend valida token JWT
         ↓
Retorna datos protegidos
```

## 4. Endpoints Principales

### Autenticación
- `POST /auth/login` - Iniciar sesión
  ```json
  Request: {
    "username": "admin@copymart.com",
    "password": "admin123"
  }
  Response: {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "user": { ... }
  }
  ```

### Usuarios (Protegidos)
- `GET /users/me` - Datos del usuario actual
- `GET /users/` - Lista de usuarios (admin)
- `POST /users/` - Crear usuario (admin)

## 5. CORS (Cross-Origin Resource Sharing)

**Archivo**: `app/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Esto permite que el frontend (puerto 5174) haga peticiones al backend (puerto 8000).

## 6. Variables de Entorno

### Backend
Crea un archivo `.env` en la raíz del proyecto:

```env
# Seguridad
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de Datos - MariaDB (actual)
DATABASE_URL=mysql+pymysql://root@localhost/copymart_erp

# Base de Datos - PostgreSQL (alternativa)
# DATABASE_URL=postgresql://usuario:password@localhost/copymart_erp
```

### Frontend
Crea un archivo `.env` en `copy-mart/`:

```env
VITE_API_URL=http://localhost:8000
```

## 7. Cambiar de MariaDB a PostgreSQL

### Paso 1: Instalar Driver
```bash
pip install psycopg2-binary
```

### Paso 2: Actualizar `app/core/database.py`
```python
# Comentar MariaDB
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/copymart_erp"

# Descomentar PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost/copymart_erp"
```

### Paso 3: Crear Base de Datos en PostgreSQL
```sql
CREATE DATABASE copymart_erp;
CREATE USER tu_usuario WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE copymart_erp TO tu_usuario;
```

### Paso 4: Ejecutar Migraciones
```bash
# Las tablas se crean automáticamente al iniciar el backend
python -m app.main
```

## 8. Estructura de Datos

### Usuario en localStorage (Frontend)
```javascript
{
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@copymart.com",
    "full_name": "Administrador CopyMart",
    "is_active": true,
    "is_superuser": true
  }
}
```

### Base de Datos (Backend)
Tablas principales:
- `users` - Usuarios del sistema
- `roles` - Roles y permisos
- `permissions` - Permisos específicos

## 9. Solución de Problemas Comunes

### Error: "Connection refused" al hacer login
- Verifica que el backend esté corriendo: `http://localhost:8000/docs`
- Revisa la configuración CORS en `app/main.py`

### Error: "Database connection failed"
- Verifica que MariaDB/PostgreSQL esté corriendo
- Confirma credenciales en `app/core/database.py`
- Revisa que la base de datos exista

### Error: "Token expired"
- El token JWT expira después de 30 minutos
- Usuario debe hacer login nuevamente

## 10. Credenciales por Defecto

```
Email: admin@copymart.com
Password: admin123
```

Para crear el usuario admin inicial:
```bash
python app/create_admin.py
```

## 11. Pruebas Rápidas

### Probar Backend
```bash
curl http://localhost:8000/
# Respuesta esperada: {"message": "CopyMart ERP API"}
```

### Probar Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@copymart.com","password":"admin123"}'
```

## Recursos Adicionales

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Vue.js Docs**: https://vuejs.org/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Axios**: https://axios-http.com/
