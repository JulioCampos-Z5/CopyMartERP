import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
os.chdir(os.path.join(os.path.dirname(__file__), 'app'))

from core.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    stmts = [
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS authorized_amount INT NULL AFTER amount",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier1_name VARCHAR(255) NULL AFTER type",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier1_cost DECIMAL(10,2) NULL AFTER supplier1_name",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier2_name VARCHAR(255) NULL AFTER supplier1_cost",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier2_cost DECIMAL(10,2) NULL AFTER supplier2_name",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier3_name VARCHAR(255) NULL AFTER supplier2_cost",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier3_cost DECIMAL(10,2) NULL AFTER supplier3_name",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS authorized_by_area_chief_id INT NULL AFTER supplier3_cost",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS authorized_by_area_chief_date DATETIME NULL AFTER authorized_by_area_chief_id",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS authorized_by_admin_id INT NULL AFTER authorized_by_area_chief_date",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS authorized_by_admin_date DATETIME NULL AFTER authorized_by_admin_id",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS quotation_file VARCHAR(500) NULL AFTER authorized_by_admin_date",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier_payment_file VARCHAR(500) NULL AFTER quotation_file",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS supplier_invoice_file VARCHAR(500) NULL AFTER supplier_payment_file",
        "ALTER TABLE purchases ADD COLUMN IF NOT EXISTS is_paid TINYINT(1) NULL AFTER supplier_invoice_file",
        # Add foreign keys if they don't exist
        "ALTER TABLE purchases ADD INDEX IF NOT EXISTS idx_chief (authorized_by_area_chief_id)",
        "ALTER TABLE purchases ADD INDEX IF NOT EXISTS idx_admin (authorized_by_admin_id)",
    ]
    for s in stmts:
        try:
            db.execute(text(s))
            print(f"OK: {s[:70]}...")
        except Exception as e:
            print(f"SKIP: {s[:70]}... ({e})")
    
    # Fix enum values - model uses display values, DB uses member names
    db.execute(text(
        "ALTER TABLE purchases MODIFY COLUMN type "
        "ENUM('INTERNA','VENTA') NOT NULL DEFAULT 'INTERNA'"
    ))
    db.execute(text(
        "ALTER TABLE purchases MODIFY COLUMN status "
        "ENUM('PAUSADO_BACK_ORDERS','EN_TRANSITO','SOLICITUD_GUIA_ALMACEN',"
        "'FALTA_PAGO_PROVEEDOR','FALTA_FACTURA','EN_CURSO','POR_REVISAR',"
        "'FALTA_AUTORIZACION','RECHAZADO','FALTA_ORDEN_SERVICIO','CONCLUIDO') "
        "NOT NULL DEFAULT 'EN_CURSO'"
    ))
    
    db.commit()
    print("\nAll columns added. Current schema:")
    result = db.execute(text("DESCRIBE purchases"))
    for row in result:
        print(f"  {row}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
