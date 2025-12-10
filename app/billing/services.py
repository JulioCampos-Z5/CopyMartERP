from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, date

from app.billing.models import Billing, BillingStatus, BillingType
from app.billing.schemas import (
    BillingCreate, 
    BillingUpdate, 
    BillingResponse, 
    BillingFilter,
    BillingBatchCreate,
    BillingPayment,
    BillingStats
)
from app.rent.models import Rent, ContractStatus as RentContractStatus
from app.sale.models import Sale, SaleStatus
from app.client.models import Client


class BillingService:
    
    @staticmethod
    def generate_invoice_number(billing_id: int, billing_type: BillingType, created_at: datetime) -> str:
        month = created_at.strftime("%m")
        year = created_at.strftime("%y")
        type_code = "R" if billing_type == BillingType.RENTA else "V"
        return f"CAT-{billing_id:04d}-{month}-{year}-{type_code}B"
    
    @staticmethod
    def calculate_status(target_date: date, due_date: date, payment_date: Optional[date]) -> BillingStatus:
        """Calcula el estado basado en las fechas"""
        if payment_date:
            return BillingStatus.PAGADO
        
        today = date.today()
        if today > due_date:
            return BillingStatus.VENCIDO
        
        return BillingStatus.PENDIENTE
    
    @staticmethod
    def validate_rent(db: Session, rent_id: int) -> Rent:
        """Valida que la renta existe y está activa"""
        rent = db.query(Rent).filter(
            Rent.rent_id == rent_id,
            Rent.is_active == True
        ).first()
        
        if not rent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Renta activa con ID {rent_id} no encontrada"
            )
        
        # Validar que la renta esté vigente
        if rent.contract_status != RentContractStatus.VIGENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La renta debe estar en estado VIGENTE para facturar"
            )
        
        return rent
    
    @staticmethod
    def validate_sale(db: Session, sale_id: int) -> Sale:
        """Valida que la venta existe y está activa"""
        sale = db.query(Sale).filter(
            Sale.sale_id == sale_id,
            Sale.is_active == True
        ).first()
        
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta activa con ID {sale_id} no encontrada"
            )
        
        # Validar que la venta esté confirmada o entregada
        if sale.sale_status not in [SaleStatus.CONFIRMADA, SaleStatus.ENTREGADA]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La venta debe estar CONFIRMADA o ENTREGADA para facturar"
            )
        
        return sale
    
    @staticmethod
    def create_billing(
        db: Session, 
        billing_data: BillingCreate,
        current_user_id: Optional[int] = None
    ) -> Billing:
        """Crea una facturación individual"""
        
        # Validar y obtener información según el tipo
        if billing_data.billing_type == BillingType.RENTA:
            rent = BillingService.validate_rent(db, billing_data.rent_id)
            client_id = rent.client_id
            branch_id = rent.branch_id
            area_id = rent.area_id
            amount = rent.rent
            
            # Verificar si ya existe facturación activa para esta renta este mes
            existing = db.query(Billing).filter(
                Billing.rent_id == billing_data.rent_id,
                Billing.is_active == True,
                func.extract('month', Billing.target_date) == billing_data.target_date.month,
                func.extract('year', Billing.target_date) == billing_data.target_date.year
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe una facturación activa para esta renta en {billing_data.target_date.strftime('%m/%Y')}"
                )
        else:  # VENTA
            sale = BillingService.validate_sale(db, billing_data.sale_id)
            client_id = sale.client_id
            branch_id = sale.branch_id
            area_id = sale.area_id
            amount = sale.sale_price
            
            # Verificar si ya existe facturación para esta venta
            existing = db.query(Billing).filter(
                Billing.sale_id == billing_data.sale_id,
                Billing.is_active == True
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe una facturación activa para esta venta"
                )
        
        # Calcular estado inicial
        initial_status = BillingService.calculate_status(
            billing_data.target_date,
            billing_data.due_date,
            None
        )
        
        # Crear facturación
        new_billing = Billing(
            billing_type=billing_data.billing_type,
            rent_id=billing_data.rent_id,
            sale_id=billing_data.sale_id,
            client_id=client_id,
            branch_id=branch_id,
            area_id=area_id,
            amount=amount,
            target_date=billing_data.target_date,
            due_date=billing_data.due_date,
            status=initial_status,
            follow_up=billing_data.follow_up,
            payment_term=billing_data.payment_term,
            payment_day=billing_data.payment_day,
            comment=billing_data.comment,
            created_by=current_user_id
        )
        
        db.add(new_billing)
        db.flush()
        
        # Generar número de factura
        new_billing.invoice_number = BillingService.generate_invoice_number(
            new_billing.billing_id,
            billing_data.billing_type,
            new_billing.created_at
        )
        
        db.commit()
        db.refresh(new_billing)
        
        return new_billing
    
    @staticmethod
    def create_billing_batch(
        db: Session,
        batch_data: BillingBatchCreate,
        current_user_id: Optional[int] = None
    ) -> dict:
        """Genera facturación masiva para rentas activas"""
        
        # Construir query base de rentas activas y vigentes
        query = db.query(Rent).filter(
            Rent.is_active == True,
            Rent.contract_status == RentContractStatus.VIGENTE
        )
        
        # Filtrar por clientes específicos si se proporcionan
        if batch_data.client_ids:
            query = query.filter(Rent.client_id.in_(batch_data.client_ids))
        
        rents = query.all()
        
        created_count = 0
        skipped_count = 0
        errors = []
        
        for rent in rents:
            try:
                # Verificar si ya existe facturación para este mes
                existing = db.query(Billing).filter(
                    Billing.rent_id == rent.rent_id,
                    Billing.is_active == True,
                    func.extract('month', Billing.target_date) == batch_data.target_date.month,
                    func.extract('year', Billing.target_date) == batch_data.target_date.year
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Crear facturación
                billing_create = BillingCreate(
                    billing_type=BillingType.RENTA,
                    rent_id=rent.rent_id,
                    target_date=batch_data.target_date,
                    due_date=batch_data.due_date,
                    payment_term=batch_data.payment_term,
                    payment_day=batch_data.payment_day,
                    comment=batch_data.comment
                )
                
                BillingService.create_billing(db, billing_create, current_user_id)
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
    def get_billing(db: Session, billing_id: int) -> Billing:
        """Obtiene una facturación por ID"""
        billing = db.query(Billing).options(
            joinedload(Billing.client),
            joinedload(Billing.branch),
            joinedload(Billing.area),
            joinedload(Billing.rent),
            joinedload(Billing.sale)
        ).filter(Billing.billing_id == billing_id).first()
        
        if not billing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Facturación con ID {billing_id} no encontrada"
            )
        
        return billing
    
    @staticmethod
    def get_billings(
        db: Session,
        filters: BillingFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[Billing]:
        """Lista facturaciones con filtros"""
        query = db.query(Billing).options(
            joinedload(Billing.client),
            joinedload(Billing.branch),
            joinedload(Billing.area),
            joinedload(Billing.rent),
            joinedload(Billing.sale)
        )
        
        # Aplicar filtros
        if filters.billing_type:
            query = query.filter(Billing.billing_type == filters.billing_type)
        
        if filters.client_id:
            query = query.filter(Billing.client_id == filters.client_id)
        
        if filters.branch_id:
            query = query.filter(Billing.branch_id == filters.branch_id)
        
        if filters.area_id:
            query = query.filter(Billing.area_id == filters.area_id)
        
        if filters.status:
            query = query.filter(Billing.status == filters.status)
        
        if filters.follow_up is not None:
            query = query.filter(Billing.follow_up == filters.follow_up)
        
        if filters.is_active is not None:
            query = query.filter(Billing.is_active == filters.is_active)
        
        if filters.date_from:
            query = query.filter(Billing.target_date >= filters.date_from)
        
        if filters.date_to:
            query = query.filter(Billing.target_date <= filters.date_to)
        
        # Ordenar por fecha objetivo descendente
        query = query.order_by(Billing.target_date.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_billing(
        db: Session,
        billing_id: int,
        billing_data: BillingUpdate
    ) -> Billing:
        """Actualiza una facturación"""
        billing = BillingService.get_billing(db, billing_id)
        
        update_data = billing_data.dict(exclude_unset=True)
        
        # Actualizar campos
        for field, value in update_data.items():
            setattr(billing, field, value)
        
        # Recalcular estado si se actualizaron fechas
        if 'target_date' in update_data or 'due_date' in update_data or 'payment_date' in update_data:
            billing.status = BillingService.calculate_status(
                billing.target_date,
                billing.due_date,
                billing.payment_date
            )
        
        billing.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(billing)
        
        return billing
    
    @staticmethod
    def mark_as_paid(
        db: Session,
        billing_id: int,
        payment_data: BillingPayment
    ) -> Billing:
        """Marca una facturación como pagada"""
        billing = BillingService.get_billing(db, billing_id)
        
        if billing.status == BillingStatus.PAGADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta facturación ya está marcada como pagada"
            )
        
        billing.payment_date = payment_data.payment_date
        billing.status = BillingStatus.PAGADO
        
        if payment_data.comment:
            billing.comment = payment_data.comment
        
        billing.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(billing)
        
        return billing
    
    @staticmethod
    def update_overdue_billings(db: Session) -> int:
        """Actualiza automáticamente los estados vencidos"""
        today = date.today()
        
        updated = db.query(Billing).filter(
            Billing.is_active == True,
            Billing.status == BillingStatus.PENDIENTE,
            Billing.due_date < today
        ).update({
            "status": BillingStatus.VENCIDO,
            "updated_at": datetime.utcnow()
        })
        
        db.commit()
        return updated
    
    @staticmethod
    def get_billing_stats(
        db: Session,
        client_id: Optional[int] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> BillingStats:
        """Obtiene estadísticas de facturación"""
        query = db.query(Billing).filter(Billing.is_active == True)
        
        if client_id:
            query = query.filter(Billing.client_id == client_id)
        
        if date_from:
            query = query.filter(Billing.target_date >= date_from)
        
        if date_to:
            query = query.filter(Billing.target_date <= date_to)
        
        billings = query.all()
        
        # Calcular estadísticas
        total_billings = len(billings)
        total_amount = sum(b.amount for b in billings)
        
        by_status = {}
        for status in BillingStatus:
            by_status[status.value] = sum(1 for b in billings if b.status == status)
        
        by_type = {}
        for btype in BillingType:
            by_type[btype.value] = sum(1 for b in billings if b.billing_type == btype)
        
        pending_amount = sum(b.amount for b in billings if b.status == BillingStatus.PENDIENTE)
        overdue_amount = sum(b.amount for b in billings if b.status == BillingStatus.VENCIDO)
        paid_amount = sum(b.amount for b in billings if b.status == BillingStatus.PAGADO)
        
        return BillingStats(
            total_billings=total_billings,
            total_amount=total_amount,
            by_status=by_status,
            by_type=by_type,
            pending_amount=pending_amount,
            overdue_amount=overdue_amount,
            paid_amount=paid_amount
        )
    
    @staticmethod
    def delete_billing(db: Session, billing_id: int) -> None:
        """Desactiva una facturación"""
        billing = BillingService.get_billing(db, billing_id)
        
        if billing.status == BillingStatus.PAGADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar una facturación ya pagada"
            )
        
        billing.is_active = False
        billing.updated_at = datetime.utcnow()
        
        db.commit()