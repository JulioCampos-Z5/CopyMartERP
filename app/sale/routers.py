from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..auth.routers import get_current_user
from ..auth.models import User
from .schemas import (
    SaleCreate,
    SaleUpdate,
    SaleResponse,
    SaleFilter,
    SaleStatus
)
from .services import SaleService
from sqlalchemy import func
from .models import Sale

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una nueva venta"""
    return SaleService.create_sale(
        db, 
        sale_data, 
        current_user.user_id
    )


@router.get("/", response_model=List[SaleResponse])
def get_sales(
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    branch_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    area_id: Optional[int] = Query(None, description="Filtrar por área"),
    sale_status: Optional[SaleStatus] = Query(None, description="Filtrar por estado de la venta"),
    is_foreign: Optional[bool] = Query(None, description="Filtrar por servicio foráneo"),
    is_active: Optional[bool] = Query(True, description="Filtrar por ventas activas"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene lista de ventas con filtros opcionales"""
    filters = SaleFilter(
        client_id=client_id,
        branch_id=branch_id,
        area_id=area_id,
        sale_status=sale_status,
        is_foreign=is_foreign,
        is_active=is_active
    )
    
    return SaleService.get_sales(db, filters, skip, limit)


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene una venta por ID"""
    return SaleService.get_sale(db, sale_id)


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    sale_data: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza una venta existente"""
    return SaleService.update_sale(db, sale_id, sale_data)


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancela una venta y devuelve el equipo a bodega"""
    SaleService.delete_sale(db, sale_id)
    return None


@router.patch("/{sale_id}/status", response_model=SaleResponse)
def update_sale_status(
    sale_id: int,
    new_status: SaleStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza el estado de una venta"""
    return SaleService.update_sale_status(db, sale_id, new_status)


@router.get("/client/{client_id}/summary", response_model=dict)
def get_client_sale_summary(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene resumen de ventas de un cliente"""
    
    # Total de ventas activas
    total_active = db.query(func.count(Sale.sale_id)).filter(
        Sale.client_id == client_id,
        Sale.is_active == True
    ).scalar()
    
    # Por estado
    by_status = db.query(
        Sale.sale_status,
        func.count(Sale.sale_id)
    ).filter(
        Sale.client_id == client_id,
        Sale.is_active == True
    ).group_by(Sale.sale_status).all()
    
    # Total de ventas confirmadas y entregadas
    total_sales_amount = db.query(
        func.sum(Sale.sale_price)
    ).filter(
        Sale.client_id == client_id,
        Sale.is_active == True,
        Sale.sale_status.in_([SaleStatus.CONFIRMADA, SaleStatus.ENTREGADA])
    ).scalar() or 0
    
    return {
        "client_id": client_id,
        "total_active_sales": total_active,
        "sales_by_status": {status: count for status, count in by_status},
        "total_sales_amount": float(total_sales_amount)
    }
