from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
from decimal import Decimal

from . import models, schemas
from equipment.models import Brand, Supplier, Equipment

class ItemCatalogService:
    """Servicio para manejar el catálogo de items (TK-410, CF283A.)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_catalog_item(self, item_data: schemas.ItemCatalogCreate) -> models.ItemCatalog:
        """Crea un nuevo item en el catálogo"""
        # Verificar que no exista otro item con el mismo nombre
        existing = self.db.query(models.ItemCatalog).filter(
            models.ItemCatalog.item_name == item_data.item_name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un item con el nombre '{item_data.item_name}'"
            )
        
        # Verificar marca si se proporcionó
        if item_data.brand_id:
            brand = self.db.query(Brand).filter(
                Brand.brand_id == item_data.brand_id
            ).first()
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Marca con ID {item_data.brand_id} no encontrada"
                )
        
        # Crear item del catálogo
        db_catalog = models.ItemCatalog(
            **item_data.model_dump(exclude={'stock_min', 'stock_max'})
        )
        self.db.add(db_catalog)
        self.db.flush()
        
        # Crear registro de stock
        db_stock = models.ItemStock(
            catalog_id=db_catalog.catalog_id,
            stock_min=item_data.stock_min,
            stock_max=item_data.stock_max
        )
        self.db.add(db_stock)
        
        self.db.commit()
        self.db.refresh(db_catalog)
        
        return db_catalog
    
    def get_catalog_item(self, catalog_id: int) -> Optional[models.ItemCatalog]:
        """Obtiene un item del catálogo por ID"""
        return self.db.query(models.ItemCatalog).filter(
            models.ItemCatalog.catalog_id == catalog_id
        ).first()
    
    def get_catalog_items(
        self,
        item_type: Optional[schemas.ItemType] = None,
        brand_id: Optional[int] = None,
        is_active: bool = True,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.ItemCatalog]:
        """Obtiene items del catálogo con filtros"""
        query = self.db.query(models.ItemCatalog)
        
        if item_type:
            query = query.filter(models.ItemCatalog.item_type == item_type)
        
        if brand_id:
            query = query.filter(models.ItemCatalog.brand_id == brand_id)
        
        if is_active is not None:
            query = query.filter(models.ItemCatalog.is_active == is_active)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    models.ItemCatalog.item_name.ilike(search_term),
                    models.ItemCatalog.description.ilike(search_term)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def update_catalog_item(
        self,
        catalog_id: int,
        item_data: schemas.ItemCatalogUpdate
    ) -> models.ItemCatalog:
        """Actualiza un item del catálogo"""
        db_catalog = self.get_catalog_item(catalog_id)
        if not db_catalog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item del catálogo con ID {catalog_id} no encontrado"
            )
        
        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_catalog, field, value)
        
        self.db.commit()
        self.db.refresh(db_catalog)
        
        return db_catalog
    
    def update_stock_levels(
        self,
        catalog_id: int,
        stock_data: schemas.StockUpdate
    ) -> models.ItemStock:
        """Actualiza los niveles de stock mínimo y máximo"""
        db_stock = self.db.query(models.ItemStock).filter(
            models.ItemStock.catalog_id == catalog_id
        ).first()
        
        if not db_stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuración de stock no encontrada para catalog_id {catalog_id}"
            )
        
        if stock_data.stock_min is not None:
            db_stock.stock_min = stock_data.stock_min
        
        if stock_data.stock_max is not None:
            db_stock.stock_max = stock_data.stock_max
        
        self.db.commit()
        self.db.refresh(db_stock)
        
        return db_stock
    
    def get_catalog_with_counts(self, catalog_id: int) -> dict:
        """Obtiene un item del catálogo con contadores de inventario"""
        catalog_item = self.get_catalog_item(catalog_id)
        if not catalog_item:
            return None
        
        # Contar total de items en inventario
        total_items = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            and_(
                models.InventoryItem.catalog_id == catalog_id,
                models.InventoryItem.is_active == True
            )
        ).scalar()
        
        # Contar items disponibles
        available_items = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            and_(
                models.InventoryItem.catalog_id == catalog_id,
                models.InventoryItem.is_active == True,
                models.InventoryItem.is_available == True
            )
        ).scalar()
        
        # Obtener stock configurado
        stock_config = self.db.query(models.ItemStock).filter(
            models.ItemStock.catalog_id == catalog_id
        ).first()
        
        return {
            "catalog_item": catalog_item,
            "total_items": total_items,
            "available_items": available_items,
            "stock_min": stock_config.stock_min if stock_config else 0,
            "stock_max": stock_config.stock_max if stock_config else 0
        }

class InventoryService:
    """Servicio para manejar instancias individuales de inventario"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _get_or_create_sequence(self, prefix: str) -> models.InventorySequence:
        """Obtiene o crea una secuencia para un prefijo dado"""
        sequence = self.db.query(models.InventorySequence).filter(
            models.InventorySequence.prefix == prefix
        ).first()
        
        if not sequence:
            sequence = models.InventorySequence(prefix=prefix, current_value=0)
            self.db.add(sequence)
            self.db.commit()
            self.db.refresh(sequence)
        
        return sequence
    
    def _generate_item_code(self, catalog_item: models.ItemCatalog, quality: str) -> str:
        """Genera el código del item basado en tipo y calidad"""
        # Determinar prefijo
        if catalog_item.item_type == schemas.ItemType.TONER:
            if quality == schemas.QualityType.GENERICO:
                prefix = "TG"
            elif quality == schemas.QualityType.ORIGINAL:
                prefix = "TO"
            else:
                prefix = "TG"
        elif catalog_item.item_type == schemas.ItemType.REFACCION:
            if quality == schemas.QualityType.NUEVA:
                prefix = "RN"
            elif quality == schemas.QualityType.REPARADO:
                prefix = "RR"
            elif quality == schemas.QualityType.USADO:
                prefix = "RU"
            else:
                prefix = "RN"
        else:
            prefix = "GEN"
        
        # Obtener y actualizar secuencia
        sequence = self._get_or_create_sequence(prefix)
        sequence.current_value += 1
        self.db.commit()
        
        # Generar código con formato: PREFIX-NNNN
        item_code = f"{prefix}-{sequence.current_value:04d}"
        return item_code
    
    def create_item(self, item_data: schemas.InventoryItemCreate) -> models.InventoryItem:
        """Crea una nueva instancia de inventario"""
        # Verificar que el item del catálogo existe
        catalog_item = self.db.query(models.ItemCatalog).filter(
            models.ItemCatalog.catalog_id == item_data.catalog_id
        ).first()
        
        if not catalog_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item del catálogo con ID {item_data.catalog_id} no encontrado"
            )
        
        # Verificar proveedor si se proporcionó
        if item_data.supplier_id:
            supplier = self.db.query(Supplier).filter(
                Supplier.supplier_id == item_data.supplier_id
            ).first()
            if not supplier:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proveedor con ID {item_data.supplier_id} no encontrado"
                )
        
        # Verificar anaquel si se proporcionó
        if item_data.shelf_id:
            shelf = self.db.query(models.Shelf).filter(
                models.Shelf.shelf_id == item_data.shelf_id
            ).first()
            if not shelf:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Anaquel con ID {item_data.shelf_id} no encontrado"
                )
        
        # Generar código automático
        item_code = self._generate_item_code(catalog_item, item_data.quality)
        
        # Crear el item
        db_item = models.InventoryItem(
            item_code=item_code,
            **item_data.model_dump(exclude={'equipment_ids'})
        )
        
        # Agregar equipos relacionados si se proporcionaron
        if item_data.equipment_ids:
            equipments = self.db.query(Equipment).filter(
                Equipment.item_id.in_(item_data.equipment_ids)
            ).all()
            db_item.equipments.extend(equipments)
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        
        return db_item
    
    def create_bulk_items(self, bulk_data: schemas.BulkInventoryCreate) -> List[models.InventoryItem]:
        """Crea múltiples instancias de un item a la vez"""
        created_items = []
        
        for _ in range(bulk_data.quantity):
            item_data = schemas.InventoryItemCreate(
                catalog_id=bulk_data.catalog_id,
                section=bulk_data.section,
                shelf_id=bulk_data.shelf_id,
                quality=bulk_data.quality,
                supplier_id=bulk_data.supplier_id,
                invoice=bulk_data.invoice,
                cost=bulk_data.cost,
                comments=bulk_data.comments,
                equipment_ids=bulk_data.equipment_ids
            )
            created_item = self.create_item(item_data)
            created_items.append(created_item)
        
        return created_items
    
    def get_item(self, inventory_id: int) -> Optional[models.InventoryItem]:
        """Obtiene un item por ID"""
        return self.db.query(models.InventoryItem).filter(
            models.InventoryItem.inventory_id == inventory_id
        ).first()
    
    def get_item_by_code(self, item_code: str) -> Optional[models.InventoryItem]:
        """Obtiene un item por su código"""
        return self.db.query(models.InventoryItem).filter(
            models.InventoryItem.item_code == item_code
        ).first()
    
    def get_items(
        self,
        filters: schemas.InventoryFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.InventoryItem]:
        """Obtiene items con filtros"""
        query = self.db.query(models.InventoryItem)
        
        # Join con catalog para filtros relacionados
        if filters.item_type or filters.brand_id or filters.color or filters.item_name:
            query = query.join(models.ItemCatalog)
        
        if filters.catalog_id:
            query = query.filter(models.InventoryItem.catalog_id == filters.catalog_id)
        
        if filters.item_name:
            query = query.filter(models.ItemCatalog.item_name.ilike(f"%{filters.item_name}%"))
        
        if filters.item_type:
            query = query.filter(models.ItemCatalog.item_type == filters.item_type)
        
        if filters.brand_id:
            query = query.filter(models.ItemCatalog.brand_id == filters.brand_id)
        
        if filters.color:
            query = query.filter(models.ItemCatalog.color == filters.color)
        
        if filters.section:
            query = query.filter(models.InventoryItem.section == filters.section)
        
        if filters.quality:
            query = query.filter(models.InventoryItem.quality == filters.quality)
        
        if filters.shelf_id:
            query = query.filter(models.InventoryItem.shelf_id == filters.shelf_id)
        
        if filters.supplier_id:
            query = query.filter(models.InventoryItem.supplier_id == filters.supplier_id)
        
        if filters.is_available is not None:
            query = query.filter(models.InventoryItem.is_available == filters.is_available)
        
        if filters.is_active is not None:
            query = query.filter(models.InventoryItem.is_active == filters.is_active)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    models.InventoryItem.item_code.ilike(search_term),
                    models.InventoryItem.comments.ilike(search_term)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def update_item(
        self,
        inventory_id: int,
        item_data: schemas.InventoryItemUpdate
    ) -> models.InventoryItem:
        """Actualiza un item de inventario"""
        db_item = self.get_item(inventory_id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item con ID {inventory_id} no encontrado"
            )
        
        # Actualizar equipos si se proporcionaron
        if item_data.equipment_ids is not None:
            equipments = self.db.query(Equipment).filter(
                Equipment.item_id.in_(item_data.equipment_ids)
            ).all()
            db_item.equipments = equipments
        
        # Actualizar otros campos
        update_data = item_data.model_dump(exclude_unset=True, exclude={'equipment_ids'})
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_item)
        
        return db_item
    
    def mark_as_unavailable(self, inventory_id: int) -> models.InventoryItem:
        """Marca un item como no disponible (usado/asignado)"""
        db_item = self.get_item(inventory_id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item con ID {inventory_id} no encontrado"
            )
        
        db_item.is_available = False
        db_item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_item)
        
        return db_item
    
    def delete_item(self, inventory_id: int) -> bool:
        """Elimina (desactiva) un item de inventario"""
        db_item = self.get_item(inventory_id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item con ID {inventory_id} no encontrado"
            )
        
        db_item.is_active = False
        db_item.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def get_statistics(self) -> schemas.InventoryStats:
        """Obtiene estadísticas del inventario"""
        # Total de items en catálogo
        total_catalog_items = self.db.query(func.count(models.ItemCatalog.catalog_id)).filter(
            models.ItemCatalog.is_active == True
        ).scalar()
        
        # Total de instancias en inventario
        total_inventory_items = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            models.InventoryItem.is_active == True
        ).scalar()
        
        # Items disponibles
        available_items = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            and_(
                models.InventoryItem.is_active == True,
                models.InventoryItem.is_available == True
            )
        ).scalar()
        
        # Contadores por tipo (requiere join con catálogo)
        total_toners = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            and_(
                models.InventoryItem.is_active == True,
                models.InventoryItem.catalog_id == models.ItemCatalog.catalog_id,
                models.ItemCatalog.item_type == schemas.ItemType.TONER
            )
        ).scalar()
        
        total_refacciones = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            and_(
                models.InventoryItem.is_active == True,
                models.InventoryItem.catalog_id == models.ItemCatalog.catalog_id,
                models.ItemCatalog.item_type == schemas.ItemType.REFACCION
            )
        ).scalar()
        
        # Items con stock bajo (comparar con stock_min)
        low_stock_count = 0
        catalog_items = self.db.query(models.ItemCatalog).filter(
            models.ItemCatalog.is_active == True
        ).all()
        
        for cat_item in catalog_items:
            current = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
                and_(
                    models.InventoryItem.catalog_id == cat_item.catalog_id,
                    models.InventoryItem.is_active == True,
                    models.InventoryItem.is_available == True
                )
            ).scalar()
            
            stock_config = self.db.query(models.ItemStock).filter(
                models.ItemStock.catalog_id == cat_item.catalog_id
            ).first()
            
            if stock_config and current < stock_config.stock_min:
                low_stock_count += 1
        
        # Items por sección
        items_by_section = {}
        for section in schemas.SectionLocation:
            count = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
                and_(
                    models.InventoryItem.is_active == True,
                    models.InventoryItem.section == section
                )
            ).scalar()
            items_by_section[section.value] = count
        
        # Items por calidad
        items_by_quality = {}
        for quality in schemas.QualityType:
            count = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
                and_(
                    models.InventoryItem.is_active == True,
                    models.InventoryItem.quality == quality
                )
            ).scalar()
            items_by_quality[quality.value] = count
        
        # Valor total
        total_value = self.db.query(func.sum(models.InventoryItem.cost)).filter(
            and_(
                models.InventoryItem.is_active == True,
                models.InventoryItem.is_available == True
            )
        ).scalar() or Decimal(0)
        
        return schemas.InventoryStats(
            total_catalog_items=total_catalog_items,
            total_inventory_items=total_inventory_items,
            total_toners=total_toners,
            total_refacciones=total_refacciones,
            available_items=available_items,
            low_stock_items=low_stock_count,
            items_by_section=items_by_section,
            items_by_quality=items_by_quality,
            total_value=total_value
        )

