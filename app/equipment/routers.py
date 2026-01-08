from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .models import Supplier, Equipment, Brand
from .schemas import (
    BrandCreate, BrandRead, 
    SupplierCreate, SupplierRead, 
    EquipmentCreate, EquipmentRead, EquipmentUpdate
)
from .services import create_brand, create_supplier, create_equipment, update_equipment_status
from ..core.database import get_db

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"]
)

# BRAND 
@router.post("/brands/", response_model=BrandRead)
def add_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return create_brand(db, brand)

@router.get("/brands/", response_model=List[BrandRead])
def list_brands(db: Session = Depends(get_db)):
    return db.query(Brand).all()

@router.delete("/brands/{brand_id}/")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.brand_id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    db.delete(brand)
    db.commit()
    return {"message": "Brand deleted successfully"}

# SUPPLIER 
@router.post("/suppliers/", response_model=SupplierRead)
def add_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(db, supplier)

@router.get("/suppliers/", response_model=List[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

# EQUIPMENT 
@router.post("/equipment/", response_model=EquipmentRead)
def add_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    try:
        return create_equipment(db, equipment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/equipment/", response_model=List[EquipmentRead])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).all()

@router.get("/equipment/{item_id}/", response_model=EquipmentRead)
def get_equipment(item_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/equipment/{item_id}/", response_model=EquipmentRead)
def update_equipment(item_id: int, equipment_update: EquipmentUpdate, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Actualizar campos
    for key, value in equipment_update.dict(exclude_unset=True).items():
        setattr(equipment, key, value)
    
    db.commit()
    db.refresh(equipment)
    return equipment

@router.delete("/equipment/{item_id}/")
def delete_equipment(item_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted successfully"}

@router.patch("/equipment/{item_id}/status", response_model=EquipmentRead)
def change_equipment_status(item_id: int, update: EquipmentUpdate, db: Session = Depends(get_db)):
    if not update.location_status:
        raise HTTPException(status_code=400, detail="Status is required")
    try:
        return update_equipment_status(db, item_id, update.location_status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
