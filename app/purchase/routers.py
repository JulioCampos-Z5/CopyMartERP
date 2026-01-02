from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import math

from app.core.database import get_db
from schemas import (
    PurchaseCreate,
    PurchaseUpdate,
    PurchaseResponse,
    PurchaseDetailResponse,
    PurchaseListResponse,
    PurchaseStatusUpdate,
    PurchaseStatsResponse
)
from services import PurchaseService

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)

@router.post(
    "/",
    response_model=PurchaseDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva compra"
)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db)
):

    return PurchaseService.create_purchase(db, purchase)

@router.get(
    "/",
    response_model=PurchaseListResponse,
    summary="Listar todas las compras"
)
def list_purchases(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    search: Optional[str] = Query(None, description="Buscar por nombre, código de envío o comentarios"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    type: Optional[str] = Query(None, description="Filtrar por tipo (Interna/Venta)"),
    user_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    sparepart_id: Optional[int] = Query(None, description="Filtrar por refacción"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin"),
    db: Session = Depends(get_db)
):
    # Obtener listado de compras con paginación y filtros opcionales.
    skip = (page - 1) * page_size
    purchases, total = PurchaseService.get_all_purchases(
        db=db,
        skip=skip,
        limit=page_size,
        search=search,
        status_filter=status,
        type_filter=type,
        user_id=user_id,
        sparepart_id=sparepart_id,
        start_date=start_date,
        end_date=end_date
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "total": total,
        "items": purchases,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get(
    "/pending",
    response_model=list[PurchaseDetailResponse],
    summary="Obtener compras pendientes"
)
def get_pending_purchases(db: Session = Depends(get_db)):

    return PurchaseService.get_pending_purchases(db)

@router.get(
    "/statistics",
    response_model=PurchaseStatsResponse,
    summary="Obtener estadísticas de compras"
)
def get_purchase_statistics(db: Session = Depends(get_db)):
    """
    Obtener estadísticas generales de compras:
    - Total de compras
    - Compras por estado
    - Compras por tipo
    - Costo total de envíos
    """
    return PurchaseService.get_purchase_statistics(db)

@router.get(
    "/user/{user_id}",
    response_model=PurchaseListResponse,
    summary="Obtener compras por usuario"
)
def get_purchases_by_user(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Obtener todas las compras realizadas por un usuario específico.
    skip = (page - 1) * page_size
    purchases, total = PurchaseService.get_purchases_by_user(db, user_id, skip, page_size)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "total": total,
        "items": purchases,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get(
    "/sparepart/{sparepart_id}",
    response_model=PurchaseListResponse,
    summary="Obtener compras por refacción"
)
def get_purchases_by_sparepart(
    sparepart_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Obtener todas las compras de una refacción específica.
    skip = (page - 1) * page_size
    purchases, total = PurchaseService.get_purchases_by_sparepart(db, sparepart_id, skip, page_size)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "total": total,
        "items": purchases,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get(
    "/shipping/{shipping_code}",
    response_model=list[PurchaseDetailResponse],
    summary="Obtener compras por código de envío"
)
def get_purchases_by_shipping_code(
    shipping_code: str,
    db: Session = Depends(get_db)
):
    # Obtener todas las compras con un código de rastreo específico.
    return PurchaseService.get_purchases_by_shipping_code(db, shipping_code)

@router.get(
    "/{purchase_id}",
    response_model=PurchaseDetailResponse,
    summary="Obtener compra por ID"
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
   #  Obtener una compra específica por su ID con toda la información relacionada.
    return PurchaseService.get_purchase_by_id(db, purchase_id)

@router.put(
    "/{purchase_id}",
    response_model=PurchaseDetailResponse,
    summary="Actualizar compra"
)
def update_purchase(
    purchase_id: int,
    purchase: PurchaseUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar información de una compra existente.
    Solo se actualizarán los campos proporcionados.
    """
    return PurchaseService.update_purchase(db, purchase_id, purchase)

@router.patch(
    "/{purchase_id}/status",
    response_model=PurchaseDetailResponse,
    summary="Actualizar estado de compra"
)
def update_purchase_status(
    purchase_id: int,
    status_update: PurchaseStatusUpdate,
    db: Session = Depends(get_db)
):
    return PurchaseService.update_purchase_status(db, purchase_id, status_update)

@router.delete(
    "/{purchase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar compra"
)
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    # Eliminar una compra del sistema.
    PurchaseService.delete_purchase(db, purchase_id)
    return None