from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime


class PrintCounter(Base):
    __tablename__ = "print_counters"
    
    counter_id = Column(Integer, primary_key=True, index=True)
    rent_id = Column(Integer, ForeignKey("rents.rent_id"), nullable=False, index=True)
    billing_id = Column(Integer, ForeignKey("billings.billing_id"), nullable=True, index=True)
    
    period_month = Column(Integer, nullable=False, index=True)
    period_year = Column(Integer, nullable=False, index=True)
    
    # Contadores B/N
    bn_previous = Column(Integer, nullable=False, default=0)  
    bn_current = Column(Integer, nullable=False, default=0)  
    bn_printed = Column(Integer, nullable=False, default=0)   
    bn_included = Column(Integer, nullable=False, default=0)  
    bn_excess = Column(Integer, nullable=False, default=0)    
    bn_cost_per_page = Column(DECIMAL(10, 4), nullable=False, default=0.0)  # Costo por página B/N
    bn_excess_amount = Column(DECIMAL(10, 2), nullable=False, default=0.0)  # Monto por exceso B/N
    
    # Contadores Color
    color_previous = Column(Integer, nullable=False, default=0) 
    color_current = Column(Integer, nullable=False, default=0)   
    color_printed = Column(Integer, nullable=False, default=0)  
    color_included = Column(Integer, nullable=False, default=0) 
    color_excess = Column(Integer, nullable=False, default=0)   
    color_cost_per_page = Column(DECIMAL(10, 4), nullable=False, default=0.0)  # Costo por página Color
    color_excess_amount = Column(DECIMAL(10, 2), nullable=False, default=0.0)  # Monto por exceso Color
    
    # Total
    total_excess_amount = Column(DECIMAL(10, 2), nullable=False, default=0.0)  
    
    # Evidencia
    counter_photo_url = Column(String(500), nullable=True)  
    notes = Column(String(500), nullable=True)
    
    # Fechas de registro
    reading_date = Column(Date, nullable=False, default=datetime.utcnow)  # Fecha de lectura del contador
    
    # Control
    is_billed = Column(Boolean, default=False, index=True)  # Si ya fue facturado
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    
    # Relaciones
    rent = relationship("Rent", back_populates="print_counters")
    billing = relationship("Billing", back_populates="print_counter")
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<PrintCounter(id={self.counter_id}, rent={self.rent_id}, period={self.period_month}/{self.period_year})>"