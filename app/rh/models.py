from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Numeric, Date, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, date
import enum


class AdministrativeTypeEnum(str, enum.Enum):
    RETROALIMENTACION_ESCRITA = "retroalimentacion_escrita"
    AMONESTACION = "amonestacion"
    ACTA_ADMINISTRATIVA = "acta_administrativa"
    ENTREVISTA_AUSENTISMO = "entrevista_ausentismo"


class AbsenceTypeEnum(str, enum.Enum):
    ENFERMEDAD = "enfermedad"
    AUSENTISMO = "ausentismo"
    PERMISO_PERSONAL = "permiso_personal"
    OTRO = "otro"


class StatusEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    ACTIVO = "activo"
    PAGADO = "pagado"


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    nss = Column(String(11), unique=True, nullable=False, index=True) 
    rfc = Column(String(13), unique=True, nullable=False, index=True)  
    curp = Column(String(18), unique=True, nullable=False, index=True) 
    birthday = Column(Date, nullable=False)
    hire_date = Column(Date, nullable=False, default=date.today)
    phone_emergency = Column(String(15), nullable=False)
    contact_emergency = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacion
    payrolls = relationship("Payroll", back_populates="employee", cascade="all, delete-orphan")
    vacations = relationship("Vacation", back_populates="employee", cascade="all, delete-orphan")
    administrative_records = relationship("AdministrativeRecord", back_populates="employee", cascade="all, delete-orphan")
    absences = relationship("Absence", back_populates="employee", cascade="all, delete-orphan")


class Payroll(Base):
    __tablename__ = "payrolls"

    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)  # Salario base
    pay_day = Column(Date, nullable=False)  # Día de pago
    bonus = Column(Numeric(10, 2), default=0.00)  # Bonos
    commission = Column(Numeric(10, 2), default=0.00)  # Comisiones
    total_pay = Column(Numeric(10, 2), nullable=False)  # Pago total
    status = Column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.PENDIENTE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacion
    employee = relationship("Employee", back_populates="payrolls")


class Vacation(Base):
    __tablename__ = "vacations"

    vacation_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    vacation_days = Column(Integer, nullable=False)  # Días solicitados
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    requested_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Quién solicitó
    
    status = Column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.PENDIENTE)
    remaining_days = Column(Integer, nullable=False)  # Días que quedan 
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacion
    employee = relationship("Employee", back_populates="vacations")


class AdministrativeRecord(Base):
    __tablename__ = "administrative_records"

    record_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    type_administrative = Column(SQLEnum(AdministrativeTypeEnum), nullable=False)
    suspended_days = Column(Integer, default=0)  # Días suspendidos
    start_date = Column(Date, nullable=True)  # Fecha inicio de suspensión
    end_date = Column(Date, nullable=True)  # Fecha fin de suspensión
    file_path = Column(String(500), nullable=True)  # Ruta del archivo
    description = Column(Text, nullable=False)  # Descripción del incidente
    issued_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Quién emitió el registro
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacion
    employee = relationship("Employee", back_populates="administrative_records")


class Absence(Base):
    __tablename__ = "absences"

    absence_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    absence_type = Column(SQLEnum(AbsenceTypeEnum), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_justified = Column(Boolean, default=False)  # Si tiene justificante
    justification = Column(Text, nullable=True)  # Descripción del justificante
    file_path = Column(String(500), nullable=True)  # Archivo del justificante
    status = Column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.PENDIENTE)
    notes = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)  # Quién revisó
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    employee = relationship("Employee", back_populates="absences")