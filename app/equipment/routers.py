from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from equipment.models import Supplier, Equipment, Brand
from equipment.schemas import (
    BrandCreate, BrandRead, 
    SupplierCreate, SupplierRead, 
    EquipmentCreate, EquipmentRead, EquipmentUpdate
)
from equipment.services import create_brand, create_supplier, create_equipment, update_equipment_status
from core.database import get_db

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

@router.patch("/equipment/{item_id}/status", response_model=EquipmentRead)
def change_equipment_status(item_id: int, update: EquipmentUpdate, db: Session = Depends(get_db)):
    if not update.location_status:
        raise HTTPException(status_code=400, detail="Status is required")
    try:
        return update_equipment_status(db, item_id, update.location_status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
