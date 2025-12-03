"""
Modelo de Cliente (Client)
==========================
Este modelo representa a los clientes del sistema CopyMart ERP.

Cambios realizados (Dic 2025):
- Agregados campos: email, phone, website, industry, updated_at para coincidir con la BD
- Cambiado 'contact' (singular) a 'contacts' (plural) en la relación
- Removido ForeignKey de contact_id para evitar dependencia circular
- El contacto principal se referencia mediante contact_id pero los contactos
  se almacenan en la tabla 'contacts' con referencia al client_id
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.auth.models import User

class Client(Base):
    """
    Modelo de Cliente.
    
    Atributos principales:
    - name: Nombre legal/razón social (requerido)
    - comercial_name: Nombre comercial
    - rfc: Registro Federal de Contribuyentes
    - contact_id: Referencia al contacto principal (sin FK para evitar circular)
    - user_id: Usuario que creó el cliente
    
    Relaciones:
    - branches: Sucursales del cliente (one-to-many)
    - contacts: Contactos asociados al cliente (one-to-many)
    - creator: Usuario que creó el registro
    """
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    comercial_name = Column(String(255), nullable=True)
    rfc = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    colonia = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    contact_id = Column(Integer, nullable=True)  # Referencia simple sin FK para evitar circular
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    branches = relationship("Branch", back_populates="client", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="client", foreign_keys="Contact.client_id")
    creator = relationship("User")


class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    is_main = Column(Boolean, default=False)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    colonia = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="branches")
    areas = relationship("Area", back_populates="branch", cascade="all, delete-orphan")


class Area(Base):
    __tablename__ = "areas"

    area_id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    branch = relationship("Branch", back_populates="areas")