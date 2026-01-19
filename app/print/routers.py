from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.auth.routers import get_current_user
from app.auth.models import User
from app.print.schemas import (
    PrintCounterCreate,
    PrintCounterUpdate,
    PrintCounterResponse,
    PrintCounterFilter,
    PrintCounterBatchCreate,
    PrintCounterStats
)
from app.print.services import PrintCounterService

router = APIRouter(
    prefix="/print",
    tags=["Print Counters"]
)


@router.post("/", response_model=PrintCounterResponse, status_code=status.HTTP_201_CREATED)
def create_counter(
    counter_data: PrintCounterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PrintCounterService.create_counter(
        db,
        counter_data,
        current_user.user_id
    )


@router.post("/batch", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_counters_batch(
    batch_data: PrintCounterBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PrintCounterService.create_counters_batch(
        db,
        batch_data,
        current_user.user_id
    )


@router.get("/", response_model=List[PrintCounterResponse])
def get_counters(
    rent_id: Optional[int] = Query(None, description="Filtrar por renta"),
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    period_month: Optional[int] = Query(None, ge=1, le=12, description="Mes del período"),
    period_year: Optional[int] = Query(None, ge=2020, description="Año del período"),
    is_billed: Optional[bool] = Query(None, description="Filtrar por facturado"),
    is_active: Optional[bool] = Query(True, description="Filtrar por activos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filters = PrintCounterFilter(
        rent_id=rent_id,
        client_id=client_id,
        period_month=period_month,
        period_year=period_year,
        is_billed=is_billed,
        is_active=is_active
    )
    
    return PrintCounterService.get_counters(db, filters, skip, limit)


@router.get("/{counter_id}", response_model=PrintCounterResponse)
def get_counter(
    counter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PrintCounterService.get_counter(db, counter_id)


@router.put("/{counter_id}", response_model=PrintCounterResponse)
def update_counter(
    counter_id: int,
    counter_data: PrintCounterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PrintCounterService.update_counter(db, counter_id, counter_data)


@router.delete("/{counter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_counter(
    counter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    PrintCounterService.delete_counter(db, counter_id)
    return None


@router.get("/stats/summary", response_model=PrintCounterStats)
def get_counter_stats(
    rent_id: Optional[int] = Query(None, description="Filtrar por renta"),
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    period_month: Optional[int] = Query(None, ge=1, le=12, description="Mes del período"),
    period_year: Optional[int] = Query(None, ge=2020, description="Año del período"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PrintCounterService.get_counter_stats(
        db,
        rent_id=rent_id,
        client_id=client_id,
        period_month=period_month,
        period_year=period_year
    )


@router.get("/rent/{rent_id}/history", response_model=List[PrintCounterResponse])
def get_rent_counter_history(
    rent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filters = PrintCounterFilter(rent_id=rent_id, is_active=True)
    return PrintCounterService.get_counters(db, filters, skip=0, limit=1000)