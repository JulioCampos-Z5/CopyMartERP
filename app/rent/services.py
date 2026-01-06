from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

from .models import Rent, ContractStatus
from .schemas import RentCreate, RentUpdate, RentResponse, RentFilter
from ..client.models import Client, Branch, Area
from ..equipment.models import Equipment, LocationStatus


class RentService:
    
    @staticmethod
    def generate_contract_number(rent_id: int, created_at: datetime) -> str:
        month = created_at.strftime("%m")
        year = created_at.strftime("%y")
        return f"CAT-{rent_id:02d}-{month}-{year}-R"
    
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
            
            # Validar que el área pertenece al cliente
            if area.client_id != client_id:
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
        """Valida que el equipo existe y está disponible"""
        equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {item_id} no encontrado"
            )
        
        # Verificar si el equipo ya está asignado a otra renta activa
        active_rent = db.query(Rent).filter(
            and_(
                Rent.item_id == item_id,
                Rent.is_active == True,
                Rent.contract_status.in_([
                    ContractStatus.VIGENTE,
                    ContractStatus.PENDIENTE,
                    ContractStatus.SIN_FIRMAR
                ])
            )
        ).first()
        
        if active_rent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El equipo ya está asignado a otra renta activa (ID: {active_rent.rent_id})"
            )
        
        return equipment
    
    @staticmethod
    def create_rent(
        db: Session, 
        rent_data: RentCreate,
        current_user_id: Optional[int] = None
    ) -> Rent:
        
        # Validar asignación
        RentService.validate_assignment(
            db, 
            rent_data.client_id,
            rent_data.branch_id,
            rent_data.area_id
        )
        
        # Validar equipo
        RentService.validate_equipment(db, rent_data.item_id)
        
        # Crear renta 
        new_rent = Rent(
            **rent_data.dict(),
            created_by=current_user_id
        )
        
        db.add(new_rent)
        db.flush() 
        
        # Generar número de contrato
        new_rent.contract_number = RentService.generate_contract_number(
            new_rent.rent_id, 
            new_rent.created_at
        )
        
        # Actualizar estado del equipo a ASIGNADO
        equipment = db.query(Equipment).filter(Equipment.item_id == rent_data.item_id).first()
        equipment.location_status = LocationStatus.ASIGNADO
        
        db.commit()
        db.refresh(new_rent)
        
        return new_rent
    
    @staticmethod
    def get_rent(db: Session, rent_id: int) -> Rent:
        rent = db.query(Rent).options(
            joinedload(Rent.client),
            joinedload(Rent.branch),
            joinedload(Rent.area),
            joinedload(Rent.equipment)
        ).filter(Rent.rent_id == rent_id).first()
        
        if not rent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Renta con ID {rent_id} no encontrada"
            )
        
        return rent
    
    @staticmethod
    def get_rents(
        db: Session,
        filters: RentFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[Rent]:
        query = db.query(Rent).options(
            joinedload(Rent.client),
            joinedload(Rent.branch),
            joinedload(Rent.area),
            joinedload(Rent.equipment)
        )
        
        # Aplicar filtros
        if filters.client_id:
            query = query.filter(Rent.client_id == filters.client_id)
        
        if filters.branch_id:
            query = query.filter(Rent.branch_id == filters.branch_id)
        
        if filters.area_id:
            query = query.filter(Rent.area_id == filters.area_id)
        
        if filters.contract_status:
            query = query.filter(Rent.contract_status == filters.contract_status)
        
        if filters.is_foreign is not None:
            query = query.filter(Rent.is_foreign == filters.is_foreign)
        
        if filters.is_active is not None:
            query = query.filter(Rent.is_active == filters.is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_rent(
        db: Session,
        rent_id: int,
        rent_data: RentUpdate
    ) -> Rent:
        """Actualiza una renta"""
        rent = RentService.get_rent(db, rent_id)
        
        update_data = rent_data.dict(exclude_unset=True)
        
        # Si se actualizan branch_id o area_id, validar
        if 'branch_id' in update_data or 'area_id' in update_data:
            new_branch_id = update_data.get('branch_id', rent.branch_id)
            new_area_id = update_data.get('area_id', rent.area_id)
            RentService.validate_assignment(
                db,
                rent.client_id,
                new_branch_id,
                new_area_id
            )
        
        # Actualizar campos
        for field, value in update_data.items():
            setattr(rent, field, value)
        
        rent.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(rent)
        
        return rent
    
    @staticmethod
    def delete_rent(db: Session, rent_id: int) -> None:
        """Elimina (desactiva) una renta"""
        rent = RentService.get_rent(db, rent_id)
        rent.is_active = False
        
        # Devolver el equipo a BODEGA
        equipment = db.query(Equipment).filter(Equipment.item_id == rent.item_id).first()
        if equipment:
            equipment.location_status = LocationStatus.BODEGA
        
        db.commit()
    
    @staticmethod
    def update_contract_status(
        db: Session,
        rent_id: int,
        new_status: ContractStatus
    ) -> Rent:
        rent = RentService.get_rent(db, rent_id)
        rent.contract_status = new_status
        rent.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(rent)
        
        return rent
