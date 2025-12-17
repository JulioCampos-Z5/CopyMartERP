from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from auth.models import User

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    comercial_name = Column(String(255), nullable=True)
    rfc = Column(String(50), nullable=True)
    address = Column(String(500), nullable=True)
    colonia = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    branches = relationship("Branch", back_populates="client", cascade="all, delete-orphan")
    contact = relationship("Contact", back_populates="client", uselist=False)
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

