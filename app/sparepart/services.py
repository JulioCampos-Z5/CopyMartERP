from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException, status
from typing import Optional
import math
from models import Sparepart
from schemas import SparepartCreate, SparepartUpdate

class SparepartService:
    
    @staticmethod
    def create_sparepart(db: Session, sparepart_data: SparepartCreate) -> Sparepart:
        # Verificar si el código ya existe
        if sparepart_data.code:
            existing = db.query(Sparepart).filter(Sparepart.code == sparepart_data.code).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe una refacción con el código: {sparepart_data.code}"
                )
        
        db_sparepart = Sparepart(**sparepart_data.model_dump())
        db.add(db_sparepart)
        db.commit()
        db.refresh(db_sparepart)
        return db_sparepart
    
    @staticmethod
    def get_sparepart_by_id(db: Session, sparepart_id: int) -> Sparepart:
        sparepart = db.query(Sparepart).filter(Sparepart.sparepart_id == sparepart_id).first()
        if not sparepart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Refacción con ID {sparepart_id} no encontrada"
            )
        return sparepart
    
    @staticmethod
    def get_sparepart_by_code(db: Session, code: str) -> Optional[Sparepart]:
        return db.query(Sparepart).filter(Sparepart.code == code).first()
    
    @staticmethod
    def get_all_spareparts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        brand: Optional[str] = None,
        color: Optional[str] = None,
        supplier: Optional[str] = None
    ) -> tuple[list[Sparepart], int]:
        query = db.query(Sparepart)
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                Sparepart.name.ilike(f"%{search}%"),
                Sparepart.code.ilike(f"%{search}%"),
                Sparepart.description.ilike(f"%{search}%"),
                Sparepart.equipment.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if brand:
            query = query.filter(Sparepart.brand == brand)
        
        if color:
            query = query.filter(Sparepart.color == color)
        
        if supplier:
            query = query.filter(Sparepart.supplier == supplier)
        
        # Obtener total
        total = query.count()
        
        # Aplicar paginación
        spareparts = query.order_by(Sparepart.created_at.desc()).offset(skip).limit(limit).all()
        
        return spareparts, total
    
    @staticmethod
    def update_sparepart(
        db: Session,
        sparepart_id: int,
        sparepart_data: SparepartUpdate
    ) -> Sparepart:
        """Actualizar una refacción"""
        db_sparepart = SparepartService.get_sparepart_by_id(db, sparepart_id)
        
        # Verificar si se está actualizando el código y si ya existe
        if sparepart_data.code and sparepart_data.code != db_sparepart.code:
            existing = db.query(Sparepart).filter(
                Sparepart.code == sparepart_data.code,
                Sparepart.sparepart_id != sparepart_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otra refacción con el código: {sparepart_data.code}"
                )
        
        # Actualizar solo los campos proporcionados
        update_data = sparepart_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sparepart, field, value)
        
        db.commit()
        db.refresh(db_sparepart)
        return db_sparepart
    
    @staticmethod
    def delete_sparepart(db: Session, sparepart_id: int) -> bool:
        """Eliminar una refacción"""
        db_sparepart = SparepartService.get_sparepart_by_id(db, sparepart_id)
        db.delete(db_sparepart)
        db.commit()
        return True
    
    @staticmethod
    def get_brands(db: Session) -> list[str]:
        """Obtener todas las marcas únicas"""
        brands = db.query(Sparepart.brand).distinct().filter(Sparepart.brand.isnot(None)).all()
        return sorted([brand[0] for brand in brands if brand[0]])
    
    @staticmethod
    def get_suppliers(db: Session) -> list[str]:
        """Obtener todos los proveedores únicos"""
        suppliers = db.query(Sparepart.supplier).distinct().filter(Sparepart.supplier.isnot(None)).all()
        return sorted([supplier[0] for supplier in suppliers if supplier[0]])
    
    @staticmethod
    def get_colors(db: Session) -> list[str]:
        """Obtener todos los colores únicos"""
        colors = db.query(Sparepart.color).distinct().filter(Sparepart.color.isnot(None)).all()
        return sorted([color[0] for color in colors if color[0]])