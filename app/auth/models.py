"""
Modelos de Autenticación
========================
Contiene el modelo de Usuario y los enums de roles y departamentos.

Sincronizado con la estructura real de la base de datos MariaDB.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum
from app.core.database import Base
from datetime import datetime
import enum


class RolEnum(str, enum.Enum):
    """
    Enum de roles de usuario (coincide con BD).
    """
    ADMINISTRADOR = "ADMINISTRADOR"
    GERENCIA = "GERENCIA"
    USUARIO = "USUARIO"


class DepartmentEnum(str, enum.Enum):
    """
    Enum de departamentos (coincide con BD).
    """
    RH = "RH"
    ADMINISTRACION = "ADMINISTRACION"
    COMERCIAL = "COMERCIAL"
    OPERACIONES = "OPERACIONES"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    rol = Column(SQLEnum(RolEnum), nullable=False, default=RolEnum.USUARIO)
    department = Column(SQLEnum(DepartmentEnum), nullable=False, default=DepartmentEnum.ADMINISTRACION)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)