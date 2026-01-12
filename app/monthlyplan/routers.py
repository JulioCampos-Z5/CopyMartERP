from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from app.monthlyplan.schemas import (
    ServiceTypeCreate, ServiceTypeUpdate, ServiceTypeResponse,
    MonthlyPlanCreate, MonthlyPlanUpdate, MonthlyPlanResponse, MonthlyPlanListResponse
)
from app.monthlyplan.services import ServiceTypeService, MonthlyPlanService
from app.monthlyplan.models import AttendanceStatus

service_type_router = APIRouter(prefix="/service", tags=["Service Types"])

@service_type_router.post("/", response_model=ServiceTypeResponse, status_code=status.HTTP_201_CREATED)
def create_service_type(
    service_type: ServiceTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceTypeService.create_service_type(db, service_type)

@service_type_router.get("/", response_model=List[ServiceTypeResponse])
def get_service_types(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceTypeService.get_all_service_types(db, include_inactive)

@service_type_router.get("/{service_type_id}", response_model=ServiceTypeResponse)
def get_service_type(
    service_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceTypeService.get_service_type_by_id(db, service_type_id)

@service_type_router.put("/{service_type_id}", response_model=ServiceTypeResponse)
def update_service_type(
    service_type_id: int,
    service_type_update: ServiceTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceTypeService.update_service_type(db, service_type_id, service_type_update)

@service_type_router.delete("/{service_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_type(
    service_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ServiceTypeService.delete_service_type(db, service_type_id)
    return None

monthlyplan_router = APIRouter(prefix="/monthly-plans", tags=["Monthly Plans"])

@monthlyplan_router.post("/", response_model=MonthlyPlanResponse, status_code=status.HTTP_201_CREATED)
def create_monthly_plan(
    plan: MonthlyPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MonthlyPlanService.create_monthly_plan(db, plan, current_user.user_id)

@monthlyplan_router.get("/", response_model=List[MonthlyPlanListResponse])
def get_monthly_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    client_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    attendance_status: Optional[AttendanceStatus] = None,
    service_type_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MonthlyPlanService.get_all_monthly_plans(
        db,
        skip=skip,
        limit=limit,
        client_id=client_id,
        branch_id=branch_id,
        attendance_status=attendance_status,
        service_type_id=service_type_id,
        user_id=user_id
    )

@monthlyplan_router.get("/my-plans", response_model=List[MonthlyPlanListResponse])
def get_my_monthly_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MonthlyPlanService.get_all_monthly_plans(
        db,
        skip=skip,
        limit=limit,
        user_id=current_user.user_id
    )

@monthlyplan_router.get("/date-range", response_model=List[MonthlyPlanResponse])
def get_plans_by_date_range(
    start_date: datetime,
    end_date: datetime,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MonthlyPlanService.get_plans_by_date_range(db, start_date, end_date, user_id)

@monthlyplan_router.get("/{plan_id}", response_model=MonthlyPlanResponse)
def get_monthly_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MonthlyPlanService.get_monthly_plan_by_id(db, plan_id)

@monthlyplan_router.put("/{plan_id}", response_model=MonthlyPlanResponse)
def update_monthly_plan(
    plan_id: int,
    plan_update: MonthlyPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MonthlyPlanService.update_monthly_plan(db, plan_id, plan_update)

@monthlyplan_router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_monthly_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    MonthlyPlanService.delete_monthly_plan(db, plan_id)
    return None