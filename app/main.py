from fastapi import FastAPI
from app.auth.routers import router as user_router
from app.equipment.routers import router as equipment_router
from app.client.routers import router as client_router

from app.core.database import Base, engine

app = FastAPI(title="API de Usuarios")

app.include_router(user_router)
app.include_router(equipment_router)
app.include_router(client_router)

@app.get("/")
def root():
    return {"message": "Copy mart Api,  "}

Base.metadata.create_all(bind=engine)