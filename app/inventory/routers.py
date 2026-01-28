from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from . import schemas, services

catalog_router = APIRouter(prefix="/catalog", tags=["Item Catalog"])
inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])
shelf_router = APIRouter(prefix="/shelves", tags=["Shelves"])


@catalog_router.post("/", response_model=schemas.ItemCatalogResponse, status_code=status.HTTP_201_CREATED)
def create_catalog_item(
    item: schemas.ItemCatalogCreate,
    db: Session = Depends(get_db)
):
    service = services.ItemCatalogService(db)
    return service.create_catalog_item(item)

@catalog_router.get("/", response_model=List[schemas.ItemCatalogResponse])
def get_catalog_items(
    item_type: Optional[schemas.ItemType] = None,
    brand_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Obtiene items del catálogo con filtros opcionales.
    """
    service = services.ItemCatalogService(db)
    items = service.get_catalog_items(item_type, brand_id, is_active, search, skip, limit)
    
    # Agregar contadores a cada item
    result = []
    for item in items:
        counts = service.get_catalog_with_counts(item.catalog_id)
        item_dict = schemas.ItemCatalogResponse.model_validate(item).model_dump()
        item_dict['total_items'] = counts['total_items']
        item_dict['available_items'] = counts['available_items']
        item_dict['stock_min'] = counts['stock_min']
        item_dict['stock_max'] = counts['stock_max']
        result.append(item_dict)
    
    return result

@catalog_router.get("/{catalog_id}", response_model=schemas.ItemCatalogResponse)
def get_catalog_item(
    catalog_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un item del catálogo por ID con contadores de inventario"""
    service = services.ItemCatalogService(db)
    counts = service.get_catalog_with_counts(catalog_id)
    
    if not counts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item del catálogo con ID {catalog_id} no encontrado"
        )
    
    item_dict = schemas.ItemCatalogResponse.model_validate(counts['catalog_item']).model_dump()
    item_dict['total_items'] = counts['total_items']
    item_dict['available_items'] = counts['available_items']
    item_dict['stock_min'] = counts['stock_min']
    item_dict['stock_max'] = counts['stock_max']
    
    return item_dict

