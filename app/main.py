import os
import sys

# Asegurar que el directorio app/ esté en el path cuando se ejecuta directamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from logger_config import logger
from pydantic import BaseModel
from typing import Any, Optional
from pathlib import Path
from datetime import datetime
import json
import psutil
import platform
import shutil
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
from route.routers import router as route_router
from inventory.routers import (
    catalog_router,
    inventory_router,
    shelf_router
)
from audit.routers import router as audit_router
from notification.routers import router as notification_router
from system.routers import router as system_router


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
from route import models as route_models
from audit import models as audit_models
from notification import models as notification_models

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
        "http://192.168.100.93:5173",
        "http://192.168.100.93:5174",
        "http://192.168.100.93:5175",
        "http://192.168.100.93:5176",
        "http://192.168.100.93:3000"
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


# ── System Info endpoint for TI module ──
from auth.routers import get_current_user

@app.get("/api/system-info")
def get_system_info(current_user = Depends(get_current_user)):
    """Return real system metrics for the TI dashboard."""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()

    # RAM
    mem = psutil.virtual_memory()
    ram_total_gb = round(mem.total / (1024**3), 1)
    ram_used_gb = round(mem.used / (1024**3), 1)
    ram_percent = mem.percent

    # Disk
    disk = shutil.disk_usage("/")
    disk_total_gb = round(disk.total / (1024**3), 1)
    disk_used_gb = round(disk.used / (1024**3), 1)
    disk_percent = round((disk.used / disk.total) * 100, 1)

    # Network
    net = psutil.net_io_counters()
    net_sent_mb = round(net.bytes_sent / (1024**2), 1)
    net_recv_mb = round(net.bytes_recv / (1024**2), 1)

    # Uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = (datetime.now() - boot_time).total_seconds()
    uptime_hours = int(uptime_seconds // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)

    # DB check
    db_online = False
    try:
        from core.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db_online = True
        db.close()
    except Exception:
        db_online = False

    # Backend status
    backend_online = True  # If we reached here, backend is up

    return {
        "cpu": {"percent": cpu_percent, "cores": cpu_count},
        "ram": {"total_gb": ram_total_gb, "used_gb": ram_used_gb, "percent": ram_percent},
        "disk": {"total_gb": disk_total_gb, "used_gb": disk_used_gb, "percent": disk_percent},
        "network": {"sent_mb": net_sent_mb, "recv_mb": net_recv_mb},
        "uptime": {"hours": uptime_hours, "minutes": uptime_minutes, "boot_time": boot_time.isoformat()},
        "services": {
            "backend": backend_online,
            "database": db_online
        },
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": platform.node(),
            "python_version": platform.python_version()
        }
    }

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
app.include_router(route_router, prefix="/api")
app.include_router(audit_router, prefix="/api")
app.include_router(notification_router, prefix="/api")
app.include_router(system_router, prefix="/api")



@app.get("/")
def root():
    return {"message": "CopyMart ERP API"}

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))

    logger.info(f"Servidor iniciando en http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