class ShelfService:
    """Servicio para manejar anaqueles"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_shelf(self, shelf_data: schemas.ShelfCreate) -> models.Shelf:
        """Crea un nuevo anaquel"""
        existing = self.db.query(models.Shelf).filter(
            models.Shelf.name == shelf_data.name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un anaquel con el nombre '{shelf_data.name}'"
            )
        
        db_shelf = models.Shelf(**shelf_data.model_dump())
        self.db.add(db_shelf)
        self.db.commit()
        self.db.refresh(db_shelf)
        
        return db_shelf
    
    def get_shelf(self, shelf_id: int) -> Optional[models.Shelf]:
        """Obtiene un anaquel por ID"""
        return self.db.query(models.Shelf).filter(
            models.Shelf.shelf_id == shelf_id
        ).first()
    
    def get_shelves(
        self,
        section: Optional[schemas.SectionLocation] = None,
        is_active: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Shelf]:
        """Obtiene anaqueles con filtros"""
        query = self.db.query(models.Shelf)
        
        if section:
            query = query.filter(models.Shelf.section == section)
        
        if is_active is not None:
            query = query.filter(models.Shelf.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def update_shelf(
        self,
        shelf_id: int,
        shelf_data: schemas.ShelfUpdate
    ) -> models.Shelf:
        """Actualiza un anaquel"""
        db_shelf = self.get_shelf(shelf_id)
        if not db_shelf:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Anaquel con ID {shelf_id} no encontrado"
            )
        
        update_data = shelf_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_shelf, field, value)
        
        self.db.commit()
        self.db.refresh(db_shelf)
        
        return db_shelf
    
    def delete_shelf(self, shelf_id: int) -> bool:
        """Elimina (desactiva) un anaquel"""
        db_shelf = self.get_shelf(shelf_id)
        if not db_shelf:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Anaquel con ID {shelf_id} no encontrado"
            )
        
        items_count = self.db.query(func.count(models.InventoryItem.inventory_id)).filter(
            models.InventoryItem.shelf_id == shelf_id,
            models.InventoryItem.is_active == True
        ).scalar()
        
        if items_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el anaquel porque tiene {items_count} items asignados"
            )
        
        db_shelf.is_active = False
        self.db.commit()
        
        return True