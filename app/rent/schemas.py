from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from rent.models import ContractStatus


class RentBase(BaseModel):
    client_id: int = Field(..., gt=0)
    branch_id: Optional[int] = Field(None, gt=0)
    area_id: Optional[int] = Field(None, gt=0)
    item_id: int = Field(..., gt=0)
    rent: Decimal = Field(..., gt=0, description="Renta mensual base")
    start_date: date
    end_date: Optional[date] = None
    is_foreign: bool = False
    
    # Configuración de impresión
    has_print_service: bool = False
    bn_included: Optional[int] = Field(None, ge=0, description="Impresiones B/N incluidas")
    bn_cost_per_excess: Optional[Decimal] = Field(None, ge=0, description="Costo por exceso B/N")
    color_included: Optional[int] = Field(None, ge=0, description="Impresiones Color incluidas")
    color_cost_per_excess: Optional[Decimal] = Field(None, ge=0, description="Costo por exceso Color")
    print_notes: Optional[str] = None
    
    @validator('bn_included', 'bn_cost_per_excess', 'color_included', 'color_cost_per_excess')
    def validate_print_config(cls, v, values, field):
        """Valida que si has_print_service es True, los campos de impresión no sean None"""
        if values.get('has_print_service'):
            if field.name in ['bn_included', 'bn_cost_per_excess']:
                if v is None:
                    raise ValueError(f"{field.name} es requerido cuando has_print_service es True")
        return v
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if v and 'start_date' in values:
            if v <= values['start_date']:
                raise ValueError("end_date debe ser posterior a start_date")
        return v


class RentCreate(RentBase):
    contract_status: ContractStatus = ContractStatus.PENDIENTE


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
    
    client: Optional[dict] = None
    branch: Optional[dict] = None
    area: Optional[dict] = None
    equipment: Optional[dict] = None
    
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