@catalog_router.put("/{catalog_id}", response_model=schemas.ItemCatalogResponse)
def update_catalog_item(
    catalog_id: int,
    item: schemas.ItemCatalogUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un item del catálogo"""
    service = services.ItemCatalogService(db)
    return service.update_catalog_item(catalog_id, item)

@catalog_router.patch("/{catalog_id}/stock")
def update_stock_levels(
    catalog_id: int,
    stock_data: schemas.StockUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza los niveles de stock mínimo y máximo para un item del catálogo"""
    service = services.ItemCatalogService(db)
    return service.update_stock_levels(catalog_id, stock_data)


@inventory_router.post("/", response_model=schemas.InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item: schemas.InventoryItemCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva instancia de inventario.
    El código (TG-0001, TO-0002, etc.) se genera automáticamente.
    """
    service = services.InventoryService(db)
    return service.create_item(item)

@inventory_router.post("/bulk", response_model=List[schemas.InventoryItemResponse], status_code=status.HTTP_201_CREATED)
def create_bulk_inventory(
    bulk_data: schemas.BulkInventoryCreate,
    db: Session = Depends(get_db)
):
    """
    Crea múltiples instancias de un item a la vez.
    Útil cuando recibes varias unidades del mismo item en una compra.
    """
    service = services.InventoryService(db)
    return service.create_bulk_items(bulk_data)

@inventory_router.get("/", response_model=List[schemas.InventoryItemResponse])
def get_inventory_items(
    catalog_id: Optional[int] = None,
    item_name: Optional[str] = None,
    item_type: Optional[schemas.ItemType] = None,
    section: Optional[schemas.SectionLocation] = None,
    brand_id: Optional[int] = None,
    quality: Optional[schemas.QualityType] = None,
    color: Optional[schemas.ColorType] = None,
    shelf_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    is_available: Optional[bool] = None,
    is_active: Optional[bool] = True,
    low_stock: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Obtiene instancias de inventario con filtros opcionales.
    - catalog_id: Filtrar por item del catálogo específico
    - item_name: Buscar por nombre (TK-410, CF283A, etc.)
    - is_available: Filtrar por items disponibles/no disponibles
    """
    filters = schemas.InventoryFilter(
        catalog_id=catalog_id,
        item_name=item_name,
        item_type=item_type,
        section=section,
        brand_id=brand_id,
        quality=quality,
        color=color,
        shelf_id=shelf_id,
        supplier_id=supplier_id,
        is_available=is_available,
        is_active=is_active,
        low_stock=low_stock,
        search=search
    )
    service = services.InventoryService(db)
    return service.get_items(filters, skip, limit)

@inventory_router.get("/stats", response_model=schemas.InventoryStats)
def get_inventory_statistics(db: Session = Depends(get_db)):
    """Obtiene estadísticas generales del inventario"""
    service = services.InventoryService(db)
    return service.get_statistics()

@inventory_router.get("/{inventory_id}", response_model=schemas.InventoryItemResponse)
def get_inventory_item(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene una instancia de inventario por ID"""
    service = services.InventoryService(db)
    item = service.get_item(inventory_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {inventory_id} no encontrado"
        )
    return item

@inventory_router.get("/code/{item_code}", response_model=schemas.InventoryItemResponse)
def get_inventory_item_by_code(
    item_code: str,
    db: Session = Depends(get_db)
):
    """Obtiene una instancia de inventario por su código (ej: TG-0001, RN-0042)"""
    service = services.InventoryService(db)
    item = service.get_item_by_code(item_code)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con código '{item_code}' no encontrado"
        )
    return item

@inventory_router.put("/{inventory_id}", response_model=schemas.InventoryItemResponse)
def update_inventory_item(
    inventory_id: int,
    item: schemas.InventoryItemUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza una instancia de inventario"""
    service = services.InventoryService(db)
    return service.update_item(inventory_id, item)

@inventory_router.patch("/{inventory_id}/mark-unavailable", response_model=schemas.InventoryItemResponse)
def mark_item_unavailable(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    """
    Marca un item como no disponible (usado/asignado).
    Útil cuando se usa un toner o refacción.
    """
    service = services.InventoryService(db)
    return service.mark_as_unavailable(inventory_id)

@inventory_router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    """Elimina (desactiva) una instancia de inventario"""
    service = services.InventoryService(db)
    service.delete_item(inventory_id)
    return None


@shelf_router.post("/", response_model=schemas.ShelfResponse, status_code=status.HTTP_201_CREATED)
def create_shelf(
    shelf: schemas.ShelfCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo anaquel"""
    service = services.ShelfService(db)
    return service.create_shelf(shelf)

@shelf_router.get("/", response_model=List[schemas.ShelfResponse])
def get_shelves(
    section: Optional[schemas.SectionLocation] = None,
    is_active: Optional[bool] = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Obtiene anaqueles con filtros opcionales"""
    service = services.ShelfService(db)
    return service.get_shelves(section, is_active, skip, limit)

@shelf_router.get("/{shelf_id}", response_model=schemas.ShelfResponse)
def get_shelf(
    shelf_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un anaquel por ID"""
    service = services.ShelfService(db)
    shelf = service.get_shelf(shelf_id)
    if not shelf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anaquel con ID {shelf_id} no encontrado"
        )
    return shelf

@shelf_router.put("/{shelf_id}", response_model=schemas.ShelfResponse)
def update_shelf(
    shelf_id: int,
    shelf: schemas.ShelfUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un anaquel"""
    service = services.ShelfService(db)
    return service.update_shelf(shelf_id, shelf)

@shelf_router.delete("/{shelf_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shelf(
    shelf_id: int,
    db: Session = Depends(get_db)
):
    """Elimina (desactiva) un anaquel"""
    service = services.ShelfService(db)
    service.delete_shelf(shelf_id)
    return None