from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, and_
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
from decimal import Decimal

from models import Purchase, Sparepart, Contact, PurchaseStatus, PurchaseType
from schemas import PurchaseCreate, PurchaseUpdate, PurchaseStatusUpdate

class PurchaseService:
    
    @staticmethod
    def create_purchase(db: Session, purchase_data: PurchaseCreate) -> Purchase:
        """Crear una nueva compra"""
        # Verificar que existe la refacción
        sparepart = db.query(Sparepart).filter(Sparepart.sparepart_id == purchase_data.sparepart_id).first()
        if not sparepart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Refacción con ID {purchase_data.sparepart_id} no encontrada"
            )
        
        # Verificar que existe el usuario
        user = db.query(Contact).filter(Contact.contact_id == purchase_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {purchase_data.user_id} no encontrado"
            )
        
        db_purchase = Purchase(**purchase_data.model_dump())
        db.add(db_purchase)
        db.commit()
        db.refresh(db_purchase)
        
        # Cargar relaciones
        db.refresh(db_purchase)
        return db_purchase
    
    @staticmethod
    def get_purchase_by_id(db: Session, purchase_id: int) -> Purchase:
        """Obtener una compra por ID con sus relaciones"""
        purchase = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user)
        ).filter(Purchase.purchase_id == purchase_id).first()
        
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con ID {purchase_id} no encontrada"
            )
        return purchase
    
    @staticmethod
    def get_all_purchases(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        user_id: Optional[int] = None,
        sparepart_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> tuple[list[Purchase], int]:
        """Obtener todas las compras con filtros y paginación"""
        query = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user)
        )
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                Purchase.name.ilike(f"%{search}%"),
                Purchase.shipping_code.ilike(f"%{search}%"),
                Purchase.comments.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if status_filter:
            query = query.filter(Purchase.status == status_filter)
        
        if type_filter:
            query = query.filter(Purchase.type == type_filter)
        
        if user_id:
            query = query.filter(Purchase.user_id == user_id)
        
        if sparepart_id:
            query = query.filter(Purchase.sparepart_id == sparepart_id)
        
        if start_date:
            query = query.filter(Purchase.created_at >= start_date)
        
        if end_date:
            query = query.filter(Purchase.created_at <= end_date)
        
        # Obtener total
        total = query.count()
        
        # Aplicar paginación y ordenar por fecha de creación descendente
        purchases = query.order_by(Purchase.created_at.desc()).offset(skip).limit(limit).all()
        
        return purchases, total
    
    @staticmethod
    def update_purchase(
        db: Session,
        purchase_id: int,
        purchase_data: PurchaseUpdate
    ) -> Purchase:
        """Actualizar una compra"""
        db_purchase = PurchaseService.get_purchase_by_id(db, purchase_id)
        
        # Actualizar solo los campos proporcionados
        update_data = purchase_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_purchase, field, value)
        
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
    
    @staticmethod
    def update_purchase_status(
        db: Session,
        purchase_id: int,
        status_data: PurchaseStatusUpdate
    ) -> Purchase:
        """Actualizar solo el estado de una compra"""
        db_purchase = PurchaseService.get_purchase_by_id(db, purchase_id)
        
        db_purchase.status = status_data.status
        
        # Si hay comentarios, agregarlos o actualizarlos
        if status_data.comments:
            if db_purchase.comments:
                db_purchase.comments += f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {status_data.comments}"
            else:
                db_purchase.comments = status_data.comments
        
        # Si el estado es CONCLUIDO y se proporciona end_date, actualizarla
        if status_data.status == PurchaseStatus.CONCLUIDO:
            if status_data.end_date:
                db_purchase.end_date = status_data.end_date
            elif not db_purchase.end_date:
                db_purchase.end_date = datetime.now()
        
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
    
    @staticmethod
    def delete_purchase(db: Session, purchase_id: int) -> bool:
        """Eliminar una compra"""
        db_purchase = PurchaseService.get_purchase_by_id(db, purchase_id)
        db.delete(db_purchase)
        db.commit()
        return True
    
    @staticmethod
    def get_purchases_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> tuple[list[Purchase], int]:
        """Obtener todas las compras de un usuario específico"""
        query = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user)
        ).filter(Purchase.user_id == user_id)
        
        total = query.count()
        purchases = query.order_by(Purchase.created_at.desc()).offset(skip).limit(limit).all()
        
        return purchases, total
    
    @staticmethod
    def get_purchases_by_sparepart(db: Session, sparepart_id: int, skip: int = 0, limit: int = 100) -> tuple[list[Purchase], int]:
        """Obtener todas las compras de una refacción específica"""
        query = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user)
        ).filter(Purchase.sparepart_id == sparepart_id)
        
        total = query.count()
        purchases = query.order_by(Purchase.created_at.desc()).offset(skip).limit(limit).all()
        
        return purchases, total
    
    @staticmethod
    def get_purchases_by_shipping_code(db: Session, shipping_code: str) -> list[Purchase]:
        """Obtener compras por código de envío"""
        return db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user)
        ).filter(Purchase.shipping_code == shipping_code).all()
    
    @staticmethod
    def get_purchase_statistics(db: Session) -> dict:
        """Obtener estadísticas de compras"""
        # Total de compras
        total_purchases = db.query(Purchase).count()
        
        # Compras por estado
        by_status = {}
        for status in PurchaseStatus:
            count = db.query(Purchase).filter(Purchase.status == status).count()
            by_status[status.value] = count
        
        # Compras por tipo
        by_type = {}
        for purchase_type in PurchaseType:
            count = db.query(Purchase).filter(Purchase.type == purchase_type).count()
            by_type[purchase_type.value] = count
        
        # Costo total de envíos
        total_shipping = db.query(func.sum(Purchase.shipping_cost)).scalar() or Decimal('0.00')
        
        return {
            "total_purchases": total_purchases,
            "by_status": by_status,
            "by_type": by_type,
            "total_shipping_cost": total_shipping
        }
    
    @staticmethod
    def get_pending_purchases(db: Session) -> list[Purchase]:
        """Obtener compras pendientes (no concluidas ni rechazadas)"""
        pending_statuses = [
            PurchaseStatus.PAUSADO_BACK_ORDERS,
            PurchaseStatus.EN_TRANSITO,
            PurchaseStatus.SOLICITUD_GUIA_ALMACEN,
            PurchaseStatus.FALTA_PAGO_PROVEEDOR,
            PurchaseStatus.FALTA_FACTURA,
            PurchaseStatus.EN_CURSO,
            PurchaseStatus.POR_REVISAR,
            PurchaseStatus.FALTA_AUTORIZACION,
            PurchaseStatus.FALTA_ORDEN_SERVICIO
        ]
        
        return db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user)
        ).filter(Purchase.status.in_(pending_statuses)).order_by(Purchase.created_at.desc()).all()