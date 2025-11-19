from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routers import router as user_router
from app.client.routers import router as client_router
from app.equipment.routers import router as equipment_router
from app.core.database import Base, engine
# Importar modelos para que se registren con SQLAlchemy
from app.auth import models as auth_models
from app.client import models as client_models
from app.equipment import models as equipment_models

app = FastAPI(title="API de Usuarios")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # URLs del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(client_router, prefix="/api/clients", tags=["clients"])
app.include_router(equipment_router, prefix="/api/equipment", tags=["equipment"])

@app.get("/")
def root():
    return {"message": "ok"}

Base.metadata.create_all(bind=engine)