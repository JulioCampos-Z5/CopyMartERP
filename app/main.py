from fastapi import FastAPI
from app.auth.routers import router as user_router
from app.core.database import Base, engine

app = FastAPI(title="API de Usuarios")

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "ok"}

Base.metadata.create_all(bind=engine)