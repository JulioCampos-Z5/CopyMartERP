from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class ColorEnum(str, Enum):
    NA = "NA"
    K = "K"
    COLOR = "COLOR"
    Y = "Y"
    M = "M"
    C = "C"

class BrandEnum(str, Enum):
    KONICA = "KONICA"
    REPARADO_KONICA = "REPARADO KONICA"
    KYOCERA = "KYOCERA"
    TONER_EMERGENCIA = "TONER DE EMERGENCIA"
    SAMSUNG = "SAMSUNG"
    HP = "HP"
    MULTIMODELO = "MULTIMODELO"
    ESP = "ESP"
    CORSAIR = "CORSAIR"
    SILIMEX = "SILIMEX"
    SEAFON = "SEAFON"
    THERMAL_GRIZZLY = "THERMAL GRIZZLY"
    MOBI_LOCK = "MOBI LOCK"
    TP_LINK = "TP-LINK"
    MEMUNI = "MEMUNI"
    DELL = "DELL"

class SupplierEnum(str, Enum):
    KONICA = "KONICA"
    BIG99 = "BIG99"
    AMAZON = "AMAZON"
    GREBIS = "GREBIS"
    SDTA = "SDTA"
    COPYMART = "COPYMART"
    KYOCERA = "KYOCERA"
    PRINTERPARTS = "PRINTERPARTS"
    CTR = "CTR"
    CVA = "CVA"
    MERCADOLIBRE = "MERCADOLIBRE"
    COMPUACCESORIOS = "COMPUACCESORIOS"
    CAD_TONER = "CAD TONER"
    ASTA = "ASTA"
    EXEL_DEL_NORTE = "EXEL DEL NORTE"
    CORP = "CORP"
    ELECTRICA_BUGAMBILIA = "ELECTRICA BUGAMBILIA"
    ALIEXPRESS = "ALIEXPRESS"

class SparepartBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    color: Optional[str] = Field(max_length=50)
    description: Optional[str]
    brand: Optional[str] = Field(None, max_length=100)
    equipment: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=100)
    supplier: Optional[str] = Field(None, max_length=100)

class SparepartCreate(SparepartBase):
    pass

class SparepartUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    color: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    brand: Optional[str] = Field(None, max_length=100)
    equipment: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=100)
    supplier: Optional[str] = Field(None, max_length=100)

class SparepartResponse(SparepartBase):
    sparepart_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class SparepartListResponse(BaseModel):
    total: int
    items: list[SparepartResponse]
    page: int
    page_size: int
    total_pages: int