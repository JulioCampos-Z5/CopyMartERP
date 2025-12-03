from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum


class ContractStatus(str, Enum):
    PENDIENTE = "pendiente"
    SIN_FIRMAR = "sin_firmar"
    VIGENTE = "vigente"
    VENCIDO = "vencido"


# Schemas para las relaciones
class ClientBasic(BaseModel):
    client_id: int
    name: str
    comercial_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class BranchBasic(BaseModel):
    branch_id: int
    name: str
    
    class Config:
        from_attributes = True


class AreaBasic(BaseModel):
    area_id: int
    name: str
    
    class Config:
        from_attributes = True


class EquipmentBasic(BaseModel):
    item_id: int
    sku: Optional[str] = None
    model: str
    serie: str
    brand_id: int
    
    class Config:
        from_attributes = True


# Schema de creación
class RentCreate(BaseModel):
    client_id: int
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    item_id: int
    contract_status: ContractStatus = ContractStatus.PENDIENTE
    rent: float = Field(gt=0, description="Renta debe ser mayor a 0")
    is_foreign: bool = False
    
    @validator('area_id')
    def validate_area_assignment(cls, v, values):
        # Si se asigna área sin sucursal, se validará en el servicio
        if v and not values.get('branch_id'):
            pass
        return v


# Schema de actualización
class RentUpdate(BaseModel):
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    contract_status: Optional[ContractStatus] = None
    rent: Optional[float] = Field(None, gt=0)
    is_foreign: Optional[bool] = None
    is_active: Optional[bool] = None


# Schema de respuesta
class RentResponse(BaseModel):
    rent_id: int
    client_id: int
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    item_id: int
    contract_number: Optional[str] = None
    contract_status: ContractStatus
    rent: float
    is_foreign: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    client: ClientBasic
    branch: Optional[BranchBasic] = None
    area: Optional[AreaBasic] = None
    equipment: EquipmentBasic
    
    class Config:
        from_attributes = True


# Schema para listados
class RentList(BaseModel):
    rent_id: int
    contract_number: Optional[str] = None
    client_name: str
    branch_name: Optional[str] = None
    area_name: Optional[str] = None
    equipment_model: str
    equipment_serie: str
    contract_status: ContractStatus
    rent: float
    is_foreign: bool
    
    class Config:
        from_attributes = True


# Schema para filtros
class RentFilter(BaseModel):
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    contract_status: Optional[ContractStatus] = None
    is_foreign: Optional[bool] = None
    is_active: Optional[bool] = True