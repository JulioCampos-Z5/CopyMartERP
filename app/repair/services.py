from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, and_
from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException, status, UploadFile
import os
import shutil
from pathlib import Path

from repair.models import Repair, TallerStatus, TallerLocation, TallerProcess, TallerEstatus, Procedencia
from repair.schemas import RepairCreate, RepairUpdate, RepairResponse
from equipment.models import Equipment, LocationStatus

class RepairService:
    
    @staticmethod
    def create_repair(db: Session, repair_data: RepairCreate) -> Repair:
        """
        Crea un nuevo registro de reparación y cambia el estado del equipo a TALLER
        """
        # Verificar que el equipo existe
        equipment = db.query(Equipment).filter(
            Equipment.item_id == repair_data.item_id,
            Equipment.is_active == True
        ).first()
        
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {repair_data.item_id} no encontrado"
            )
        
        # Verificar que el equipo no esté ya en taller
        existing_repair = db.query(Repair).filter(
            Repair.item_id == repair_data.item_id,
            Repair.is_active == True,
            Repair.estado_taller != TallerStatus.LISTO
        ).first()
        
        if existing_repair:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El equipo ya tiene una reparación activa (ID: {existing_repair.repair_id})"
            )
        
        # Crear el registro de reparación copiando datos del equipo
        new_repair = Repair(
            item_id=equipment.item_id,
            model=equipment.model,
            serie=equipment.serie,
            model_toner=equipment.model_toner,
            procedencia=repair_data.procedencia,
            estado_taller=repair_data.estado_taller,
            ubicacion=repair_data.ubicacion,
            proceso=repair_data.proceso,
            estatus=repair_data.estatus,
            diagnostico_inicial=repair_data.diagnostico_inicial,
            comments=repair_data.comments
        )
        
        # Cambiar el estado del equipo a TALLER
        equipment.location_status = LocationStatus.TALLER
        
        db.add(new_repair)
        db.commit()
        db.refresh(new_repair)
        
        return new_repair
    
    @staticmethod
    def get_repair_by_id(db: Session, repair_id: int) -> Optional[Repair]:
        """Obtiene una reparación por ID"""
        return db.query(Repair).filter(
            Repair.repair_id == repair_id,
            Repair.is_active == True
        ).first()
    
    @staticmethod
    def get_repairs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        estado_taller: Optional[TallerStatus] = None,
        estatus: Optional[TallerEstatus] = None,
        ubicacion: Optional[TallerLocation] = None,
        proceso: Optional[TallerProcess] = None,
        search: Optional[str] = None
    ) -> tuple[List[Repair], int]:
        """
        Lista reparaciones con filtros opcionales
        """
        query = db.query(Repair).filter(Repair.is_active == True)
        
        # Filtros
        if estado_taller:
            query = query.filter(Repair.estado_taller == estado_taller)
        
        if estatus:
            query = query.filter(Repair.estatus == estatus)
        
        if ubicacion:
            query = query.filter(Repair.ubicacion == ubicacion)
        
        if proceso:
            query = query.filter(Repair.proceso == proceso)
        
        if search:
            query = query.filter(
                or_(
                    Repair.model.ilike(f"%{search}%"),
                    Repair.serie.ilike(f"%{search}%"),
                    Repair.model_toner.ilike(f"%{search}%"),
                    Repair.diagnostico_inicial.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        repairs = query.order_by(desc(Repair.created_at)).offset(skip).limit(limit).all()
        
        return repairs, total
    
    @staticmethod
    def update_repair(db: Session, repair_id: int, repair_data: RepairUpdate) -> Repair:
        """Actualiza una reparación"""
        repair = RepairService.get_repair_by_id(db, repair_id)
        
        if not repair:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reparación con ID {repair_id} no encontrada"
            )
        
        # Actualizar campos si se proporcionan
        update_data = repair_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(repair, field, value)
        
        # Si el estado cambia a LISTO, establecer fecha de conclusión
        if repair_data.estado_taller == TallerStatus.LISTO and not repair.fecha_conclusion:
            repair.fecha_conclusion = datetime.utcnow()
        
        repair.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(repair)
        
        return repair
    
    @staticmethod
    def delete_repair(db: Session, repair_id: int) -> bool:
        """Soft delete de una reparación"""
        repair = RepairService.get_repair_by_id(db, repair_id)
        
        if not repair:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reparación con ID {repair_id} no encontrada"
            )
        
        repair.is_active = False
        repair.updated_at = datetime.utcnow()
        
        db.commit()
        
        return True
    
    @staticmethod
    def return_equipment_to_bodega(db: Session, repair_id: int) -> Equipment:
        """
        Marca la reparación como completada y devuelve el equipo a BODEGA
        """
        repair = RepairService.get_repair_by_id(db, repair_id)
        
        if not repair:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reparación con ID {repair_id} no encontrada"
            )
        
        # Verificar que la reparación esté lista
        if repair.estado_taller != TallerStatus.LISTO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La reparación debe estar en estado 'LISTO' para devolver a bodega"
            )
        
        # Obtener el equipo
        equipment = db.query(Equipment).filter(
            Equipment.item_id == repair.item_id
        ).first()
        
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {repair.item_id} no encontrado"
            )
        
        # Cambiar estado del equipo a BODEGA
        equipment.location_status = LocationStatus.BODEGA
        
        # Marcar la reparación como inactiva (completada)
        repair.is_active = False
        repair.fecha_conclusion = datetime.utcnow()
        repair.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(equipment)
        
        return equipment
    
    @staticmethod
    async def upload_file(
        db: Session,
        repair_id: int,
        file: UploadFile,
        file_type: str  # "folio" o "evidencia"
    ) -> Repair:
        """
        Sube un archivo (folio escaneado o foto evidencia) para una reparación
        """
        repair = RepairService.get_repair_by_id(db, repair_id)
        
        if not repair:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reparación con ID {repair_id} no encontrada"
            )
        
        # Crear directorio si no existe
        upload_dir = Path("uploads/repairs")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre de archivo único
        file_extension = Path(file.filename).suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{file_type}_{repair_id}_{timestamp}{file_extension}"
        file_path = upload_dir / filename
        
        # Guardar archivo
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Actualizar el campo correspondiente
        if file_type == "folio":
            repair.folio_escaneado = str(file_path)
        elif file_type == "evidencia":
            repair.foto_evidencia = str(file_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de archivo inválido. Use 'folio' o 'evidencia'"
            )
        
        repair.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(repair)
        
        return repair
    
    @staticmethod
    def get_repairs_by_equipment(db: Session, item_id: int) -> List[Repair]:
        """Obtiene todas las reparaciones de un equipo"""
        return db.query(Repair).filter(
            Repair.item_id == item_id
        ).order_by(desc(Repair.created_at)).all()