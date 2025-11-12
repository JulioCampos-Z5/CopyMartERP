from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.auth.models import User

class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rfc = Column(String, nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)  
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    branches = relationship("Branch", back_populates="client")
    contact = relationship("Contact", back_populates="client", uselist=False)
    creator = relationship("User")


class Branch(Base):
    __tablename__ = "branches"
    branch_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    colonia = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="branches")
    areas = relationship("Area", back_populates="branch")


class Area(Base):
    __tablename__ = "areas"
    area_id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    branch = relationship("Branch", back_populates="areas")


class Contact(Base):
    __tablename__ = "contacts"
    contact_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    rol = Column(String, nullable=True)
    is_client = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="contact")