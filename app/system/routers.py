from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, text, inspect
from typing import Optional
from datetime import datetime, timedelta, timezone
from core.database import get_db, engine, Base
from auth.routers import get_current_user
from auth.models import User, RolEnum
from client.models import Client
from sale.models import Sale
from rent.models import Rent
from billing.models import Billing
from ticket.models import Ticket
from equipment.models import Equipment
from repair.models import Repair
from purchase.models import Purchase
from print.models import PrintCounter  # noqa: F401 — necesario para inicializar el mapper de Rent

router = APIRouter(prefix="/system", tags=["Sistema"])


# ─── REPORTES ───────────────────────────────────────────────────────────

@router.get("/reports/summary")
def get_reports_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Resumen general para el dashboard de reportes."""
    try:
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        total_clients = db.query(func.count(Client.client_id)).scalar() or 0
        total_sales = db.query(func.count(Sale.sale_id)).scalar() or 0
        sales_this_month = db.query(func.count(Sale.sale_id)).filter(
            Sale.created_at >= month_start
        ).scalar() or 0
        active_rents = db.query(func.count(Rent.rent_id)).filter(
            Rent.contract_status == "vigente"
        ).scalar() or 0
        total_rents = db.query(func.count(Rent.rent_id)).scalar() or 0
        overdue_billing = db.query(func.count(Billing.billing_id)).filter(
            Billing.status == "vencido"
        ).scalar() or 0
        pending_billing = db.query(func.count(Billing.billing_id)).filter(
            Billing.status == "pendiente"
        ).scalar() or 0
        open_tickets = db.query(func.count(Ticket.ticket_id)).filter(
            Ticket.report_status.in_(["pendiente", "urgente"])
        ).scalar() or 0
        equipment_count = db.query(func.count(Equipment.item_id)).scalar() or 0
        repairs_pending = db.query(func.count(Repair.repair_id)).filter(
            Repair.estado_taller == "pendiente"
        ).scalar() or 0
        purchases_active = db.query(func.count(Purchase.purchase_id)).filter(
            Purchase.status.in_(["en_curso", "en_transito"])
        ).scalar() or 0

        return {
            "clients": total_clients,
            "sales": {"total": total_sales, "this_month": sales_this_month},
            "rents": {"total": total_rents, "active": active_rents},
            "billing": {"overdue": overdue_billing, "pending": pending_billing},
            "tickets": {"open": open_tickets},
            "equipment": {"total": equipment_count},
            "repairs": {"pending": repairs_pending},
            "purchases": {"active": purchases_active}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/reports/sales-by-month")
def get_sales_by_month(
    months: int = Query(12, ge=1, le=24),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ventas agrupadas por mes."""
    since = datetime.now(timezone.utc) - timedelta(days=months * 30)
    rows = db.execute(text("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') as month, COUNT(*) as count
        FROM sales WHERE created_at >= :since
        GROUP BY month ORDER BY month
    """), {"since": since}).fetchall()
    return [{"month": r[0], "count": r[1]} for r in rows]


@router.get("/reports/rents-by-status")
def get_rents_by_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rentas agrupadas por estado."""
    try:
        rows = db.execute(text("""
            SELECT contract_status, COUNT(*) as count FROM rents GROUP BY contract_status
        """)).fetchall()
        return [{"status": r[0], "count": r[1]} for r in rows]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/reports/billing-aging")
def get_billing_aging(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Antigüedad de cobranza."""
    now = datetime.now(timezone.utc)
    rows = db.execute(text("""
        SELECT
            SUM(CASE WHEN status = 'pagado' THEN 1 ELSE 0 END) as pagado,
            SUM(CASE WHEN status = 'pendiente' AND target_date >= :now THEN 1 ELSE 0 END) as vigente,
            SUM(CASE WHEN status = 'pendiente' AND target_date < :now THEN 1 ELSE 0 END) as vencido_pendiente,
            SUM(CASE WHEN status = 'vencido' THEN 1 ELSE 0 END) as vencido
        FROM billings
    """), {"now": now}).fetchone()
    return {
        "pagado": rows[0] or 0,
        "vigente": rows[1] or 0,
        "vencido_pendiente": rows[2] or 0,
        "vencido": rows[3] or 0
    }


@router.get("/reports/tickets-by-type")
def get_tickets_by_type(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Tickets agrupados por tipo."""
    rows = db.execute(text("""
        SELECT report_type, COUNT(*) as count FROM tickets GROUP BY report_type
    """)).fetchall()
    return [{"type": r[0], "count": r[1]} for r in rows]


@router.get("/reports/equipment-by-location")
def get_equipment_by_location(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Equipos por ubicación."""
    try:
        rows = db.execute(text("""
            SELECT location_status, COUNT(*) as count FROM items GROUP BY location_status
        """)).fetchall()
        return [{"location": r[0], "count": r[1]} for r in rows]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ─── BÚSQUEDA GLOBAL ───────────────────────────────────────────────────

@router.get("/search")
def global_search(
    q: str = Query(..., min_length=2, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Búsqueda global en clientes, equipos, tickets y ventas."""
    term = f"%{q}%"
    results = []

    # Clientes
    clients = db.execute(text(
        "SELECT client_id, name, rfc FROM clients WHERE name LIKE :t OR rfc LIKE :t LIMIT 10"
    ), {"t": term}).fetchall()
    for c in clients:
        results.append({"type": "client", "id": c[0], "title": c[1],
                         "subtitle": c[2] or "", "link": f"/comercial/clientes/{c[0]}"})

    # Equipos
    equips = db.execute(text(
        "SELECT item_id, sku, serial_number, model FROM items WHERE sku LIKE :t OR serial_number LIKE :t OR model LIKE :t LIMIT 10"
    ), {"t": term}).fetchall()
    for e in equips:
        results.append({"type": "equipment", "id": e[0], "title": f"{e[1]} - {e[2]}",
                         "subtitle": e[3] or "", "link": f"/administracion/equipos/{e[0]}"})

    # Tickets
    tickets = db.execute(text(
        "SELECT ticket_id, description FROM tickets WHERE description LIKE :t LIMIT 10"
    ), {"t": term}).fetchall()
    for t_row in tickets:
        results.append({"type": "ticket", "id": t_row[0], "title": f"Ticket #{t_row[0]}",
                         "subtitle": (t_row[1] or "")[:80], "link": f"/ordenes-servicio/{t_row[0]}"})

    # Ventas
    sales = db.execute(text(
        "SELECT sale_id, invoice_number FROM sales WHERE invoice_number LIKE :t LIMIT 10"
    ), {"t": term}).fetchall()
    for s in sales:
        results.append({"type": "sale", "id": s[0], "title": f"Venta #{s[0]}",
                         "subtitle": s[1] or "", "link": f"/comercial/ventas/{s[0]}"})

    return results


# ─── SMTP TEST ──────────────────────────────────────────────────────────

@router.post("/smtp/test")
def test_smtp(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Prueba la conexión SMTP configurada en .env."""
    import os, smtplib
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

    host = os.getenv("SMTP_HOST", "")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")

    if not host or not user:
        return {"success": False, "error": "SMTP no configurado en .env"}

    try:
        server = smtplib.SMTP(host, port, timeout=10)
        server.starttls()
        server.login(user, password)
        server.quit()
        return {"success": True, "message": f"Conexión exitosa a {host}:{port}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/smtp/config")
def get_smtp_config(
    current_user: User = Depends(get_current_user)
):
    """Muestra configuración SMTP (sin password)."""
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

    return {
        "host": os.getenv("SMTP_HOST", ""),
        "port": os.getenv("SMTP_PORT", "587"),
        "user": os.getenv("SMTP_USER", ""),
        "from": os.getenv("SMTP_FROM", ""),
        "configured": bool(os.getenv("SMTP_HOST"))
    }


# ─── BACKUPS ────────────────────────────────────────────────────────────

@router.post("/backup")
def create_backup(
    current_user: User = Depends(get_current_user)
):
    """Crea un backup de la base de datos MariaDB."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores pueden crear backups")

    import os, subprocess
    from pathlib import Path

    backup_dir = Path(__file__).resolve().parent.parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"copymart_backup_{timestamp}.sql"
    filepath = backup_dir / filename

    mysqldump = r"C:\Program Files\MariaDB 11.8\bin\mariadb-dump.exe"
    if not os.path.exists(mysqldump):
        mysqldump = r"C:\Program Files\MariaDB 11.8\bin\mysqldump.exe"
    if not os.path.exists(mysqldump):
        return {"success": False, "error": "mariadb-dump no encontrado"}

    try:
        result = subprocess.run(
            [mysqldump, "-u", "root", "copymart"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            return {"success": False, "error": result.stderr}

        filepath.write_text(result.stdout, encoding="utf-8")
        size_mb = round(filepath.stat().st_size / (1024 * 1024), 2)
        return {"success": True, "filename": filename, "size_mb": size_mb,
                "path": str(filepath)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/backups")
def list_backups(
    current_user: User = Depends(get_current_user)
):
    """Lista los backups disponibles."""
    from pathlib import Path

    backup_dir = Path(__file__).resolve().parent.parent.parent / "backups"
    if not backup_dir.exists():
        return []

    backups = []
    for f in sorted(backup_dir.glob("*.sql"), reverse=True):
        backups.append({
            "filename": f.name,
            "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
            "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        })
    return backups


# ─── MIGRACIONES / CHECK DE BD ──────────────────────────────────────────

@router.get("/db/tables")
def get_db_tables(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas las tablas en la base de datos y las esperadas por los modelos."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores")

    inspector = inspect(engine)
    db_tables = set(inspector.get_table_names())
    model_tables = set(Base.metadata.tables.keys())

    missing = model_tables - db_tables
    extra = db_tables - model_tables
    present = model_tables & db_tables

    return {
        "database_tables": sorted(db_tables),
        "model_tables": sorted(model_tables),
        "present": sorted(present),
        "missing": sorted(missing),
        "extra_in_db": sorted(extra)
    }


@router.get("/db/table/{table_name}/columns")
def get_table_columns(
    table_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compara columnas de una tabla en BD vs modelo."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores")

    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise HTTPException(status_code=404, detail=f"Tabla '{table_name}' no existe en BD")

    db_columns = {col["name"]: str(col["type"]) for col in inspector.get_columns(table_name)}

    model_columns = {}
    if table_name in Base.metadata.tables:
        for col in Base.metadata.tables[table_name].columns:
            model_columns[col.name] = str(col.type)

    db_cols_set = set(db_columns.keys())
    model_cols_set = set(model_columns.keys())

    return {
        "table": table_name,
        "db_columns": db_columns,
        "model_columns": model_columns,
        "missing_in_db": sorted(model_cols_set - db_cols_set),
        "extra_in_db": sorted(db_cols_set - model_cols_set),
        "present": sorted(db_cols_set & model_cols_set)
    }


@router.post("/db/migrate")
def run_migration(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea tablas y columnas faltantes basándose en los modelos de SQLAlchemy."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores")

    try:
        Base.metadata.create_all(bind=engine)

        # Verificar estado posterior
        inspector = inspect(engine)
        db_tables = set(inspector.get_table_names())
        model_tables = set(Base.metadata.tables.keys())
        still_missing = model_tables - db_tables

        return {
            "success": True,
            "message": "Migración ejecutada correctamente",
            "tables_created": sorted(model_tables - (db_tables - model_tables)),
            "still_missing": sorted(still_missing)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/db/migrate/employees")
def migrate_employees_table(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Migra la tabla employees: hace user_id nullable y agrega columna nombre."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores")

    results = []
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns("employees")}

    try:
        # Hacer user_id nullable si no lo es ya
        db.execute(text(
            "ALTER TABLE employees MODIFY COLUMN user_id INT NULL"
        ))
        results.append("user_id → nullable OK")
    except Exception as e:
        results.append(f"user_id modify: {e}")

    try:
        if "nombre" not in columns:
            db.execute(text(
                "ALTER TABLE employees ADD COLUMN nombre VARCHAR(255) NULL"
            ))
            results.append("nombre → agregado OK")
        else:
            results.append("nombre → ya existe")
    except Exception as e:
        results.append(f"nombre add: {e}")

    db.commit()
    return {"success": True, "results": results}


@router.post("/db/migrate/users-department")
def migrate_users_department(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Agrega el valor 'ti' al ENUM department de la tabla users."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores")
    try:
        db.execute(text(
            "ALTER TABLE users MODIFY COLUMN department ENUM('rh','administracion','comercial','operaciones','ti') NOT NULL"
        ))
        db.commit()
        return {"success": True, "message": "ENUM department actualizado con valor 'ti'"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}


@router.post("/db/migrate/route-stops")
def migrate_route_stops_table(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Migra la tabla route_stops: agrega columnas visit_status y no_visit_reason."""
    if current_user.rol != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo administradores")

    results = []
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns("route_stops")}

    try:
        if "visit_status" not in columns:
            db.execute(text(
                "ALTER TABLE route_stops ADD COLUMN visit_status VARCHAR(20) NOT NULL DEFAULT 'pendiente'"
            ))
            results.append("visit_status → agregado OK")
        else:
            results.append("visit_status → ya existe")
    except Exception as e:
        results.append(f"visit_status add: {e}")

    try:
        if "no_visit_reason" not in columns:
            db.execute(text(
                "ALTER TABLE route_stops ADD COLUMN no_visit_reason TEXT NULL"
            ))
            results.append("no_visit_reason → agregado OK")
        else:
            results.append("no_visit_reason → ya existe")
    except Exception as e:
        results.append(f"no_visit_reason add: {e}")

    db.commit()
    return {"success": True, "results": results}
