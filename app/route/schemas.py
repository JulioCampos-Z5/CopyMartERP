from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from enum import Enum


class RouteStatus(str, Enum):
    PROGRAMADA = "programada"
    EN_RUTA = "en_ruta"
    PAUSADA = "pausada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class RouteCreate(BaseModel):
    route_code: str
    driver_name: str
    vehicle: Optional[str] = None
    status: RouteStatus = RouteStatus.PROGRAMADA
    scheduled_date: date
    total_stops: int = 0
    completed_stops: int = 0
    notes: Optional[str] = None


class RouteUpdate(BaseModel):
    driver_name: Optional[str] = None
    vehicle: Optional[str] = None
    status: Optional[RouteStatus] = None
    scheduled_date: Optional[date] = None
    total_stops: Optional[int] = None
    completed_stops: Optional[int] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class RouteResponse(BaseModel):
    route_id: int
    route_code: str
    driver_name: str
    vehicle: Optional[str] = None
    status: str
    scheduled_date: date
    total_stops: int
    completed_stops: int
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
