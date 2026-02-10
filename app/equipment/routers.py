from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from equipment.models import Supplier, Equipment, Brand
from equipment.schemas import (
    BrandCreate, BrandRead, BrandUpdate,
    SupplierCreate, SupplierRead, SupplierUpdate,
    EquipmentCreate, EquipmentRead, EquipmentUpdate, EquipmentUpdateFull
)
from equipment.services import (
    create_brand, create_supplier, create_equipment, 
    update_equipment_status, update_equipment_full, delete_equipment,
    update_brand, delete_brand, update_supplier, delete_supplier
)
from core.database import get_db

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"]
)


@router.post("/brands/", response_model=BrandRead)
def add_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    """Crear una nueva marca"""
    try:
        return create_brand(db, brand)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/brands/", response_model=List[BrandRead])
def list_brands(db: Session = Depends(get_db)):
    """Listar todas las marcas"""
    return db.query(Brand).all()

@router.get("/brands/{brand_id}", response_model=BrandRead)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """Obtener una marca por ID"""
    brand = db.query(Brand).filter(Brand.brand_id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.put("/brands/{brand_id}", response_model=BrandRead)
def update_brand_endpoint(
    brand_id: int, 
    brand_update: BrandUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar una marca"""
    try:
        return update_brand(db, brand_id, brand_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/brands/{brand_id}", status_code=204)
def delete_brand_endpoint(brand_id: int, db: Session = Depends(get_db)):
    """Eliminar una marca"""
    try:
        delete_brand(db, brand_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/suppliers/", response_model=SupplierRead)
def add_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Crear un nuevo proveedor"""
    return create_supplier(db, supplier)

@router.get("/suppliers/", response_model=List[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    """Listar todos los proveedores"""
    return db.query(Supplier).all()

@router.get("/suppliers/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Obtener un proveedor por ID"""
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/suppliers/{supplier_id}", response_model=SupplierRead)
def update_supplier_endpoint(
    supplier_id: int, 
    supplier_update: SupplierUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar un proveedor"""
    try:
        return update_supplier(db, supplier_id, supplier_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/suppliers/{supplier_id}", status_code=204)
def delete_supplier_endpoint(supplier_id: int, db: Session = Depends(get_db)):
    """Eliminar un proveedor"""
    try:
        delete_supplier(db, supplier_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/equipment/", response_model=EquipmentRead)
def add_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    """Crear un nuevo equipo"""
    try:
        return create_equipment(db, equipment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/equipment/", response_model=List[EquipmentRead])
def list_equipment(db: Session = Depends(get_db)):
    """Listar todos los equipos"""
    return db.query(Equipment).all()

@router.get("/equipment/{item_id}", response_model=EquipmentRead)
def get_equipment(item_id: int, db: Session = Depends(get_db)):
    """Obtener un equipo por ID"""
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/equipment/{item_id}", response_model=EquipmentRead)
def update_equipment(
    item_id: int, 
    equipment_update: EquipmentUpdateFull, 
    db: Session = Depends(get_db)
):
    """Actualizar un equipo completamente"""
    try:
        return update_equipment_full(db, item_id, equipment_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/equipment/{item_id}/status", response_model=EquipmentRead)
def change_equipment_status(
    item_id: int, 
    update: EquipmentUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar solo el estado de un equipo"""
    if not update.location_status:
        raise HTTPException(status_code=400, detail="Status is required")
    try:
        return update_equipment_status(db, item_id, update.location_status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/equipment/{item_id}", status_code=204)
def delete_equipment_endpoint(item_id: int, db: Session = Depends(get_db)):
    """Eliminar un equipo (soft delete)"""
    try:
        delete_equipment(db, item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))