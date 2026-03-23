from fastapi import APIRouter, Depends, status, Query, Body, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from auth.permissions import require_permission
from audit.services import AuditService
from rent.schemas import (
    RentCreate,
    RentUpdate,
    RentResponse,
    RentFilter,
    ContractStatus
)
from rent.services import RentService
from sqlalchemy import func
from rent.models import Rent

router = APIRouter(
    prefix="/rents",
    tags=["Rents"]
)

# crea una renta
@router.post("/", response_model=RentResponse, status_code=status.HTTP_201_CREATED)
def create_rent(
    request: Request,
    rent_data: RentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("rentas", "create"))
):
    rent = RentService.create_rent(db, rent_data, current_user.user_id)
    AuditService.log(
        db,
        user_id=current_user.user_id,
        action="create",
        module="rentas",
        record_id=rent.rent_id,
        detail=f"Renta creada para cliente_id={rent.client_id}",
        ip_address=request.client.host if request.client else None,
    )
    return rent


@router.get("/", response_model=List[RentResponse])
def get_rents(
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    branch_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    area_id: Optional[int] = Query(None, description="Filtrar por área"),
    contract_status: Optional[ContractStatus] = Query(None, description="Filtrar por estado del contrato"),
    is_foreign: Optional[bool] = Query(None, description="Filtrar por servicio foráneo"),
    is_active: Optional[bool] = Query(True, description="Filtrar por rentas activas"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("rentas", "view"))
):
    filters = RentFilter(
        client_id=client_id,
        branch_id=branch_id,
        area_id=area_id,
        contract_status=contract_status,
        is_foreign=is_foreign,
        is_active=is_active
    )
    
    return RentService.get_rents(db, filters, skip, limit)


@router.get("/{rent_id}", response_model=RentResponse)
def get_rent(
    rent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("rentas", "view"))
):
    return RentService.get_rent(db, rent_id)


# Actualiza una renta existente.
@router.put("/{rent_id}", response_model=RentResponse)
def update_rent(
    request: Request,
    rent_id: int,
    rent_data: RentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("rentas", "edit"))
):
    rent = RentService.update_rent(db, rent_id, rent_data)
    AuditService.log(
        db,
        user_id=current_user.user_id,
        action="update",
        module="rentas",
        record_id=rent_id,
        detail="Renta actualizada",
        ip_address=request.client.host if request.client else None,
    )
    return rent

# Desactiva una renta y devuelve el equipo a bodega.
@router.delete("/{rent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rent(
    request: Request,
    rent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("rentas", "delete"))
):
    RentService.delete_rent(db, rent_id)
    AuditService.log(
        db,
        user_id=current_user.user_id,
        action="delete",
        module="rentas",
        record_id=rent_id,
        detail="Renta eliminada/cancelada",
        ip_address=request.client.host if request.client else None,
    )
    return None

# Actualiza el estado del contrato de una renta.
@router.patch("/{rent_id}/status", response_model=RentResponse)
def update_contract_status(
    request: Request,
    rent_id: int,
    contract_status: ContractStatus = Query(..., description="Nuevo estado del contrato"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rent = RentService.update_contract_status(db, rent_id, contract_status)
    AuditService.log(
        db,
        user_id=current_user.user_id,
        action="update",
        module="rentas",
        record_id=rent_id,
        detail=f"Estado de contrato cambiado a: {contract_status}",
        ip_address=request.client.host if request.client else None,
    )
    return rent


@router.get("/client/{client_id}/summary", response_model=dict)
def get_client_rent_summary(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    # Total de rentas activas
    total_active = db.query(func.count(Rent.rent_id)).filter(
        Rent.client_id == client_id,
        Rent.is_active == True
    ).scalar()
    
    # Por estado
    by_status = db.query(
        Rent.contract_status,
        func.count(Rent.rent_id)
    ).filter(
        Rent.client_id == client_id,
        Rent.is_active == True
    ).group_by(Rent.contract_status).all()
    
    # Total de renta mensual
    total_rent = db.query(
        func.sum(Rent.rent)
    ).filter(
        Rent.client_id == client_id,
        Rent.is_active == True,
        Rent.contract_status == ContractStatus.VIGENTE
    ).scalar() or 0
    
    return {
        "client_id": client_id,
        "total_active_rents": total_active,
        "rents_by_status": {status: count for status, count in by_status},
        "total_monthly_rent": float(total_rent)
    }
