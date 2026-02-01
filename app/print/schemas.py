from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class PrintCounterBase(BaseModel):
    period_month: int = Field(..., ge=1, le=12, description="Mes del período (1-12)")
    period_year: int = Field(..., ge=2020, description="Año del período")
    
    bn_current: int = Field(0, ge=0, description="Contador actual B/N")
    color_current: int = Field(0, ge=0, description="Contador actual Color")
    
    counter_photo_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=500)
    reading_date: date = Field(default_factory=date.today)


class PrintCounterCreate(PrintCounterBase):
    rent_id: int = Field(..., gt=0)
    
    @field_validator('period_year', mode='after')
    @classmethod
    def validate_period(cls, v, info):
        from pydantic_core.core_schema import FieldValidationInfo
        if hasattr(info, 'data') and 'period_month' in info.data:
            # Validar que el período no sea futuro
            current_date = date.today()
            period_date = date(v, info.data['period_month'], 1)
            if period_date > current_date:
                raise ValueError("El período no puede ser futuro")
        return v


class PrintCounterUpdate(BaseModel):
    bn_current: Optional[int] = Field(None, ge=0)
    color_current: Optional[int] = Field(None, ge=0)
    counter_photo_url: Optional[str] = None
    notes: Optional[str] = None
    reading_date: Optional[date] = None


class PrintCounterResponse(PrintCounterBase):
    counter_id: int
    rent_id: int
    billing_id: Optional[int]
    
    bn_previous: int
    bn_printed: int
    bn_included: int
    bn_excess: int
    bn_cost_per_page: Decimal
    bn_excess_amount: Decimal
    
    color_previous: int
    color_printed: int
    color_included: int
    color_excess: int
    color_cost_per_page: Decimal
    color_excess_amount: Decimal
    
    total_excess_amount: Decimal
    is_billed: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PrintCounterFilter(BaseModel):
    rent_id: Optional[int] = None
    client_id: Optional[int] = None
    period_month: Optional[int] = Field(None, ge=1, le=12)
    period_year: Optional[int] = Field(None, ge=2020)
    is_billed: Optional[bool] = None
    is_active: Optional[bool] = True


class PrintCounterBatchCreate(BaseModel):
    period_month: int = Field(..., ge=1, le=12)
    period_year: int = Field(..., ge=2020)
    rent_ids: Optional[list[int]] = Field(None, description="IDs de rentas específicas (opcional)")
    client_ids: Optional[list[int]] = Field(None, description="IDs de clientes (opcional)")
    reading_date: date = Field(default_factory=date.today)


class PrintCounterStats(BaseModel):
    total_counters: int
    total_bn_printed: int
    total_color_printed: int
    total_bn_excess: int
    total_color_excess: int
    total_excess_amount: Decimal
    billed_amount: Decimal
    pending_amount: Decimal