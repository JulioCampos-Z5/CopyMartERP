from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Sparepart(Base):
    __tablename__ = "spareparts"
    
    sparepart_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    color = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    brand = Column(String(100), nullable=True)
    equipment = Column(String(255), nullable=True)
    code = Column(String(100), nullable=True, unique=True, index=True)
    supplier = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    