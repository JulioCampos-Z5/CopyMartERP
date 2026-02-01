from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from monthlyplan.models import MonthlyPlan, ServiceType, AttendanceStatus
from monthlyplan.schemas import (
    MonthlyPlanCreate, MonthlyPlanUpdate,
    ServiceTypeCreate, ServiceTypeUpdate
)
from auth.models import User
from datetime import datetime


class ServiceTypeService:
    
    @staticmethod
    def create_service_type(db: Session, service_type_data: ServiceTypeCreate) -> ServiceType:
        existing = db.query(ServiceType).filter(
            ServiceType.name == service_type_data.name
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service type with this name already exists"
            )
        
        service_type = ServiceType(**service_type_data.model_dump())
        db.add(service_type)
        db.commit()
        db.refresh(service_type)
        return service_type
    
    @staticmethod
    def get_all_service_types(db: Session, include_inactive: bool = False):
        query = db.query(ServiceType)
        if not include_inactive:
            query = query.filter(ServiceType.is_active == 1)
        return query.order_by(ServiceType.name).all()
    
    @staticmethod
    def get_service_type_by_id(db: Session, service_type_id: int) -> ServiceType:
        service_type = db.query(ServiceType).filter(
            ServiceType.service_type_id == service_type_id
        ).first()
        if not service_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service type not found"
            )
        return service_type
    
    @staticmethod
    def update_service_type(
        db: Session,
        service_type_id: int,
        service_type_data: ServiceTypeUpdate
    ) -> ServiceType:
        service_type = ServiceTypeService.get_service_type_by_id(db, service_type_id)
        
        update_data = service_type_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service_type, field, value)
        
        db.commit()
        db.refresh(service_type)
        return service_type
    
    @staticmethod
    def delete_service_type(db: Session, service_type_id: int) -> bool:
        service_type = ServiceTypeService.get_service_type_by_id(db, service_type_id)
        service_type.is_active = 0
        db.commit()
        return True

class MonthlyPlanService:
    
    @staticmethod
    def create_monthly_plan(
        db: Session,
        plan_data: MonthlyPlanCreate,
        user_id: int
    ) -> MonthlyPlan:
        assigned_user_ids = plan_data.assigned_user_ids
        plan_dict = plan_data.model_dump(exclude={'assigned_user_ids'})
        
        plan = MonthlyPlan(
            **plan_dict,
            created_by=user_id
        )
        
        #asigna usuario
        if assigned_user_ids:
            users = db.query(User).filter(User.user_id.in_(assigned_user_ids)).all()
            if len(users) != len(assigned_user_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more user IDs are invalid"
                )
            plan.assigned_users = users
        
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    
    @staticmethod
    def get_monthly_plan_by_id(db: Session, plan_id: int) -> MonthlyPlan:
        plan = db.query(MonthlyPlan).filter(
            MonthlyPlan.monthlyplan_id == plan_id
        ).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Monthly plan not found"
            )
        return plan
    
    @staticmethod
    def get_all_monthly_plans(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        client_id: int = None,
        branch_id: int = None,
        attendance_status: AttendanceStatus = None,
        service_type_id: int = None,
        user_id: int = None
    ):
        query = db.query(MonthlyPlan)
        
        if client_id:
            query = query.filter(MonthlyPlan.client_id == client_id)
        if branch_id:
            query = query.filter(MonthlyPlan.branch_id == branch_id)
        if attendance_status:
            query = query.filter(MonthlyPlan.attendance_status == attendance_status)
        if service_type_id:
            query = query.filter(MonthlyPlan.service_type_id == service_type_id)
        if user_id:
            query = query.join(MonthlyPlan.assigned_users).filter(User.user_id == user_id)
        
        query = query.order_by(desc(MonthlyPlan.visit_date))
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_monthly_plan(
        db: Session,
        plan_id: int,
        plan_data: MonthlyPlanUpdate
    ) -> MonthlyPlan:
        plan = MonthlyPlanService.get_monthly_plan_by_id(db, plan_id)
        
        update_data = plan_data.model_dump(exclude_unset=True)
        
        assigned_user_ids = update_data.pop('assigned_user_ids', None)
        
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        if assigned_user_ids is not None:
            users = db.query(User).filter(User.user_id.in_(assigned_user_ids)).all()
            if len(users) != len(assigned_user_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more user IDs are invalid"
                )
            plan.assigned_users = users
        
        db.commit()
        db.refresh(plan)
        return plan
    
    @staticmethod
    def delete_monthly_plan(db: Session, plan_id: int) -> bool:
        plan = MonthlyPlanService.get_monthly_plan_by_id(db, plan_id)
        db.delete(plan)
        db.commit()
        return True
    
    @staticmethod
    def get_plans_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        user_id: int = None
    ):
        query = db.query(MonthlyPlan).filter(
            and_(
                MonthlyPlan.visit_date >= start_date,
                MonthlyPlan.visit_date <= end_date
            )
        )
        
        if user_id:
            query = query.join(MonthlyPlan.assigned_users).filter(User.user_id == user_id)
        
        return query.order_by(MonthlyPlan.visit_date).all()