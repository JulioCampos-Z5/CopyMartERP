from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from route.schemas import RouteCreate, RouteUpdate, RouteResponse
from route.services import RouteService

router = APIRouter(prefix="/routes", tags=["Routes"])


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
    return RouteService.get_routes(db, skip, limit, status, scheduled_date, is_active)


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RouteService.get_route(db, route_id)


@router.post("/", response_model=RouteResponse)
def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RouteService.create_route(db, route_data)


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    route_data: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RouteService.update_route(db, route_id, route_data)


@router.delete("/{route_id}", response_model=RouteResponse)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RouteService.delete_route(db, route_id)
