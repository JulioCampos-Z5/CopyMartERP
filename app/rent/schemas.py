from pydantic import BaseModel, Field, field_validator, model_serializer
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional, Any
from datetime import date, datetime
from decimal import Decimal
from rent.models import ContractStatus


class RentBase(BaseModel):
    client_id: int = Field(..., gt=0)
    branch_id: Optional[int] = Field(None, gt=0)
    area_id: Optional[int] = Field(None, gt=0)
    item_id: int = Field(..., gt=0)
    rent: Decimal = Field(..., gt=0, description="Renta mensual base")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_foreign: bool = False
    
    # Configuración de impresión
    has_print_service: bool = False
    bn_included: Optional[int] = Field(None, ge=0, description="Impresiones B/N incluidas")
    bn_cost_per_excess: Optional[Decimal] = Field(None, ge=0, description="Costo por exceso B/N")
    color_included: Optional[int] = Field(None, ge=0, description="Impresiones Color incluidas")
    color_cost_per_excess: Optional[Decimal] = Field(None, ge=0, description="Costo por exceso Color")
    print_notes: Optional[str] = None
    
    @field_validator('bn_included', 'bn_cost_per_excess', 'color_included', 'color_cost_per_excess', mode='after')
    @classmethod
    def validate_print_config(cls, v, info: FieldValidationInfo):
        """Valida que si has_print_service es True, los campos de impresión no sean None"""
        if info.data.get('has_print_service'):
            if info.field_name in ['bn_included', 'bn_cost_per_excess']:
                if v is None:
                    raise ValueError(f"{info.field_name} es requerido cuando has_print_service es True")
        return v
    
    @field_validator('end_date', mode='after')
    @classmethod
    def validate_dates(cls, v, info: FieldValidationInfo):
        if v and 'start_date' in info.data:
            if v <= info.data['start_date']:
                raise ValueError("end_date debe ser posterior a start_date")
        return v


class RentCreate(RentBase):
    contract_status: ContractStatus = ContractStatus.PENDIENTE
    start_date: date  # Obligatorio al crear


class RentUpdate(BaseModel):
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    rent: Optional[Decimal] = Field(None, gt=0)
    contract_status: Optional[ContractStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_foreign: Optional[bool] = None
    
    # Configuración de impresión
    has_print_service: Optional[bool] = None
    bn_included: Optional[int] = Field(None, ge=0)
    bn_cost_per_excess: Optional[Decimal] = Field(None, ge=0)
    color_included: Optional[int] = Field(None, ge=0)
    color_cost_per_excess: Optional[Decimal] = Field(None, ge=0)
    print_notes: Optional[str] = None


class RentResponse(RentBase):
    rent_id: int
    contract_number: Optional[str]
    contract_status: ContractStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Aceptar Any para los objetos ORM
    client: Optional[Any] = None
    branch: Optional[Any] = None
    area: Optional[Any] = None
    equipment: Optional[Any] = None
    
    @model_serializer
    def serialize_model(self):
        """Serializador personalizado para convertir objetos ORM a diccionarios"""
        data = {
            'rent_id': self.rent_id,
            'client_id': self.client_id,
            'branch_id': self.branch_id,
            'area_id': self.area_id,
            'item_id': self.item_id,
            'rent': float(self.rent),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_foreign': self.is_foreign,
            'has_print_service': self.has_print_service,
            'bn_included': self.bn_included,
            'bn_cost_per_excess': float(self.bn_cost_per_excess) if self.bn_cost_per_excess else None,
            'color_included': self.color_included,
            'color_cost_per_excess': float(self.color_cost_per_excess) if self.color_cost_per_excess else None,
            'print_notes': self.print_notes,
            'contract_number': self.contract_number,
            'contract_status': self.contract_status,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        
        # Serializar relaciones
        if self.client:
            from client.schemas import ClientResponse
            data['client'] = ClientResponse.model_validate(self.client).model_dump()
        
        if self.branch:
            from client.schemas import BranchResponse
            data['branch'] = BranchResponse.model_validate(self.branch).model_dump()
        
        if self.area:
            from client.schemas import AreaResponse
            data['area'] = AreaResponse.model_validate(self.area).model_dump()
        
        if self.equipment:
            from equipment.schemas import EquipmentRead
            data['equipment'] = EquipmentRead.model_validate(self.equipment).model_dump()
        
        return data
    
    class Config:
        from_attributes = True


class RentFilter(BaseModel):
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    contract_status: Optional[ContractStatus] = None
    is_foreign: Optional[bool] = None
    is_active: Optional[bool] = True
    has_print_service: Optional[bool] = None