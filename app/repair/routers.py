from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db

from .schemas import (
    RepairCreate, 
    RepairUpdate, 
    RepairResponse, 
    RepairList,
    TallerStatusEnum,
    TallerLocationEnum,
    TallerProcessEnum,
    TallerEstatusEnum,
    EquipmentInfo
)
from repair.services import RepairService
from repair.models import TallerStatus, TallerLocation, TallerProcess, TallerEstatus

router = APIRouter(
    prefix="/repairs",
    tags=["Repairs"]
)

@router.post("/", response_model=RepairResponse, status_code=status.HTTP_201_CREATED)
def create_repair(
    repair_data: RepairCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo registro de reparación en el taller.
    
    - Copia los datos del equipo (model, serie, model_toner)
    - Cambia el estado del equipo a TALLER
    - Registra la fecha de alta automáticamente
    """
    repair = RepairService.create_repair(db, repair_data)
    return repair

@router.get("/", response_model=RepairList)
def get_repairs(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de registros"),
    estado_taller: Optional[TallerStatusEnum] = Query(None, description="Filtrar por estado del taller"),
    estatus: Optional[TallerEstatusEnum] = Query(None, description="Filtrar por estatus"),
    ubicacion: Optional[TallerLocationEnum] = Query(None, description="Filtrar por ubicación"),
    proceso: Optional[TallerProcessEnum] = Query(None, description="Filtrar por proceso"),
    search: Optional[str] = Query(None, description="Buscar en model, serie, toner o diagnóstico"),
    db: Session = Depends(get_db)
):
    """
    Lista todas las reparaciones activas con filtros opcionales.
    
    Filtros disponibles:
    - estado_taller: pendiente, pausado, listo
    - estatus: en_espera_autorizacion, en_espera_pieza, pausado, listo
    - ubicacion: zona_1, zona_2, zona_3, zona_4, basura
    - proceso: desconocido, proceso_1, proceso_2, proceso_3
    - search: búsqueda en campos de texto
    """
    # Convertir enums a los tipos del modelo
    estado_filter = TallerStatus(estado_taller.value) if estado_taller else None
    estatus_filter = TallerEstatus(estatus.value) if estatus else None
    ubicacion_filter = TallerLocation(ubicacion.value) if ubicacion else None
    proceso_filter = TallerProcess(proceso.value) if proceso else None
    
    repairs, total = RepairService.get_repairs(
        db=db,
        skip=skip,
        limit=limit,
        estado_taller=estado_filter,
        estatus=estatus_filter,
        ubicacion=ubicacion_filter,
        proceso=proceso_filter,
        search=search
    )
    
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return RepairList(
        total=total,
        page=page,
        page_size=limit,
        repairs=repairs
    )

@router.get("/{repair_id}", response_model=RepairResponse)
def get_repair(
    repair_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene una reparación específica por ID"""
    repair = RepairService.get_repair_by_id(db, repair_id)
    
    if not repair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reparación con ID {repair_id} no encontrada"
        )
    
    return repair

@router.get("/equipment/{item_id}", response_model=List[RepairResponse])
def get_repairs_by_equipment(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene el historial completo de reparaciones de un equipo"""
    repairs = RepairService.get_repairs_by_equipment(db, item_id)
    return repairs

@router.put("/{repair_id}", response_model=RepairResponse)
def update_repair(
    repair_id: int,
    repair_data: RepairUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una reparación existente.
    
    - Si cambia el estado a LISTO, se registra automáticamente la fecha de conclusión
    """
    repair = RepairService.update_repair(db, repair_id, repair_data)
    return repair

@router.post("/{repair_id}/upload-folio")
async def upload_folio(
    repair_id: int,
    file: UploadFile = File(..., description="Archivo PDF o imagen del folio"),
    db: Session = Depends(get_db)
):
    """Sube el folio escaneado para una reparación"""
    repair = await RepairService.upload_file(db, repair_id, file, "folio")
    return {
        "message": "Folio subido exitosamente",
        "repair_id": repair.repair_id,
        "file_path": repair.folio_escaneado
    }

@router.post("/{repair_id}/upload-evidencia")
async def upload_evidencia(
    repair_id: int,
    file: UploadFile = File(..., description="Foto de evidencia"),
    db: Session = Depends(get_db)
):
    """Sube una foto de evidencia para una reparación"""
    repair = await RepairService.upload_file(db, repair_id, file, "evidencia")
    return {
        "message": "Evidencia subida exitosamente",
        "repair_id": repair.repair_id,
        "file_path": repair.foto_evidencia
    }

@router.post("/{repair_id}/return-to-bodega")
def return_to_bodega(
    repair_id: int,
    db: Session = Depends(get_db)
):
    """
    Completa una reparación y devuelve el equipo a BODEGA.
    
    Requisitos:
    - La reparación debe estar en estado LISTO
    
    Acciones:
    - Marca la reparación como completada (is_active = False)
    - Cambia el estado del equipo a BODEGA
    - Registra la fecha de conclusión
    """
    equipment = RepairService.return_equipment_to_bodega(db, repair_id)
    
    return {
        "message": "Equipo devuelto a bodega exitosamente",
        "repair_id": repair_id,
        "equipment_id": equipment.item_id,
        "equipment_status": equipment.location_status.value
    }

@router.delete("/{repair_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repair(
    repair_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina (soft delete) una reparación.
    
    Nota: Esto no cambia el estado del equipo automáticamente.
    """
    RepairService.delete_repair(db, repair_id)
    return None

# Endpoints adicionales para estadísticas

@router.get("/stats/by-status")
def get_stats_by_status(db: Session = Depends(get_db)):
    """Obtiene estadísticas de reparaciones por estado"""
    from sqlalchemy import func
    from .models import Repair
    
    stats = db.query(
        Repair.estado_taller,
        func.count(Repair.repair_id).label('count')
    ).filter(
        Repair.is_active == True
    ).group_by(
        Repair.estado_taller
    ).all()
    
    return {
        "stats": [
            {"estado": stat[0].value, "count": stat[1]}
            for stat in stats
        ]
    }

@router.get("/stats/by-estatus")
def get_stats_by_estatus(db: Session = Depends(get_db)):
    """Obtiene estadísticas de reparaciones por estatus"""
    from sqlalchemy import func
    from .models import Repair
    
    stats = db.query(
        Repair.estatus,
        func.count(Repair.repair_id).label('count')
    ).filter(
        Repair.is_active == True
    ).group_by(
        Repair.estatus
    ).all()
    
    return {
        "stats": [
            {"estatus": stat[0].value, "count": stat[1]}
            for stat in stats
        ]
    }

@router.get("/stats/by-ubicacion")
def get_stats_by_ubicacion(db: Session = Depends(get_db)):
    """Obtiene estadísticas de reparaciones por ubicación"""
    from sqlalchemy import func
    from .models import Repair
    
    stats = db.query(
        Repair.ubicacion,
        func.count(Repair.repair_id).label('count')
    ).filter(
        Repair.is_active == True,
        Repair.ubicacion.isnot(None)
    ).group_by(
        Repair.ubicacion
    ).all()
    
    return {
        "stats": [
            {"ubicacion": stat[0].value, "count": stat[1]}
            for stat in stats
        ]
    }