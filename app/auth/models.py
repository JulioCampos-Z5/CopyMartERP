from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum
from app.core.database import Base
from datetime import datetime
import enum


class RolEnum(str, enum.Enum):
    ADMINISTRADOR = "administrador"
    GERENCIA = "gerencia"
    USUARIO = "usuario"

class DepartmentEnum(str, enum.Enum):
    RH = "rh"
    ADMINISTRACION = "administracion" #Credito cobranza, almacen 
    COMERCIAL = "comercial" #VENTAS Y ATENCION A CLIENTES RENTAS #sOPORTE
    OPERACIONES = "operaciones" #lO QUE ES DE DON PACO 

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    rol = Column(SQLEnum(RolEnum), nullable=False, default=RolEnum.USUARIO)
    department = Column(SQLEnum(DepartmentEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime,default= datetime.utcnow)