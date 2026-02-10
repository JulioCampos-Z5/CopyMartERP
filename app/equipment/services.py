from sqlalchemy.orm import Session
from equipment.models import Brand, Supplier, Equipment
from equipment.schemas import (
    SupplierCreate, BrandCreate, EquipmentCreate, 
    BrandUpdate, SupplierUpdate, EquipmentUpdateFull
)

def create_brand(db: Session, brand_data: BrandCreate):
    """Crear una nueva marca"""
    # Verificar si el prefijo ya existe
    existing = db.query(Brand).filter(Brand.prefix == brand_data.prefix.lower()).first()
    if existing:
        raise ValueError("Brand prefix already exists")
    
    brand = Brand(
        name=brand_data.name,
        prefix=brand_data.prefix.lower()
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand

def update_brand(db: Session, brand_id: int, brand_data: BrandUpdate):
    """Actualizar una marca"""
    brand = db.query(Brand).filter(Brand.brand_id == brand_id).first()
    if not brand:
        raise ValueError("Brand not found")
    
    update_data = brand_data.dict(exclude_unset=True)
    
    # Verificar si el nuevo prefijo ya existe
    if 'prefix' in update_data:
        update_data['prefix'] = update_data['prefix'].lower()
        existing = db.query(Brand).filter(
            Brand.prefix == update_data['prefix'],
            Brand.brand_id != brand_id
        ).first()
        if existing:
            raise ValueError("Brand prefix already exists")
    
    for field, value in update_data.items():
        setattr(brand, field, value)
    
    db.commit()
    db.refresh(brand)
    return brand

def delete_brand(db: Session, brand_id: int):
    """Eliminar una marca"""
    brand = db.query(Brand).filter(Brand.brand_id == brand_id).first()
    if not brand:
        raise ValueError("Brand not found")
    
    # Verificar si tiene equipos asociados
    has_equipment = db.query(Equipment).filter(Equipment.brand_id == brand_id).first()
    if has_equipment:
        raise ValueError("Cannot delete brand with associated equipment")
    
    db.delete(brand)
    db.commit()


def create_supplier(db: Session, supplier_data: SupplierCreate):
    """Crear un nuevo proveedor"""
    supplier = Supplier(name=supplier_data.name)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def update_supplier(db: Session, supplier_id: int, supplier_data: SupplierUpdate):
    """Actualizar un proveedor"""
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise ValueError("Supplier not found")
    
    update_data = supplier_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    return supplier

def delete_supplier(db: Session, supplier_id: int):
    """Eliminar un proveedor"""
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise ValueError("Supplier not found")
    
    # Verificar si tiene equipos asociados
    has_equipment = db.query(Equipment).filter(Equipment.supplier_id == supplier_id).first()
    if has_equipment:
        raise ValueError("Cannot delete supplier with associated equipment")
    
    db.delete(supplier)
    db.commit()


def create_equipment(db: Session, equipment_data: EquipmentCreate):
    """Crear un nuevo equipo"""
    # Verificar que la marca exista
    brand = db.query(Brand).filter(Brand.brand_id == equipment_data.brand_id).first()
    if not brand:
        raise ValueError("Brand not found")
    
    # Verificar que el proveedor exista
    supplier = db.query(Supplier).filter(Supplier.supplier_id == equipment_data.supplier_id).first()
    if not supplier:
        raise ValueError("Supplier not found")
    
    # Verificar que la serie no exista
    existing_serie = db.query(Equipment).filter(Equipment.serie == equipment_data.serie).first()
    if existing_serie:
        raise ValueError("Serie already exists")

    # Generar SKU automático
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
    """Actualizar solo el estado de un equipo"""
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise ValueError("Equipment not found")
    
    equipment.location_status = new_status
    db.commit()
    db.refresh(equipment)
    return equipment

def update_equipment_full(db: Session, item_id: int, equipment_data: EquipmentUpdateFull):
    """Actualizar todos los campos de un equipo"""
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise ValueError("Equipment not found")
    
    update_data = equipment_data.dict(exclude_unset=True)
    
    # Validar que la serie no esté duplicada si se está actualizando
    if 'serie' in update_data and update_data['serie'] != equipment.serie:
        existing = db.query(Equipment).filter(
            Equipment.serie == update_data['serie'],
            Equipment.item_id != item_id
        ).first()
        if existing:
            raise ValueError("Serie already exists")
    
    # Validar que el supplier exista si se está actualizando
    if 'supplier_id' in update_data:
        supplier = db.query(Supplier).filter(
            Supplier.supplier_id == update_data['supplier_id']
        ).first()
        if not supplier:
            raise ValueError("Supplier not found")
    
    for field, value in update_data.items():
        setattr(equipment, field, value)
    
    db.commit()
    db.refresh(equipment)
    return equipment

def delete_equipment(db: Session, item_id: int):
    """Soft delete de un equipo (marca is_active = False)"""
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise ValueError("Equipment not found")
    
    # Soft delete
    equipment.is_active = False
    db.commit()