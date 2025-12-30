from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    rol = Column(String(100), nullable=True)
    is_client = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="contact")

