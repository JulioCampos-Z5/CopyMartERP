from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class RouteStatus(str, Enum):
    PROGRAMADA = "programada"
    EN_RUTA = "en_ruta"
    PAUSADA = "pausada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


# ---- RouteStop schemas ----

class RouteStopCreate(BaseModel):
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    stop_order: int = 0
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None


class RouteStopUpdate(BaseModel):
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    stop_order: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class RouteStopResponse(BaseModel):
    stop_id: int
    route_id: int
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    client_name: Optional[str] = None
    branch_name: Optional[str] = None
    stop_order: int
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None
    is_completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- Route schemas ----

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
    stops: List[RouteStopResponse] = []

    model_config = {"from_attributes": True}
