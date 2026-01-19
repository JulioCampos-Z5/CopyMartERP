from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal

from app.print.models import PrintCounter
from app.print.schemas import (
    PrintCounterCreate, 
    PrintCounterUpdate, 
    PrintCounterFilter,
    PrintCounterBatchCreate,
    PrintCounterStats
)
from app.rent.models import Rent, ContractStatus


class PrintCounterService:
    
    @staticmethod
    def validate_rent(db: Session, rent_id: int) -> Rent:
        rent = db.query(Rent).filter(
            Rent.rent_id == rent_id,
            Rent.is_active == True
        ).first()
        
        if not rent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Renta activa con ID {rent_id} no encontrada"
            )
        
        if rent.contract_status != ContractStatus.VIGENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La renta debe estar VIGENTE para registrar contadores"
            )
        
        if not rent.has_print_service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La renta no incluye servicio de impresión"
            )
        
        return rent
    
    @staticmethod
    def get_previous_counter(db: Session, rent_id: int, period_month: int, period_year: int) -> Optional[PrintCounter]:
        prev_month = period_month - 1 if period_month > 1 else 12
        prev_year = period_year if period_month > 1 else period_year - 1
        
        return db.query(PrintCounter).filter(
            PrintCounter.rent_id == rent_id,
            PrintCounter.period_month == prev_month,
            PrintCounter.period_year == prev_year,
            PrintCounter.is_active == True
        ).first()
    
    @staticmethod
    def calculate_counters(
        rent: Rent,
        bn_current: int,
        color_current: int,
        bn_previous: int = 0,
        color_previous: int = 0
    ) -> dict:
        
        # Calcular impresiones realizadas
        bn_printed = max(0, bn_current - bn_previous)
        color_printed = max(0, color_current - color_previous)
        
        # Calcular excesos
        bn_excess = max(0, bn_printed - rent.bn_included)
        color_excess = max(0, color_printed - rent.color_included)
        
        # Calcular montos
        bn_excess_amount = Decimal(str(bn_excess)) * rent.bn_cost_per_excess
        color_excess_amount = Decimal(str(color_excess)) * rent.color_cost_per_excess
        total_excess_amount = bn_excess_amount + color_excess_amount
        
        return {
            "bn_previous": bn_previous,
            "bn_printed": bn_printed,
            "bn_included": rent.bn_included,
            "bn_excess": bn_excess,
            "bn_cost_per_page": rent.bn_cost_per_excess,
            "bn_excess_amount": bn_excess_amount,
            
            "color_previous": color_previous,
            "color_printed": color_printed,
            "color_included": rent.color_included,
            "color_excess": color_excess,
            "color_cost_per_page": rent.color_cost_per_excess,
            "color_excess_amount": color_excess_amount,
            
            "total_excess_amount": total_excess_amount
        }
    
    @staticmethod
    def create_counter(
        db: Session,
        counter_data: PrintCounterCreate,
        current_user_id: Optional[int] = None
    ) -> PrintCounter:
        """Crea un registro de contador"""
        
        # Validar renta
        rent = PrintCounterService.validate_rent(db, counter_data.rent_id)
        
        # Verificar si ya existe contador para este período
        existing = db.query(PrintCounter).filter(
            PrintCounter.rent_id == counter_data.rent_id,
            PrintCounter.period_month == counter_data.period_month,
            PrintCounter.period_year == counter_data.period_year,
            PrintCounter.is_active == True
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un contador activo para {counter_data.period_month}/{counter_data.period_year}"
            )
        
        # Obtener contador anterior
        prev_counter = PrintCounterService.get_previous_counter(
            db, 
            counter_data.rent_id,
            counter_data.period_month,
            counter_data.period_year
        )
        
        bn_previous = prev_counter.bn_current if prev_counter else 0
        color_previous = prev_counter.color_current if prev_counter else 0
        
        # Validar que los contadores actuales no sean menores a los anteriores
        if counter_data.bn_current < bn_previous:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El contador B/N actual ({counter_data.bn_current}) no puede ser menor al anterior ({bn_previous})"
            )
        
        if counter_data.color_current < color_previous:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El contador Color actual ({counter_data.color_current}) no puede ser menor al anterior ({color_previous})"
            )
        
        # Calcular valores
        calculated = PrintCounterService.calculate_counters(
            rent,
            counter_data.bn_current,
            counter_data.color_current,
            bn_previous,
            color_previous
        )
        
        # Crear contador
        new_counter = PrintCounter(
            rent_id=counter_data.rent_id,
            period_month=counter_data.period_month,
            period_year=counter_data.period_year,
            bn_current=counter_data.bn_current,
            color_current=counter_data.color_current,
            counter_photo_url=counter_data.counter_photo_url,
            notes=counter_data.notes,
            reading_date=counter_data.reading_date,
            created_by=current_user_id,
            **calculated
        )
        
        db.add(new_counter)
        db.commit()
        db.refresh(new_counter)
        
        return new_counter
    
    @staticmethod
    def create_counters_batch(
        db: Session,
        batch_data: PrintCounterBatchCreate,
        current_user_id: Optional[int] = None
    ) -> dict:
        """Crea contadores en lote para múltiples rentas"""
        
        # Construir query de rentas
        query = db.query(Rent).filter(
            Rent.is_active == True,
            Rent.contract_status == ContractStatus.VIGENTE,
            Rent.has_print_service == True
        )
        
        if batch_data.rent_ids:
            query = query.filter(Rent.rent_id.in_(batch_data.rent_ids))
        
        if batch_data.client_ids:
            query = query.filter(Rent.client_id.in_(batch_data.client_ids))
        
        rents = query.all()
        
        created_count = 0
        skipped_count = 0
        errors = []
        
        for rent in rents:
            try:
                # Verificar si ya existe
                existing = db.query(PrintCounter).filter(
                    PrintCounter.rent_id == rent.rent_id,
                    PrintCounter.period_month == batch_data.period_month,
                    PrintCounter.period_year == batch_data.period_year,
                    PrintCounter.is_active == True
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Crear contador con valores en 0 (para que el usuario los actualice)
                counter_create = PrintCounterCreate(
                    rent_id=rent.rent_id,
                    period_month=batch_data.period_month,
                    period_year=batch_data.period_year,
                    bn_current=0,
                    color_current=0,
                    reading_date=batch_data.reading_date
                )
                
                PrintCounterService.create_counter(db, counter_create, current_user_id)
                created_count += 1
                
            except Exception as e:
                errors.append({
                    "rent_id": rent.rent_id,
                    "contract_number": rent.contract_number,
                    "error": str(e)
                })
        
        return {
            "total_rents": len(rents),
            "created": created_count,
            "skipped": skipped_count,
            "errors": errors
        }
    
    @staticmethod
    def get_counter(db: Session, counter_id: int) -> PrintCounter:
        """Obtiene un contador por ID"""
        counter = db.query(PrintCounter).options(
            joinedload(PrintCounter.rent).joinedload(Rent.client),
            joinedload(PrintCounter.rent).joinedload(Rent.equipment)
        ).filter(PrintCounter.counter_id == counter_id).first()
        
        if not counter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contador con ID {counter_id} no encontrado"
            )
        
        return counter
    
    @staticmethod
    def get_counters(
        db: Session,
        filters: PrintCounterFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[PrintCounter]:
        """Lista contadores con filtros"""
        query = db.query(PrintCounter).options(
            joinedload(PrintCounter.rent).joinedload(Rent.client),
            joinedload(PrintCounter.rent).joinedload(Rent.equipment)
        )
        
        if filters.rent_id:
            query = query.filter(PrintCounter.rent_id == filters.rent_id)
        
        if filters.client_id:
            query = query.join(Rent).filter(Rent.client_id == filters.client_id)
        
        if filters.period_month:
            query = query.filter(PrintCounter.period_month == filters.period_month)
        
        if filters.period_year:
            query = query.filter(PrintCounter.period_year == filters.period_year)
        
        if filters.is_billed is not None:
            query = query.filter(PrintCounter.is_billed == filters.is_billed)
        
        if filters.is_active is not None:
            query = query.filter(PrintCounter.is_active == filters.is_active)
        
        query = query.order_by(
            PrintCounter.period_year.desc(),
            PrintCounter.period_month.desc()
        )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_counter(
        db: Session,
        counter_id: int,
        counter_data: PrintCounterUpdate
    ) -> PrintCounter:
        """Actualiza un contador"""
        counter = PrintCounterService.get_counter(db, counter_id)
        
        if counter.is_billed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede actualizar un contador ya facturado"
            )
        
        rent = counter.rent
        update_data = counter_data.dict(exclude_unset=True)
        
        # Si se actualizan contadores, recalcular
        if 'bn_current' in update_data or 'color_current' in update_data:
            bn_current = update_data.get('bn_current', counter.bn_current)
            color_current = update_data.get('color_current', counter.color_current)
            
            calculated = PrintCounterService.calculate_counters(
                rent,
                bn_current,
                color_current,
                counter.bn_previous,
                counter.color_previous
            )
            
            update_data.update(calculated)
            update_data['bn_current'] = bn_current
            update_data['color_current'] = color_current
        
        for field, value in update_data.items():
            setattr(counter, field, value)
        
        counter.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(counter)
        
        return counter
    
    @staticmethod
    def get_counter_stats(
        db: Session,
        rent_id: Optional[int] = None,
        client_id: Optional[int] = None,
        period_month: Optional[int] = None,
        period_year: Optional[int] = None
    ) -> PrintCounterStats:
        """Obtiene estadísticas de contadores"""
        query = db.query(PrintCounter).filter(PrintCounter.is_active == True)
        
        if rent_id:
            query = query.filter(PrintCounter.rent_id == rent_id)
        
        if client_id:
            query = query.join(Rent).filter(Rent.client_id == client_id)
        
        if period_month:
            query = query.filter(PrintCounter.period_month == period_month)
        
        if period_year:
            query = query.filter(PrintCounter.period_year == period_year)
        
        counters = query.all()
        
        total_counters = len(counters)
        total_bn_printed = sum(c.bn_printed for c in counters)
        total_color_printed = sum(c.color_printed for c in counters)
        total_bn_excess = sum(c.bn_excess for c in counters)
        total_color_excess = sum(c.color_excess for c in counters)
        total_excess_amount = sum(c.total_excess_amount for c in counters)
        billed_amount = sum(c.total_excess_amount for c in counters if c.is_billed)
        pending_amount = sum(c.total_excess_amount for c in counters if not c.is_billed)
        
        return PrintCounterStats(
            total_counters=total_counters,
            total_bn_printed=total_bn_printed,
            total_color_printed=total_color_printed,
            total_bn_excess=total_bn_excess,
            total_color_excess=total_color_excess,
            total_excess_amount=total_excess_amount,
            billed_amount=billed_amount,
            pending_amount=pending_amount
        )
    
    @staticmethod
    def delete_counter(db: Session, counter_id: int) -> None:
        """Desactiva un contador"""
        counter = PrintCounterService.get_counter(db, counter_id)
        
        if counter.is_billed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar un contador ya facturado"
            )
        
        counter.is_active = False
        counter.updated_at = datetime.utcnow()
        
        db.commit()