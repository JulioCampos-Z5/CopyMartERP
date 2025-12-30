from sqlalchemy.orm import Session
from equipment.models import Brand, Supplier, Equipment
from equipment.schemas import SupplierCreate, BrandCreate, EquipmentCreate

def create_brand(db: Session, brand_data: BrandCreate):
    brand = Brand(
        name=brand_data.name,
        prefix=brand_data.prefix.lower()
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand

def create_supplier(db: Session, supplier_data: SupplierCreate):
    supplier = Supplier(name=supplier_data.name)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def create_equipment(db: Session, equipment_data: EquipmentCreate):
    brand = db.query(Brand).filter(Brand.brand_id == equipment_data.brand_id).first()
    if not brand:
        raise ValueError("Brand not found")

    last_equipment = (
        db.query(Equipment)
        .filter(Equipment.brand_id == brand.brand_id)
        .order_by(Equipment.item_id.desc())
        .first()
    )
    if last_equipment:
        last_number = int(last_equipment.sku[len(brand.prefix):])
        new_number = last_number + 1
    else:
        new_number = 1

    sku = f"{brand.prefix}{str(new_number).zfill(2)}"

    equipment = Equipment(
        sku=sku,
        brand_id=brand.brand_id,
        model=equipment_data.model,
        serie=equipment_data.serie,
        model_toner=equipment_data.model_toner,
        type=equipment_data.type,
        supplier_id=equipment_data.supplier_id,
        invoice=equipment_data.invoice,
        cost=equipment_data.cost,
        location_status=equipment_data.location_status,
        comments=equipment_data.comments,
        is_active=equipment_data.is_active
    )

    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment

def update_equipment_status(db: Session, item_id: int, new_status: str):
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise ValueError("Equipment not found")
    equipment.location_status = new_status
    db.commit()
    db.refresh(equipment)
    return equipment
