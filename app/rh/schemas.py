from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime, date
from typing import Optional
from enum import Enum


class AdministrativeTypeEnum(str, Enum):
    RETROALIMENTACION_ESCRITA = "retroalimentacion_escrita"
    AMONESTACION = "amonestacion"
    ACTA_ADMINISTRATIVA = "acta_administrativa"
    ENTREVISTA_AUSENTISMO = "entrevista_ausentismo"


class AbsenceTypeEnum(str, Enum):
    ENFERMEDAD = "enfermedad"
    AUSENTISMO = "ausentismo"
    PERMISO_PERSONAL = "permiso_personal"
    OTRO = "otro"


class StatusEnum(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    ACTIVO = "activo"
    PAGADO = "pagado"


class EmployeeBase(BaseModel):
    nss: str = Field(..., min_length=11, max_length=11)
    rfc: str = Field(..., min_length=12, max_length=13)
    curp: str = Field(..., min_length=18, max_length=18)
    birthday: date
    hire_date: date
    phone_emergency: str = Field(..., max_length=15)
    contact_emergency: str = Field(..., max_length=255)


class EmployeeCreate(EmployeeBase):
    user_id: int
    
    @validator('nss')
    def validate_nss(cls, v):
        if not v.isdigit():
            raise ValueError('NSS debe contener solo números')
        return v
    
    @validator('rfc')
    def validate_rfc(cls, v):
        return v.upper()
    
    @validator('curp')
    def validate_curp(cls, v):
        return v.upper()


class EmployeeUpdate(BaseModel):
    nss: Optional[str] = None
    rfc: Optional[str] = None
    curp: Optional[str] = None
    birthday: Optional[date] = None
    hire_date: Optional[date] = None
    phone_emergency: Optional[str] = None
    contact_emergency: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeResponse(EmployeeBase):
    employee_id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PayrollBase(BaseModel):
    salary: float = Field(..., gt=0)
    pay_day: date
    bonus: float = Field(default=0.00, ge=0)
    commission: float = Field(default=0.00, ge=0)


class PayrollCreate(PayrollBase):
    employee_id: int
    
    @validator('salary', 'bonus', 'commission')
    def round_to_two_decimals(cls, v):
        return round(v, 2)


class PayrollUpdate(BaseModel):
    salary: Optional[float] = None
    pay_day: Optional[date] = None
    bonus: Optional[float] = None
    commission: Optional[float] = None
    status: Optional[StatusEnum] = None


class PayrollResponse(PayrollBase):
    payroll_id: int
    employee_id: int
    total_pay: float
    status: StatusEnum
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VacationBase(BaseModel):
    vacation_days: int = Field(..., gt=0)
    start_date: date
    end_date: date
    notes: Optional[str] = None
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date debe ser posterior a start_date')
        return v


class VacationCreate(VacationBase):
    employee_id: int
    requested_by: int


class VacationUpdate(BaseModel):
    vacation_days: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[StatusEnum] = None
    notes: Optional[str] = None


class VacationResponse(VacationBase):
    vacation_id: int
    employee_id: int
    requested_by: int
    status: StatusEnum
    remaining_days: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AdministrativeRecordBase(BaseModel):
    type_administrative: AdministrativeTypeEnum
    suspended_days: int = Field(default=0, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: str
    file_path: Optional[str] = None


class AdministrativeRecordCreate(AdministrativeRecordBase):
    employee_id: int
    issued_by: int


class AdministrativeRecordUpdate(BaseModel):
    type_administrative: Optional[AdministrativeTypeEnum] = None
    suspended_days: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    file_path: Optional[str] = None


class AdministrativeRecordResponse(AdministrativeRecordBase):
    record_id: int
    employee_id: int
    issued_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AbsenceBase(BaseModel):
    absence_type: AbsenceTypeEnum
    start_date: date
    end_date: date
    is_justified: bool = False
    justification: Optional[str] = None
    file_path: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date debe ser posterior a start_date')
        return v


class AbsenceCreate(AbsenceBase):
    employee_id: int


class AbsenceUpdate(BaseModel):
    absence_type: Optional[AbsenceTypeEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_justified: Optional[bool] = None
    justification: Optional[str] = None
    file_path: Optional[str] = None
    status: Optional[StatusEnum] = None
    notes: Optional[str] = None
    reviewed_by: Optional[int] = None


class AbsenceResponse(AbsenceBase):
    absence_id: int
    employee_id: int
    status: StatusEnum
    reviewed_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True