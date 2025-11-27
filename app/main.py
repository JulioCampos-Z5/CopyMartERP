from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routers import router as user_router
<<<<<<< HEAD
from app.equipment.routers import router as equipment_router
from app.client.routers import router as client_router
from fastapi.middleware.cors import CORSMiddleware

=======
from app.client.routers import router as client_router
from app.contact.routers import router as contact_router
from app.equipment.routers import router as equipment_router
>>>>>>> develop
from app.core.database import Base, engine

# Importar TODOS los modelos para que se registren con SQLAlchemy
from app.auth import models as auth_models
from app.client import models as client_models
from app.contact import models as contact_models
from app.equipment import models as equipment_models

app = FastAPI(title="API de Usuarios")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
<<<<<<< HEAD
app.include_router(equipment_router)
app.include_router(client_router)
=======
app.include_router(client_router, prefix="/api/clients", tags=["clients"])
app.include_router(contact_router, prefix="/api/contacts", tags=["contacts"])
app.include_router(equipment_router, prefix="/api/equipment", tags=["equipment"])
>>>>>>> develop

@app.get("/")
def root():
    return {"message": "Copy mart Api,  "}

Base.metadata.create_all(bind=engine)