from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from billing.schemas import (
    BillingCreate,
    BillingUpdate,
    BillingResponse,
    BillingFilter,
    BillingStatus,
    BillingType,
    BillingBatchCreate,
    BillingPayment,
    BillingStats
)
from billing.services import BillingService

router = APIRouter(
    prefix="/billings",
    tags=["Billings"]
)


@router.post("/", response_model=BillingResponse, status_code=status.HTTP_201_CREATED)
def create_billing(
    billing_data: BillingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una facturación individual"""
    return BillingService.create_billing(
        db, 
        billing_data, 
        current_user.user_id
    )


@router.post("/batch", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_billing_batch(
    batch_data: BillingBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Genera facturación masiva para rentas activas"""
    return BillingService.create_billing_batch(
        db,
        batch_data,
        current_user.user_id
    )


@router.get("/", response_model=List[BillingResponse])
def get_billings(
    billing_type: Optional[BillingType] = Query(None, description="Filtrar por tipo"),
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    branch_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    area_id: Optional[int] = Query(None, description="Filtrar por área"),
    status: Optional[BillingStatus] = Query(None, description="Filtrar por estado"),
    follow_up: Optional[bool] = Query(None, description="Filtrar por seguimiento"),
    is_active: Optional[bool] = Query(True, description="Filtrar por activas"),
    date_from: Optional[date] = Query(None, description="Fecha desde (target_date)"),
    date_to: Optional[date] = Query(None, description="Fecha hasta (target_date)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene lista de facturaciones con filtros opcionales"""
    filters = BillingFilter(
        billing_type=billing_type,
        client_id=client_id,
        branch_id=branch_id,
        area_id=area_id,
        status=status,
        follow_up=follow_up,
        is_active=is_active,
        date_from=date_from,
        date_to=date_to
    )
    
    return BillingService.get_billings(db, filters, skip, limit)


@router.get("/overdue", response_model=List[BillingResponse])
def get_overdue_billings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene facturaciones vencidas"""
    filters = BillingFilter(
        status=BillingStatus.VENCIDO,
        is_active=True
    )
    
    return BillingService.get_billings(db, filters, skip, limit)


@router.get("/pending", response_model=List[BillingResponse])
def get_pending_billings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene facturaciones pendientes"""
    filters = BillingFilter(
        status=BillingStatus.PENDIENTE,
        is_active=True
    )
    
    return BillingService.get_billings(db, filters, skip, limit)


@router.get("/follow-up", response_model=List[BillingResponse])
def get_follow_up_billings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene facturaciones que requieren seguimiento"""
    filters = BillingFilter(
        follow_up=True,
        is_active=True
    )
    
    return BillingService.get_billings(db, filters, skip, limit)


@router.get("/stats", response_model=BillingStats)
def get_billing_stats(
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    date_from: Optional[date] = Query(None, description="Fecha desde"),
    date_to: Optional[date] = Query(None, description="Fecha hasta"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene estadísticas de facturación"""
    return BillingService.get_billing_stats(db, client_id, date_from, date_to)


@router.get("/{billing_id}", response_model=BillingResponse)
def get_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene una facturación por ID"""
    return BillingService.get_billing(db, billing_id)


@router.put("/{billing_id}", response_model=BillingResponse)
def update_billing(
    billing_id: int,
    billing_data: BillingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza una facturación"""
    return BillingService.update_billing(db, billing_id, billing_data)


@router.patch("/{billing_id}/pay", response_model=BillingResponse)
def mark_billing_as_paid(
    billing_id: int,
    payment_data: BillingPayment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marca una facturación como pagada"""
    return BillingService.mark_as_paid(db, billing_id, payment_data)


@router.patch("/{billing_id}/follow-up", response_model=BillingResponse)
def toggle_follow_up(
    billing_id: int,
    follow_up: bool = Query(..., description="Activar/desactivar seguimiento"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activa o desactiva el seguimiento de una facturación"""
    update_data = BillingUpdate(follow_up=follow_up)
    return BillingService.update_billing(db, billing_id, update_data)


@router.delete("/{billing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Desactiva una facturación (solo si no está pagada)"""
    BillingService.delete_billing(db, billing_id)
    return None


@router.post("/update-overdue", response_model=dict)
def update_overdue_billings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza automáticamente las facturaciones vencidas"""
    updated_count = BillingService.update_overdue_billings(db)
    return {
        "message": f"Se actualizaron {updated_count} facturaciones a estado VENCIDO",
        "updated": updated_count
    }


@router.get("/client/{client_id}/summary", response_model=dict)
def get_client_billing_summary(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene resumen de facturación de un cliente"""
    stats = BillingService.get_billing_stats(db, client_id=client_id)
    
    return {
        "client_id": client_id,
        "total_billings": stats.total_billings,
        "total_amount": float(stats.total_amount),
        "pending_amount": float(stats.pending_amount),
        "overdue_amount": float(stats.overdue_amount),
        "paid_amount": float(stats.paid_amount),
        "by_status": stats.by_status,
        "by_type": stats.by_type
    }
