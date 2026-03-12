from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from route.models import Route, RouteStop
from route.schemas import RouteCreate, RouteUpdate, RouteStopCreate, RouteStopUpdate


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
        query = db.query(Route).options(
            joinedload(Route.stops).joinedload(RouteStop.client),
            joinedload(Route.stops).joinedload(RouteStop.branch)
        ).filter(Route.is_active == is_active)

        if status_filter:
            query = query.filter(Route.status == status_filter)
        if scheduled_date:
            query = query.filter(Route.scheduled_date == scheduled_date)

        return query.order_by(Route.scheduled_date.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_route(db: Session, route_id: int) -> Route:
        route = db.query(Route).options(
            joinedload(Route.stops).joinedload(RouteStop.client),
            joinedload(Route.stops).joinedload(RouteStop.branch)
        ).filter(Route.route_id == route_id).first()
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

    # ---- RouteStop methods ----

    @staticmethod
    def get_stops(db: Session, route_id: int) -> List[RouteStop]:
        RouteService.get_route(db, route_id)  # validates route exists
        return db.query(RouteStop).options(
            joinedload(RouteStop.client),
            joinedload(RouteStop.branch)
        ).filter(RouteStop.route_id == route_id).order_by(RouteStop.stop_order).all()

    @staticmethod
    def add_stop(db: Session, route_id: int, stop_data: RouteStopCreate) -> RouteStop:
        route = RouteService.get_route(db, route_id)
        stop = RouteStop(route_id=route_id, **stop_data.model_dump())
        db.add(stop)
        route.total_stops = len(route.stops) + 1
        db.commit()
        db.refresh(stop)
        return stop

    @staticmethod
    def update_stop(db: Session, stop_id: int, stop_data: RouteStopUpdate) -> RouteStop:
        stop = db.query(RouteStop).filter(RouteStop.stop_id == stop_id).first()
        if not stop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parada no encontrada")
        update_data = stop_data.model_dump(exclude_unset=True)

        # If marking as completed, update route completed_stops
        if "is_completed" in update_data and update_data["is_completed"] and not stop.is_completed:
            route = db.query(Route).filter(Route.route_id == stop.route_id).first()
            if route:
                route.completed_stops = (route.completed_stops or 0) + 1

        for key, value in update_data.items():
            setattr(stop, key, value)
        db.commit()
        db.refresh(stop)
        return stop

    @staticmethod
    def delete_stop(db: Session, stop_id: int) -> None:
        stop = db.query(RouteStop).filter(RouteStop.stop_id == stop_id).first()
        if not stop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parada no encontrada")
        route = db.query(Route).filter(Route.route_id == stop.route_id).first()
        db.delete(stop)
        if route:
            route.total_stops = max(0, (route.total_stops or 1) - 1)
            if stop.is_completed:
                route.completed_stops = max(0, (route.completed_stops or 1) - 1)
        db.commit()
