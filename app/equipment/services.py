"""
==============================================================================
MÓDULO DE EQUIPOS - SERVICIOS
==============================================================================
Lógica de negocio para la gestión de equipos, marcas y proveedores.

Funciones principales:
  - create_brand()           -> Crea una marca nueva
  - create_supplier()        -> Crea un proveedor nuevo
  - create_equipment()       -> Crea equipo con SKU automático
  - update_equipment()       -> Actualiza todos los datos de un equipo
  - update_equipment_status() -> Cambia solo la ubicación del equipo

Actualizado: 3 de diciembre de 2025
==============================================================================
"""

from sqlalchemy.orm import Session
from app.equipment.models import Brand, Supplier, Equipment
from app.equipment.schemas import SupplierCreate, BrandCreate, EquipmentCreate, EquipmentUpdate


def create_brand(db: Session, brand_data: BrandCreate):
    """
    Crea una nueva marca de equipos.
    
    El prefijo se guarda en minúsculas para estandarizar la generación de SKUs.
    
    Args:
        db: Sesión de base de datos
        brand_data: Datos de la marca (name, prefix)
    
    Returns:
        Brand: Marca creada
    """
    brand = Brand(
        name=brand_data.name,
        prefix=brand_data.prefix.lower()  # Normalizar a minúsculas
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


def create_supplier(db: Session, supplier_data: SupplierCreate):
    """
    Crea un nuevo proveedor de equipos.
    
    Args:
        db: Sesión de base de datos
        supplier_data: Datos del proveedor (name)
    
    Returns:
        Supplier: Proveedor creado
    """
    supplier = Supplier(name=supplier_data.name)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def create_equipment(db: Session, equipment_data: EquipmentCreate):
    """
    Crea un nuevo equipo con generación automática de SKU.
    
    El SKU se genera con el formato: {prefijo_marca}{número_secuencial}
    Ejemplo: hp01, hp02, canon01, xerox01, etc.
    
    El número secuencial se calcula buscando el último equipo de la misma marca
    y sumándole 1.
    
    Args:
        db: Sesión de base de datos
        equipment_data: Datos del equipo a crear
    
    Returns:
        Equipment: Equipo creado con SKU asignado
    
    Raises:
        ValueError: Si la marca especificada no existe
    """
    # Verificar que la marca existe
    brand = db.query(Brand).filter(Brand.brand_id == equipment_data.brand_id).first()
    if not brand:
        raise ValueError("Brand not found")

    # Calcular el siguiente número de SKU para esta marca
    last_equipment = (
        db.query(Equipment)
        .filter(Equipment.brand_id == brand.brand_id)
        .order_by(Equipment.item_id.desc())
        .first()
    )
    
    if last_equipment:
        # Extraer el número del último SKU y sumarle 1
        last_number = int(last_equipment.sku[len(brand.prefix):])
        new_number = last_number + 1
    else:
        # Primer equipo de esta marca
        new_number = 1

    # Generar SKU: prefijo + número con 2 dígitos (ej: hp01, canon05)
    sku = f"{brand.prefix}{str(new_number).zfill(2)}"

    # Crear el equipo
    equipment = Equipment(
        sku=sku,
        brand_id=brand.brand_id,
        model=equipment_data.model,
        serie=equipment_data.serie,
        model_toner=equipment_data.model_toner,
        type=equipment_data.type,
        supplier_id=equipment_data.supplier_id,
        invoice=equipment_data.invoice,
        cost=equipment_data.cost,
        location_status=equipment_data.location_status,
        comments=equipment_data.comments,
        is_active=equipment_data.is_active
    )

    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


def update_equipment(db: Session, item_id: int, equipment_data: EquipmentCreate):
    """
    Actualiza todos los datos de un equipo existente.
    
    NOTA IMPORTANTE: El SKU NO se modifica aunque se cambie la marca.
    Esto es intencional para mantener la trazabilidad del equipo.
    
    Args:
        db: Sesión de base de datos
        item_id: ID del equipo a actualizar
        equipment_data: Nuevos datos del equipo
    
    Returns:
        Equipment: Equipo actualizado
    
    Raises:
        ValueError: Si el equipo no existe
    """
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise ValueError("Equipment not found")
    
    # Actualizar todos los campos editables (excepto SKU)
    equipment.brand_id = equipment_data.brand_id
    equipment.model = equipment_data.model
    equipment.serie = equipment_data.serie
    equipment.model_toner = equipment_data.model_toner
    equipment.type = equipment_data.type
    equipment.supplier_id = equipment_data.supplier_id
    equipment.invoice = equipment_data.invoice
    equipment.cost = equipment_data.cost
    equipment.location_status = equipment_data.location_status
    equipment.comments = equipment_data.comments
    equipment.is_active = equipment_data.is_active
    
    db.commit()
    db.refresh(equipment)
    return equipment


def update_equipment_status(db: Session, item_id: int, new_status: str):
    """
    Actualiza únicamente la ubicación/estado de un equipo.
    
    Útil para cambios rápidos de ubicación sin modificar otros datos.
    Estados válidos: bodega, asignado, vendido, taller, desconocido
    
    Args:
        db: Sesión de base de datos
        item_id: ID del equipo
        new_status: Nueva ubicación del equipo
    
    Returns:
        Equipment: Equipo con ubicación actualizada
    
    Raises:
        ValueError: Si el equipo no existe
    """
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise ValueError("Equipment not found")
    
    equipment.location_status = new_status
    db.commit()
    db.refresh(equipment)
    return equipment