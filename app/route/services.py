from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from route.models import Route
from route.schemas import RouteCreate, RouteUpdate


class RouteService:

    @staticmethod
    def get_routes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None,
        scheduled_date: Optional[date] = None,
        is_active: bool = True
    ) -> List[Route]:
        query = db.query(Route).filter(Route.is_active == is_active)

        if status_filter:
            query = query.filter(Route.status == status_filter)
        if scheduled_date:
            query = query.filter(Route.scheduled_date == scheduled_date)

        return query.order_by(Route.scheduled_date.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_route(db: Session, route_id: int) -> Route:
        route = db.query(Route).filter(Route.route_id == route_id).first()
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ruta no encontrada")
        return route

    @staticmethod
    def create_route(db: Session, route_data: RouteCreate) -> Route:
        existing = db.query(Route).filter(Route.route_code == route_data.route_code).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe una ruta con ese código")

        route = Route(**route_data.model_dump())
        db.add(route)
        db.commit()
        db.refresh(route)
        return route

    @staticmethod
    def update_route(db: Session, route_id: int, route_data: RouteUpdate) -> Route:
        route = RouteService.get_route(db, route_id)
        update_data = route_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(route, key, value)
        db.commit()
        db.refresh(route)
        return route

    @staticmethod
    def delete_route(db: Session, route_id: int) -> Route:
        route = RouteService.get_route(db, route_id)
        route.is_active = False
        db.commit()
        db.refresh(route)
        return route
