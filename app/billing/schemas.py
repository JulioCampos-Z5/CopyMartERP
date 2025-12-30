from pydantic import BaseModel, Field, field_validator, FieldValidationInfo
from datetime import datetime, date
from typing import Optional
from enum import Enum
from decimal import Decimal


class BillingStatus(str, Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    VENCIDO = "vencido"


class BillingType(str, Enum):
    RENTA = "renta"
    VENTA = "venta"


# Schemas para las relaciones
class ClientBasic(BaseModel):
    client_id: int
    name: str
    comercial_name: Optional[str] = None

    model_config = {"from_attributes": True}


class BranchBasic(BaseModel):
    branch_id: int
    name: str

    model_config = {"from_attributes": True}


class AreaBasic(BaseModel):
    area_id: int
    name: str

    model_config = {"from_attributes": True}


class RentBasic(BaseModel):
    rent_id: int
    contract_number: Optional[str] = None
    rent: Decimal

    model_config = {"from_attributes": True}


class SaleBasic(BaseModel):
    sale_id: int
    invoice_number: Optional[str] = None
    sale_price: Decimal

    model_config = {"from_attributes": True}


# Schema de creación
class BillingCreate(BaseModel):
    billing_type: BillingType
    rent_id: Optional[int] = None
    sale_id: Optional[int] = None
    target_date: date
    due_date: date
    payment_term: Optional[int] = Field(None, ge=0, description="Días de crédito")
    payment_day: Optional[int] = Field(None, ge=1, le=31, description="Día del mes para pago")
    follow_up: bool = False
    comment: Optional[str] = None

    # --- VALIDACIÓN DE rent_id / sale_id ---
    @field_validator("rent_id", mode="after")
    def validate_rent_id(cls, v, info: FieldValidationInfo):
        if info.data.get("billing_type") == BillingType.RENTA and not v:
            raise ValueError("rent_id es requerido para facturación de renta")
        return v

    @field_validator("sale_id", mode="after")
    def validate_sale_id(cls, v, info: FieldValidationInfo):
        if info.data.get("billing_type") == BillingType.VENTA and not v:
            raise ValueError("sale_id es requerido para facturación de venta")
        return v

    # --- VALIDAR due_date >= target_date ---
    @field_validator("due_date", mode="after")
    def validate_due_date(cls, v, info: FieldValidationInfo):
        target_date = info.data.get("target_date")
        if target_date and v < target_date:
            raise ValueError("due_date no puede ser anterior a target_date")
        return v


# Schema de actualización
class BillingUpdate(BaseModel):
    target_date: Optional[date] = None
    due_date: Optional[date] = None
    payment_date: Optional[date] = None
    status: Optional[BillingStatus] = None
    follow_up: Optional[bool] = None
    payment_term: Optional[int] = Field(None, ge=0)
    payment_day: Optional[int] = Field(None, ge=1, le=31)
    comment: Optional[str] = None
    is_active: Optional[bool] = None


# Schema para marcar como pagado
class BillingPayment(BaseModel):
    payment_date: date = Field(default_factory=date.today)
    comment: Optional[str] = None


# Schema de respuesta
class BillingResponse(BaseModel):
    billing_id: int
    billing_type: BillingType
    rent_id: Optional[int] = None
    sale_id: Optional[int] = None
    client_id: int
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    invoice_number: Optional[str] = None
    amount: Decimal
    target_date: date
    due_date: date
    payment_date: Optional[date] = None
    status: BillingStatus
    follow_up: bool
    payment_term: Optional[int] = None
    payment_day: Optional[int] = None
    comment: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    client: ClientBasic
    branch: Optional[BranchBasic] = None
    area: Optional[AreaBasic] = None
    rent: Optional[RentBasic] = None
    sale: Optional[SaleBasic] = None

    model_config = {"from_attributes": True}


class BillingList(BaseModel):
    billing_id: int
    billing_type: BillingType
    invoice_number: Optional[str] = None
    client_name: str
    branch_name: Optional[str] = None
    amount: Decimal
    target_date: date
    due_date: date
    status: BillingStatus
    follow_up: bool
    days_until_due: Optional[int] = None

    model_config = {"from_attributes": True}


class BillingFilter(BaseModel):
    billing_type: Optional[BillingType] = None
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    status: Optional[BillingStatus] = None
    follow_up: Optional[bool] = None
    is_active: Optional[bool] = True
    date_from: Optional[date] = None
    date_to: Optional[date] = None


class BillingBatchCreate(BaseModel):
    target_date: date
    due_date: date
    payment_term: Optional[int] = Field(None, ge=0)
    payment_day: Optional[int] = Field(None, ge=1, le=31)
    client_ids: Optional[list[int]] = None
    comment: Optional[str] = None

    @field_validator("due_date", mode="after")
    def validate_due_date(cls, v, info: FieldValidationInfo):
        target_date = info.data.get("target_date")
        if target_date and v < target_date:
            raise ValueError("due_date no puede ser anterior a target_date")
        return v


class BillingStats(BaseModel):
    total_billings: int
    total_amount: Decimal
    by_status: dict[str, int]
    by_type: dict[str, int]
    pending_amount: Decimal
    overdue_amount: Decimal
    paid_amount: Decimal