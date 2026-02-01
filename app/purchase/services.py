from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, and_
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
from decimal import Decimal

from purchase.models import Purchase, PurchaseStatus, PurchaseType
from sparepart.models import Sparepart
from contact.models import Contact
from purchase.schemas import (
    PurchaseCreate, 
    PurchaseUpdate, 
    PurchaseStatusUpdate,
    PurchaseAuthorizationUpdate
)

class PurchaseService:
    
    @staticmethod
    def create_purchase(db: Session, purchase_data: PurchaseCreate) -> Purchase:
        """Crear una nueva compra"""
        # Verificar que existe la refacción
        sparepart = db.query(Sparepart).filter(
            Sparepart.sparepart_id == purchase_data.sparepart_id
        ).first()
        if not sparepart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Refacción con ID {purchase_data.sparepart_id} no encontrada"
            )
        
        # Verificar que existe el usuario
        user = db.query(Contact).filter(
            Contact.contact_id == purchase_data.user_id
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {purchase_data.user_id} no encontrado"
            )
        
        # Validar proveedores
        suppliers = [
            (purchase_data.supplier1_name, purchase_data.supplier1_cost),
            (purchase_data.supplier2_name, purchase_data.supplier2_cost),
            (purchase_data.supplier3_name, purchase_data.supplier3_cost)
        ]
        
        for i, (name, cost) in enumerate(suppliers, 1):
            if (name and cost is None) or (cost is not None and not name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Proveedor {i}: si proporciona nombre debe proporcionar costo y viceversa"
                )
        
        db_purchase = Purchase(**purchase_data.model_dump())
        db.add(db_purchase)
        db.commit()
        db.refresh(db_purchase)
        
        return db_purchase
    
    @staticmethod
    def get_purchase_by_id(db: Session, purchase_id: int) -> Purchase:
        """Obtener una compra por ID con sus relaciones"""
        purchase = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
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
        end_date: Optional[datetime] = None,
        pending_authorization: Optional[bool] = None,
        is_paid: Optional[bool] = None
    ) -> tuple[list[Purchase], int]:
        """Obtener todas las compras con filtros y paginación"""
        query = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
        )
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                Purchase.name.ilike(f"%{search}%"),
                Purchase.shipping_code.ilike(f"%{search}%"),
                Purchase.comments.ilike(f"%{search}%"),
                Purchase.supplier1_name.ilike(f"%{search}%"),
                Purchase.supplier2_name.ilike(f"%{search}%"),
                Purchase.supplier3_name.ilike(f"%{search}%")
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
        
        if pending_authorization is not None:
            if pending_authorization:
                query = query.filter(
                    or_(
                        Purchase.authorized_by_area_chief_id.is_(None),
                        Purchase.authorized_by_admin_id.is_(None)
                    )
                )
            else:
                query = query.filter(
                    and_(
                        Purchase.authorized_by_area_chief_id.isnot(None),
                        Purchase.authorized_by_admin_id.isnot(None)
                    )
                )
        
        if is_paid is not None:
            query = query.filter(Purchase.is_paid == is_paid)
        
        # Obtener total
        total = query.count()
        
        # Aplicar paginación y ordenar
        purchases = query.order_by(
            Purchase.created_at.desc()
        ).offset(skip).limit(limit).all()
        
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
        
        # Validar proveedores si se están actualizando
        if any(k.startswith('supplier') for k in update_data.keys()):
            suppliers = [
                (
                    update_data.get('supplier1_name', db_purchase.supplier1_name),
                    update_data.get('supplier1_cost', db_purchase.supplier1_cost)
                ),
                (
                    update_data.get('supplier2_name', db_purchase.supplier2_name),
                    update_data.get('supplier2_cost', db_purchase.supplier2_cost)
                ),
                (
                    update_data.get('supplier3_name', db_purchase.supplier3_name),
                    update_data.get('supplier3_cost', db_purchase.supplier3_cost)
                )
            ]
            
            for i, (name, cost) in enumerate(suppliers, 1):
                if (name and cost is None) or (cost is not None and not name):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Proveedor {i}: debe proporcionar nombre y costo juntos"
                    )
        
        for field, value in update_data.items():
            setattr(db_purchase, field, value)
        
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
    
    @staticmethod
    def authorize_by_area_chief(
        db: Session,
        purchase_id: int,
        chief_id: int,
        authorization_data: PurchaseAuthorizationUpdate
    ) -> Purchase:
        """Autorizar compra por jefe de área"""
        db_purchase = PurchaseService.get_purchase_by_id(db, purchase_id)
        
        # Verificar que el jefe existe
        chief = db.query(Contact).filter(Contact.contact_id == chief_id).first()
        if not chief:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {chief_id} no encontrado"
            )
        
        db_purchase.authorized_by_area_chief_id = chief_id
        db_purchase.authorized_by_area_chief_date = datetime.now()
        
        if authorization_data.authorized_amount is not None:
            db_purchase.authorized_amount = authorization_data.authorized_amount
        
        if authorization_data.comments:
            comment = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Autorización Jefe Área: {authorization_data.comments}"
            db_purchase.comments = (db_purchase.comments or "") + comment
        
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
    
    @staticmethod
    def authorize_by_admin(
        db: Session,
        purchase_id: int,
        admin_id: int,
        authorization_data: PurchaseAuthorizationUpdate
    ) -> Purchase:
        """Autorizar compra por administrador"""
        db_purchase = PurchaseService.get_purchase_by_id(db, purchase_id)
        
        # Verificar que el admin existe
        admin = db.query(Contact).filter(Contact.contact_id == admin_id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {admin_id} no encontrado"
            )
        
        db_purchase.authorized_by_admin_id = admin_id
        db_purchase.authorized_by_admin_date = datetime.now()
        
        if authorization_data.authorized_amount is not None:
            db_purchase.authorized_amount = authorization_data.authorized_amount
        
        if authorization_data.comments:
            comment = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Autorización Admin: {authorization_data.comments}"
            db_purchase.comments = (db_purchase.comments or "") + comment
        
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
        
        if status_data.comments:
            comment = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {status_data.comments}"
            db_purchase.comments = (db_purchase.comments or "") + comment
        
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
    def get_purchases_by_user(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[list[Purchase], int]:
        """Obtener todas las compras de un usuario específico"""
        query = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
        ).filter(Purchase.user_id == user_id)
        
        total = query.count()
        purchases = query.order_by(
            Purchase.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return purchases, total
    
    @staticmethod
    def get_purchases_by_sparepart(
        db: Session, 
        sparepart_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[list[Purchase], int]:
        """Obtener todas las compras de una refacción específica"""
        query = db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
        ).filter(Purchase.sparepart_id == sparepart_id)
        
        total = query.count()
        purchases = query.order_by(
            Purchase.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return purchases, total
    
    @staticmethod
    def get_purchases_by_shipping_code(db: Session, shipping_code: str) -> list[Purchase]:
        """Obtener compras por código de envío"""
        return db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
        ).filter(Purchase.shipping_code == shipping_code).all()
    
    @staticmethod
    def get_purchase_statistics(db: Session) -> dict:
        """Obtener estadísticas de compras"""
        total_purchases = db.query(Purchase).count()
        
        by_status = {}
        for purchase_status in PurchaseStatus:
            count = db.query(Purchase).filter(
                Purchase.status == purchase_status
            ).count()
            by_status[purchase_status.value] = count
        
        by_type = {}
        for purchase_type in PurchaseType:
            count = db.query(Purchase).filter(
                Purchase.type == purchase_type
            ).count()
            by_type[purchase_type.value] = count
        
        total_shipping = db.query(
            func.sum(Purchase.shipping_cost)
        ).scalar() or Decimal('0.00')
        
        pending_authorizations = db.query(Purchase).filter(
            or_(
                Purchase.authorized_by_area_chief_id.is_(None),
                Purchase.authorized_by_admin_id.is_(None)
            )
        ).count()
        
        total_authorized = db.query(Purchase).filter(
            and_(
                Purchase.authorized_by_area_chief_id.isnot(None),
                Purchase.authorized_by_admin_id.isnot(None)
            )
        ).count()
        
        return {
            "total_purchases": total_purchases,
            "by_status": by_status,
            "by_type": by_type,
            "total_shipping_cost": total_shipping,
            "pending_authorizations": pending_authorizations,
            "total_authorized": total_authorized
        }
    
    @staticmethod
    def get_pending_purchases(db: Session) -> list[Purchase]:
        """Obtener compras pendientes"""
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
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
        ).filter(
            Purchase.status.in_(pending_statuses)
        ).order_by(Purchase.created_at.desc()).all()
    
    @staticmethod
    def get_pending_authorizations(db: Session) -> list[Purchase]:
        """Obtener compras pendientes de autorización"""
        return db.query(Purchase).options(
            joinedload(Purchase.sparepart),
            joinedload(Purchase.user),
            joinedload(Purchase.authorized_by_area_chief),
            joinedload(Purchase.authorized_by_admin)
        ).filter(
            or_(
                Purchase.authorized_by_area_chief_id.is_(None),
                Purchase.authorized_by_admin_id.is_(None)
            )
        ).order_by(Purchase.created_at.desc()).all()