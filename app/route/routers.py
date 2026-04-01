from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from route.schemas import RouteCreate, RouteUpdate, RouteResponse, RouteStopCreate, RouteStopUpdate, RouteStopResponse
from route.services import RouteService

router = APIRouter(prefix="/routes", tags=["Routes"])


def _serialize_stop(stop) -> dict:
    """Serializa una parada incluyendo nombres de cliente y sucursal."""
    return {
        "stop_id": stop.stop_id,
        "route_id": stop.route_id,
        "client_id": stop.client_id,
        "branch_id": stop.branch_id,
        "client_name": stop.client.name if stop.client else None,
        "branch_name": stop.branch.name if stop.branch else None,
        "stop_order": stop.stop_order,
        "address": stop.address,
        "city": stop.city,
        "notes": stop.notes,
        "is_completed": stop.is_completed,
        "visit_status": stop.visit_status,
        "no_visit_reason": stop.no_visit_reason,
        "created_at": stop.created_at
    }


def _serialize_route(route) -> dict:
    """Serializa una ruta incluyendo sus paradas con nombres."""
    data = {
        "route_id": route.route_id,
        "route_code": route.route_code,
        "driver_name": route.driver_name,
        "vehicle": route.vehicle,
        "status": route.status,
        "scheduled_date": route.scheduled_date,
        "total_stops": route.total_stops,
        "completed_stops": route.completed_stops,
        "notes": route.notes,
        "is_active": route.is_active,
        "created_at": route.created_at,
        "updated_at": route.updated_at,
        "stops": [_serialize_stop(s) for s in (route.stops or [])]
    }
    return data


@router.get("/", response_model=List[RouteResponse])
def get_routes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
    scheduled_date: Optional[date] = None,
    is_active: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    routes = RouteService.get_routes(db, skip, limit, status, scheduled_date, is_active)
    return [_serialize_route(r) for r in routes]


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = RouteService.get_route(db, route_id)
    return _serialize_route(route)


@router.post("/", response_model=RouteResponse)
def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = RouteService.create_route(db, route_data)
    return _serialize_route(route)


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    route_data: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = RouteService.update_route(db, route_id, route_data)
    return _serialize_route(route)


@router.delete("/{route_id}", response_model=RouteResponse)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = RouteService.delete_route(db, route_id)
    return _serialize_route(route)


# ---- RouteStop endpoints ----

@router.get("/{route_id}/stops", response_model=List[RouteStopResponse])
def get_stops(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stops = RouteService.get_stops(db, route_id)
    return [_serialize_stop(s) for s in stops]


@router.post("/{route_id}/stops", response_model=RouteStopResponse)
def add_stop(
    route_id: int,
    stop_data: RouteStopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stop = RouteService.add_stop(db, route_id, stop_data)
    # Reload to get relationships
    from sqlalchemy.orm import joinedload
    from route.models import RouteStop
    stop = db.query(RouteStop).options(
        joinedload(RouteStop.client), joinedload(RouteStop.branch)
    ).filter(RouteStop.stop_id == stop.stop_id).first()
    return _serialize_stop(stop)


@router.put("/stops/{stop_id}", response_model=RouteStopResponse)
def update_stop(
    stop_id: int,
    stop_data: RouteStopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stop = RouteService.update_stop(db, stop_id, stop_data)
    from sqlalchemy.orm import joinedload
    from route.models import RouteStop
    stop = db.query(RouteStop).options(
        joinedload(RouteStop.client), joinedload(RouteStop.branch)
    ).filter(RouteStop.stop_id == stop.stop_id).first()
    return _serialize_stop(stop)


@router.delete("/stops/{stop_id}", status_code=204)
def delete_stop(
    stop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    RouteService.delete_stop(db, stop_id)
