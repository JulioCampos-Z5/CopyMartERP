import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine

# Importar modelos para que se registren con SQLAlchemy
print("Importando modelos...")
try:
    from auth import models as auth_models
    print("✓ Modelos de autenticación importados")
except ImportError as e:
    print(f"⚠ Error importando modelos de auth: {e}")

try:
    from client import models as client_models
    print("✓ Modelos de cliente importados")
except ImportError as e:
    print(f"⚠ Error importando modelos de client: {e}")

try:
    from equipment import models as equipment_models
    print("✓ Modelos de equipo importados")
except ImportError as e:
    print(f"⚠ Error importando modelos de equipment: {e}")

app = FastAPI(title="CopyMart ERP API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers cuando estén disponibles
try:
    from auth.routers import router as user_router
    app.include_router(user_router)
    print("✓ Router de usuarios incluido")
except ImportError as e:
    print(f"⚠ Router de users no disponible: {e}")

try:
    from client.routers import router as client_router
    app.include_router(client_router, prefix="/api/clients", tags=["clients"])
    print("✓ Router de clientes incluido")
except ImportError as e:
    print(f"⚠ Router de clients no disponible: {e}")

try:
    from equipment.routers import router as equipment_router
    app.include_router(equipment_router, prefix="/api/equipment", tags=["equipment"])
    print("✓ Router de equipos incluido")
except ImportError as e:
    print(f"⚠ Router de equipment no disponible: {e}")

try:
    from sale.routers import router as sale_router
    app.include_router(sale_router)
    print("✓ Router de ventas incluido")
except ImportError as e:
    print(f"⚠ Router de sales no disponible: {e}")

try:
    from rent.routers import router as rent_router
    app.include_router(rent_router)
    print("✓ Router de rentas incluido")
except ImportError as e:
    print(f"⚠ Router de rents no disponible: {e}")

try:
    from billing.routers import router as billing_router
    app.include_router(billing_router)
    print("✓ Router de facturación incluido")
except ImportError as e:
    print(f"⚠ Router de billings no disponible: {e}")

@app.get("/")
def root():
    return {"message": "CopyMart ERP API funcionando correctamente"}

# Crear tablas
print("Creando tablas en la base de datos...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")
except Exception as e:
    print(f"❌ Error creando tablas: {e}")
