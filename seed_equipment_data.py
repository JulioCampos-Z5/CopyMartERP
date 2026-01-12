"""
Script para generar datos de ejemplo en la base de datos de equipos
Ejecutar con: python seed_equipment_data.py
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.equipment.models import Brand, Supplier, Equipment, TypeColor, LocationStatus
from datetime import datetime

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Crear marcas
        print("Creando marcas...")
        brands_data = [
            {"name": "Canon", "prefix": "CAN"},
            {"name": "HP", "prefix": "HP"},
            {"name": "Xerox", "prefix": "XER"},
            {"name": "Ricoh", "prefix": "RIC"},
            {"name": "Konica Minolta", "prefix": "KM"},
            {"name": "Brother", "prefix": "BRO"},
            {"name": "Epson", "prefix": "EPS"},
            {"name": "Samsung", "prefix": "SAM"}
        ]
        
        brands = []
        for brand_data in brands_data:
            # Verificar si ya existe
            existing = db.query(Brand).filter(Brand.name == brand_data["name"]).first()
            if not existing:
                brand = Brand(**brand_data)
                db.add(brand)
                db.flush()
                brands.append(brand)
                print(f"  ✓ Marca creada: {brand.name}")
            else:
                brands.append(existing)
                print(f"  - Marca ya existe: {existing.name}")
        
        db.commit()
        
        # Crear proveedores
        print("\nCreando proveedores...")
        suppliers_data = [
            {"name": "Distribuidora TecnoOffice"},
            {"name": "Suministros Industriales SA"},
            {"name": "ImportMex"},
            {"name": "Global Office Solutions"},
            {"name": "Proveedora Nacional"}
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            existing = db.query(Supplier).filter(Supplier.name == supplier_data["name"]).first()
            if not existing:
                supplier = Supplier(**supplier_data)
                db.add(supplier)
                db.flush()
                suppliers.append(supplier)
                print(f"  ✓ Proveedor creado: {supplier.name}")
            else:
                suppliers.append(existing)
                print(f"  - Proveedor ya existe: {existing.name}")
        
        db.commit()
        
        # Crear equipos
        print("\nCreando equipos...")
        equipments_data = [
            # Canon
            {
                "brand_id": brands[0].brand_id,
                "model": "imageRUNNER ADVANCE C5535i",
                "serie": "FKG12345",
                "model_toner": "C-EXV49",
                "type": TypeColor.COLOR,
                "supplier_id": suppliers[0].supplier_id,
                "invoice": "FAC-2024-001",
                "cost": 125000.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Equipo nuevo, recién llegado"
            },
            {
                "brand_id": brands[0].brand_id,
                "model": "imageRUNNER 2525i",
                "serie": "FKG12346",
                "model_toner": "C-EXV33",
                "type": TypeColor.MONOCROMO,
                "supplier_id": suppliers[0].supplier_id,
                "invoice": "FAC-2024-002",
                "cost": 45000.00,
                "location_status": LocationStatus.ASIGNADO,
                "comments": "Asignado a cliente Acme Corp"
            },
            # HP
            {
                "brand_id": brands[1].brand_id,
                "model": "LaserJet Pro MFP M428fdw",
                "serie": "VNB5Q12345",
                "model_toner": "CF259A",
                "type": TypeColor.MONOCROMO,
                "supplier_id": suppliers[1].supplier_id,
                "invoice": "FAC-2024-003",
                "cost": 15000.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Equipo listo para renta"
            },
            {
                "brand_id": brands[1].brand_id,
                "model": "Color LaserJet Pro M479fdw",
                "serie": "VNB5Q12346",
                "model_toner": "CF410A",
                "type": TypeColor.COLOR,
                "supplier_id": suppliers[1].supplier_id,
                "invoice": "FAC-2024-004",
                "cost": 22000.00,
                "location_status": LocationStatus.TALLER,
                "comments": "En mantenimiento preventivo"
            },
            # Xerox
            {
                "brand_id": brands[2].brand_id,
                "model": "VersaLink C405",
                "serie": "XER123456",
                "model_toner": "106R03532",
                "type": TypeColor.COLOR,
                "supplier_id": suppliers[2].supplier_id,
                "invoice": "FAC-2024-005",
                "cost": 35000.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Multifuncional a color"
            },
            {
                "brand_id": brands[2].brand_id,
                "model": "WorkCentre 3335",
                "serie": "XER123457",
                "model_toner": "106R03621",
                "type": TypeColor.MONOCROMO,
                "supplier_id": suppliers[2].supplier_id,
                "invoice": "FAC-2024-006",
                "cost": 12000.00,
                "location_status": LocationStatus.VENDIDO,
                "comments": "Vendido a cliente XYZ"
            },
            # Ricoh
            {
                "brand_id": brands[3].brand_id,
                "model": "MP C3004ex",
                "serie": "RIC123456",
                "model_toner": "841817",
                "type": TypeColor.COLOR,
                "supplier_id": suppliers[3].supplier_id,
                "invoice": "FAC-2024-007",
                "cost": 65000.00,
                "location_status": LocationStatus.ASIGNADO,
                "comments": "Rentado a oficinas centrales"
            },
            # Konica Minolta
            {
                "brand_id": brands[4].brand_id,
                "model": "bizhub C258",
                "serie": "KM123456",
                "model_toner": "TN-324K",
                "type": TypeColor.COLOR,
                "supplier_id": suppliers[3].supplier_id,
                "invoice": "FAC-2024-008",
                "cost": 55000.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Multifuncional color de alto volumen"
            },
            {
                "brand_id": brands[4].brand_id,
                "model": "bizhub 4050",
                "serie": "KM123457",
                "model_toner": "TN-512",
                "type": TypeColor.MONOCROMO,
                "supplier_id": suppliers[3].supplier_id,
                "invoice": "FAC-2024-009",
                "cost": 18000.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Compacta y eficiente"
            },
            # Brother
            {
                "brand_id": brands[5].brand_id,
                "model": "MFC-L5900DW",
                "serie": "BRO123456",
                "model_toner": "TN-880",
                "type": TypeColor.MONOCROMO,
                "supplier_id": suppliers[4].supplier_id,
                "invoice": "FAC-2024-010",
                "cost": 8500.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Impresora láser monocromo"
            },
            # Epson
            {
                "brand_id": brands[6].brand_id,
                "model": "WorkForce Pro WF-C5790",
                "serie": "EPS123456",
                "model_toner": "T9451",
                "type": TypeColor.COLOR,
                "supplier_id": suppliers[4].supplier_id,
                "invoice": "FAC-2024-011",
                "cost": 16000.00,
                "location_status": LocationStatus.ASIGNADO,
                "comments": "Inyección de tinta empresarial"
            },
            # Samsung
            {
                "brand_id": brands[7].brand_id,
                "model": "ProXpress M4020ND",
                "serie": "SAM123456",
                "model_toner": "MLT-D203L",
                "type": TypeColor.MONOCROMO,
                "supplier_id": suppliers[0].supplier_id,
                "invoice": "FAC-2024-012",
                "cost": 7500.00,
                "location_status": LocationStatus.BODEGA,
                "comments": "Impresora láser compacta"
            }
        ]
        
        for eq_data in equipments_data:
            # Verificar si ya existe por número de serie
            existing = db.query(Equipment).filter(Equipment.serie == eq_data["serie"]).first()
            if not existing:
                equipment = Equipment(**eq_data)
                db.add(equipment)
                db.flush()
                print(f"  ✓ Equipo creado: {equipment.model} (Serie: {equipment.serie})")
            else:
                print(f"  - Equipo ya existe: {existing.model} (Serie: {existing.serie})")
        
        db.commit()
        
        print("\n✅ Datos de ejemplo creados exitosamente!")
        
        # Mostrar resumen
        total_brands = db.query(Brand).count()
        total_suppliers = db.query(Supplier).count()
        total_equipment = db.query(Equipment).count()
        
        print(f"\n📊 Resumen:")
        print(f"   Marcas: {total_brands}")
        print(f"   Proveedores: {total_suppliers}")
        print(f"   Equipos: {total_equipment}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de datos de ejemplo...\n")
    create_sample_data()
