from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger_config import logger
from pydantic import BaseModel
from typing import Any, Optional
from pathlib import Path
from datetime import datetime
import json
from auth.routers import router as user_router
from equipment.routers import router as equipment_router
from rent.routers import router as rent_router
from sale.routers import router as sale_router
from billing.routers import router as billing_router
from client.routers import router as client_router
from ticket.routers import router as ticket_router
from monthlyplan.routers import service_type_router, monthlyplan_router
from contact.routers import router as contact_router
from sparepart.routers import router as sparepart_router
from purchase.routers import router as purchase_router
from print.routers import router as print_router
from rh.routers import router as rh_router
from repair.routers import router as repair_router
from inventory.routers import (
    catalog_router,
    inventory_router,
    shelf_router
)


from core.database import Base, engine

# Importar TODOS los modelos para que se registren con SQLAlchemy
from auth import models as auth_models
from client import models as client_models
from contact import models as contact_models
from equipment import models as equipment_models
from rent import models as rent_models
from sale import models as sale_models
from billing import models as billing_models
from sparepart import models as sparepart_models
from purchase import models as purchase_models
from print import models as print_models
from rh import models as rh_models
from ticket import models as ticket_models
from monthlyplan import models as monthlyplan_models
from inventory import models as inventory_models

app = FastAPI(title="API de Usuarios")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:3000",
        "http://192.168.100.58:5173",
        "http://192.168.100.58:5174",
        "http://192.168.100.58:5175",
        "http://192.168.100.58:5176",
        "http://192.168.100.58:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FrontendLogEntry(BaseModel):
    level: str
    message: str
    data: Optional[Any] = None
    timestamp: Optional[str] = None
    url: Optional[str] = None


def _append_frontend_log(entry: FrontendLogEntry) -> None:
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "node.log"

    ts = entry.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = ""
    if entry.data is not None:
        try:
            payload = json.dumps(entry.data, ensure_ascii=False)
        except TypeError:
            payload = json.dumps(str(entry.data), ensure_ascii=False)

    line = f"[{ts}] [{entry.level.upper()}] {entry.message}"
    if payload:
        line += f" | {payload}"
    if entry.url:
        line += f" | url={entry.url}"
    line += "\n"

    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(line)


@app.post("/api/logs/frontend")
def log_frontend(entry: FrontendLogEntry):
    _append_frontend_log(entry)
    return {"status": "ok"}

app.include_router(user_router, prefix="/api")
app.include_router(equipment_router, prefix="/api")
app.include_router(client_router, prefix="/api/clients", tags=["clients"])
app.include_router(rent_router, prefix="/api")
app.include_router(sale_router, prefix="/api")
app.include_router(billing_router, prefix="/api")
app.include_router(ticket_router, prefix="/api")
app.include_router(service_type_router, prefix="/api")
app.include_router(monthlyplan_router, prefix="/api")
app.include_router(contact_router, prefix="/api")
app.include_router(sparepart_router, prefix="/api")
app.include_router(purchase_router, prefix="/api")
app.include_router(print_router, prefix="/api")
app.include_router(rh_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(shelf_router, prefix="/api")
app.include_router(repair_router, prefix="/api")



@app.get("/")
def root():
    return {"message": "Copy mart Api,  "}

Base.metadata.create_all(bind=engine)
