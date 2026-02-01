from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import math
from core.database import get_db
from sparepart.schemas import (
    SparepartCreate,
    SparepartUpdate,
    SparepartResponse,
    SparepartListResponse
)
from sparepart.services import SparepartService

router = APIRouter(
    prefix="/spareparts",
    tags=["Spareparts"]
)

@router.post(
    "/",
    response_model=SparepartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva refacción"
)
def create_sparepart(
    sparepart: SparepartCreate,
    db: Session = Depends(get_db)
):

    return SparepartService.create_sparepart(db, sparepart)

@router.get(
    "/",
    response_model=SparepartListResponse,
    summary="Listar todas las refacciones"
)
def list_spareparts(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    search: Optional[str] = Query(None, description="Buscar por nombre, código, descripción o equipo"),
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    color: Optional[str] = Query(None, description="Filtrar por color"),
    supplier: Optional[str] = Query(None, description="Filtrar por proveedor"),
    db: Session = Depends(get_db)
):

    skip = (page - 1) * page_size
    spareparts, total = SparepartService.get_all_spareparts(
        db=db,
        skip=skip,
        limit=page_size,
        search=search,
        brand=brand,
        color=color,
        supplier=supplier
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "total": total,
        "items": spareparts,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get(
    "/{sparepart_id}",
    response_model=SparepartResponse,
    summary="Obtener refacción por ID"
)
def get_sparepart(
    sparepart_id: int,
    db: Session = Depends(get_db)
):

    return SparepartService.get_sparepart_by_id(db, sparepart_id)

@router.get(
    "/code/{code}",
    response_model=SparepartResponse,
    summary="Obtener refacción por código"
)
def get_sparepart_by_code(
    code: str,
    db: Session = Depends(get_db)
):

    sparepart = SparepartService.get_sparepart_by_code(db, code)
    if not sparepart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Refacción con código {code} no encontrada"
        )
    return sparepart

@router.put(
    "/{sparepart_id}",
    response_model=SparepartResponse,
    summary="Actualizar refacción"
)
def update_sparepart(
    sparepart_id: int,
    sparepart: SparepartUpdate,
    db: Session = Depends(get_db)
):

    return SparepartService.update_sparepart(db, sparepart_id, sparepart)

@router.delete(
    "/{sparepart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar refacción"
)
def delete_sparepart(
    sparepart_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una refacción del sistema.
    """
    SparepartService.delete_sparepart(db, sparepart_id)
    return None

@router.get(
    "/filters/brands",
    response_model=list[str],
    summary="Obtener todas las marcas"
)
def get_brands(db: Session = Depends(get_db)):
    """
    Obtener lista de todas las marcas únicas registradas en el sistema.
    """
    return SparepartService.get_brands(db)

@router.get(
    "/filters/suppliers",
    response_model=list[str],
    summary="Obtener todos los proveedores"
)
def get_suppliers(db: Session = Depends(get_db)):

    return SparepartService.get_suppliers(db)

@router.get(
    "/filters/colors",
    response_model=list[str],
    summary="Obtener todos los colores"
)
def get_colors(db: Session = Depends(get_db)):
    return SparepartService.get_colors(db)