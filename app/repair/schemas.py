from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
class TallerStatusEnum(str, Enum):
    PENDIENTE = "pendiente"
    PAUSADO = "pausado"
    LISTO = "listo"

class TallerLocationEnum(str, Enum):
    ZONA_1 = "zona_1"
    ZONA_2 = "zona_2"
    ZONA_3 = "zona_3"
    ZONA_4 = "zona_4"
    BASURA = "basura"

class TallerProcessEnum(str, Enum):
    DESCONOCIDO = "desconocido"
    PROCESO_1 = "proceso_1"
    PROCESO_2 = "proceso_2"
    PROCESO_3 = "proceso_3"

class TallerEstatusEnum(str, Enum):
    EN_ESPERA_AUTORIZACION = "en_espera_autorizacion"
    EN_ESPERA_PIEZA = "en_espera_pieza"
    PAUSADO = "pausado"
    LISTO = "listo"

class ProcedenciaEnum(str, Enum):
    BODEGA = "bodega"
    ASIGNADO = "asignado"
    VENDIDO = "vendido"
    DESCONOCIDO = "desconocido"

# Schema base
class RepairBase(BaseModel):
    procedencia: ProcedenciaEnum
    estado_taller: Optional[TallerStatusEnum] = TallerStatusEnum.PENDIENTE
    ubicacion: Optional[TallerLocationEnum] = None
    proceso: Optional[TallerProcessEnum] = TallerProcessEnum.DESCONOCIDO
    estatus: Optional[TallerEstatusEnum] = TallerEstatusEnum.EN_ESPERA_AUTORIZACION
    diagnostico_inicial: Optional[str] = None
    comments: Optional[str] = None

# Schema para crear un repair
class RepairCreate(RepairBase):
    item_id: int = Field(..., description="ID del equipo a reparar")

# Schema para actualizar un repair
class RepairUpdate(BaseModel):
    estado_taller: Optional[TallerStatusEnum] = None
    fecha_conclusion: Optional[datetime] = None
    ubicacion: Optional[TallerLocationEnum] = None
    proceso: Optional[TallerProcessEnum] = None
    estatus: Optional[TallerEstatusEnum] = None
    diagnostico_inicial: Optional[str] = None
    comments: Optional[str] = None
    is_active: Optional[bool] = None

# Schema para subir archivos
class RepairFileUpload(BaseModel):
    folio_escaneado: Optional[str] = None
    foto_evidencia: Optional[str] = None

# Schema de respuesta - información del equipo
class EquipmentInfo(BaseModel):
    item_id: int
    sku: Optional[str]
    brand_name: Optional[str]
    model: str
    serie: str
    model_toner: str
    location_status: str

    class Config:
        from_attributes = True

# Schema de respuesta completo
class RepairResponse(RepairBase):
    repair_id: int
    item_id: int
    model: str
    serie: str
    model_toner: str
    fecha_alta: datetime
    fecha_conclusion: Optional[datetime]
    folio_escaneado: Optional[str]
    foto_evidencia: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    # Información del equipo relacionado
    equipment: Optional[EquipmentInfo] = None

    class Config:
        from_attributes = True

# Schema para listados con paginación
class RepairList(BaseModel):
    total: int
    page: int
    page_size: int
    repairs: list[RepairResponse]

# Schema para cambiar estado del equipo
class ChangeEquipmentStatus(BaseModel):
    item_id: int
    new_status: str = Field(..., description="bodega o taller")