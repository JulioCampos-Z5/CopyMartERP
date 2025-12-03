"""
Modelos de Autenticación
========================
Contiene el modelo de Usuario y los enums de roles.

Cambios realizados (Dic 2025):
- Actualizado para coincidir con la estructura de la BD
- Cambiado 'password' por 'hashed_password'
- Cambiado 'rol' por 'role' 
- Removido DepartmentEnum (no existe en la BD)
- Los roles disponibles son: ADMIN, GERENTE, EMPLEADO
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum
from app.core.database import Base
from datetime import datetime
import enum


class RolEnum(str, enum.Enum):
    """
    Enum de roles de usuario.
    
    - ADMIN: Acceso total al sistema
    - GERENTE: Acceso a gestión y reportes
    - EMPLEADO: Acceso básico a operaciones
    """
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    EMPLEADO = "EMPLEADO"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(RolEnum), nullable=False, default=RolEnum.EMPLEADO)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)