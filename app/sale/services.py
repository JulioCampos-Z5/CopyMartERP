from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

from app.sale.models import Sale, SaleStatus
from app.sale.schemas import SaleCreate, SaleUpdate, SaleResponse, SaleFilter
from app.client.models import Client, Branch, Area
from app.equipment.models import Equipment, LocationStatus


class SaleService:
    
    @staticmethod
    def generate_invoice_number(sale_id: int, created_at: datetime) -> str:
        """Genera número de factura en formato CAT-XX-MM-YY-V"""
        month = created_at.strftime("%m")
        year = created_at.strftime("%y")
        return f"CAT-{sale_id:02d}-{month}-{year}-V"
    
    @staticmethod
    def validate_assignment(
        db: Session, 
        client_id: int, 
        branch_id: Optional[int], 
        area_id: Optional[int]
    ) -> None:
        """Valida que las relaciones jerárquicas sean correctas"""
        
        # Validar que el cliente existe
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {client_id} no encontrado"
            )
        
        # Si se proporciona sucursal, validar que pertenece al cliente
        if branch_id:
            branch = db.query(Branch).filter(
                and_(
                    Branch.branch_id == branch_id,
                    Branch.client_id == client_id
                )
            ).first()
            if not branch:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La sucursal {branch_id} no pertenece al cliente {client_id}"
                )
        
        # Si se proporciona área, validar
        if area_id:
            area = db.query(Area).filter(Area.area_id == area_id).first()
            if not area:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Área con ID {area_id} no encontrada"
                )
            
            # Validar que el área pertenece al cliente a través de la sucursal
            area_branch = db.query(Branch).filter(Branch.branch_id == area.branch_id).first()
            if area_branch and area_branch.client_id != client_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El área {area_id} no pertenece al cliente {client_id}"
                )
            
            # Si se especificó sucursal, validar que el área pertenece a esa sucursal
            if branch_id and area.branch_id != branch_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El área {area_id} no pertenece a la sucursal {branch_id}"
                )
    
    @staticmethod
    def validate_equipment(db: Session, item_id: int) -> Equipment:
        """Valida que el equipo existe y está disponible para venta"""
        equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {item_id} no encontrado"
            )
        
        # Verificar si el equipo ya está vendido
        active_sale = db.query(Sale).filter(
            and_(
                Sale.item_id == item_id,
                Sale.is_active == True,
                Sale.sale_status.in_([
                    SaleStatus.CONFIRMADA,
                    SaleStatus.ENTREGADA
                ])
            )
        ).first()
        
        if active_sale:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El equipo ya fue vendido (Venta ID: {active_sale.sale_id})"
            )
        
        return equipment
    
    @staticmethod
    def create_sale(
        db: Session, 
        sale_data: SaleCreate,
        current_user_id: Optional[int] = None
    ) -> Sale:
        
        # Validar asignación
        SaleService.validate_assignment(
            db, 
            sale_data.client_id,
            sale_data.branch_id,
            sale_data.area_id
        )
        
        # Validar equipo
        SaleService.validate_equipment(db, sale_data.item_id)
        
        # Crear venta 
        new_sale = Sale(
            **sale_data.dict(),
            created_by=current_user_id
        )
        
        db.add(new_sale)
        db.flush() 
        
        # Generar número de factura
        new_sale.invoice_number = SaleService.generate_invoice_number(
            new_sale.sale_id, 
            new_sale.created_at
        )
        
        # Actualizar estado del equipo a vendido
        equipment = db.query(Equipment).filter(Equipment.item_id == sale_data.item_id).first()
        equipment.location_status = LocationStatus.VENDIDO
        
        db.commit()
        db.refresh(new_sale)
        
        return new_sale
    
    @staticmethod
    def get_sale(db: Session, sale_id: int) -> Sale:
        sale = db.query(Sale).options(
            joinedload(Sale.client),
            joinedload(Sale.branch),
            joinedload(Sale.area),
            joinedload(Sale.equipment)
        ).filter(Sale.sale_id == sale_id).first()
        
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con ID {sale_id} no encontrada"
            )
        
        return sale
    
    @staticmethod
    def get_sales(
        db: Session,
        filters: SaleFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[Sale]:
        query = db.query(Sale).options(
            joinedload(Sale.client),
            joinedload(Sale.branch),
            joinedload(Sale.area),
            joinedload(Sale.equipment)
        )
        
        # Aplicar filtros
        if filters.client_id:
            query = query.filter(Sale.client_id == filters.client_id)
        
        if filters.branch_id:
            query = query.filter(Sale.branch_id == filters.branch_id)
        
        if filters.area_id:
            query = query.filter(Sale.area_id == filters.area_id)
        
        if filters.sale_status:
            query = query.filter(Sale.sale_status == filters.sale_status)
        
        if filters.is_foreign is not None:
            query = query.filter(Sale.is_foreign == filters.is_foreign)
        
        if filters.is_active is not None:
            query = query.filter(Sale.is_active == filters.is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_sale(
        db: Session,
        sale_id: int,
        sale_data: SaleUpdate
    ) -> Sale:
        """Actualiza una venta"""
        sale = SaleService.get_sale(db, sale_id)
        
        update_data = sale_data.dict(exclude_unset=True)
        
        # Si se actualizan branch_id o area_id, validar
        if 'branch_id' in update_data or 'area_id' in update_data:
            new_branch_id = update_data.get('branch_id', sale.branch_id)
            new_area_id = update_data.get('area_id', sale.area_id)
            SaleService.validate_assignment(
                db,
                sale.client_id,
                new_branch_id,
                new_area_id
            )
        
        # Actualizar campos
        for field, value in update_data.items():
            setattr(sale, field, value)
        
        sale.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(sale)
        
        return sale
    
    @staticmethod
    def delete_sale(db: Session, sale_id: int) -> None:
        """Elimina una venta y devuelve el equipo a bodega"""
        sale = SaleService.get_sale(db, sale_id)
        
        # Solo se puede cancelar si no ha sido entregada
        if sale.sale_status == SaleStatus.ENTREGADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cancelar una venta ya entregada"
            )
        
        sale.is_active = False
        sale.sale_status = SaleStatus.CANCELADA
        
        # Devolver el equipo a BODEGA
        equipment = db.query(Equipment).filter(Equipment.item_id == sale.item_id).first()
        if equipment:
            equipment.location_status = LocationStatus.BODEGA
        
        db.commit()
    
    @staticmethod
    def update_sale_status(
        db: Session,
        sale_id: int,
        new_status: SaleStatus
    ) -> Sale:
        """Actualiza el estado de una venta"""
        sale = SaleService.get_sale(db, sale_id)
        
        # Validar transiciones de estado
        if sale.sale_status == SaleStatus.CANCELADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar una venta cancelada"
            )
        
        if sale.sale_status == SaleStatus.ENTREGADA and new_status != SaleStatus.ENTREGADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cambiar el estado de una venta ya entregada"
            )
        
        sale.sale_status = new_status
        sale.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(sale)
        
        return sale