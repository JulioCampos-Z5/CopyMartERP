"""
Modelo de Contacto (Contact)
============================
Este modelo representa los contactos asociados a clientes, sucursales o áreas.

Cambios realizados (Dic 2025):
- Actualizado para coincidir con la estructura de la BD existente
- client_id es obligatorio (cada contacto pertenece a un cliente)
- branch_id y area_id son opcionales para mayor granularidad
- Cambiado 'rol' por 'position' para coincidir con la BD
- Agregado 'is_primary' para indicar contacto principal
- Corregido back_populates de 'contact' a 'contacts' (plural)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Contact(Base):
    """
    Modelo de Contacto.
    
    Atributos principales:
    - client_id: Cliente al que pertenece (requerido)
    - branch_id: Sucursal específica (opcional)
    - area_id: Área específica (opcional)
    - name: Nombre del contacto
    - position: Cargo/puesto del contacto
    - is_primary: Indica si es el contacto principal del cliente
    
    Relaciones:
    - client: Cliente al que pertenece
    - branch: Sucursal (opcional)
    - area: Área (opcional)
    """
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=True)
    name = Column(String(255), nullable=False)
    position = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="contacts", foreign_keys=[client_id])
    branch = relationship("Branch")
    area = relationship("Area")
