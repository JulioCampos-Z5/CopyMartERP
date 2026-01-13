from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import date, timedelta
from . import models, schemas


class EmployeeService:
    
    @staticmethod
    def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
        try:
            db_employee = models.Employee(**employee.dict())
            db.add(db_employee)
            db.commit()
            db.refresh(db_employee)
            return db_employee
        except IntegrityError as e:
            db.rollback()
            if "nss" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="NSS ya existe en el sistema"
                )
            elif "rfc" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="RFC ya existe en el sistema"
                )
            elif "curp" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CURP ya existe en el sistema"
                )
            elif "user_id" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este usuario ya tiene un registro de empleado"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear empleado"
            )
    
    @staticmethod
    def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
        employee = db.query(models.Employee).filter(
            models.Employee.employee_id == employee_id
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        return employee
    
    @staticmethod
    def get_employee_by_user_id(db: Session, user_id: int) -> Optional[models.Employee]:
        return db.query(models.Employee).filter(
            models.Employee.user_id == user_id
        ).first()
    
    @staticmethod
    def get_employees(db: Session, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[models.Employee]:
        query = db.query(models.Employee)
        if is_active is not None:
            query = query.filter(models.Employee.is_active == is_active)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_employee(db: Session, employee_id: int, employee_update: schemas.EmployeeUpdate) -> models.Employee:
        db_employee = EmployeeService.get_employee(db, employee_id)
        
        update_data = employee_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        
        try:
            db.commit()
            db.refresh(db_employee)
            return db_employee
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar: datos duplicados"
            )
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        db_employee = EmployeeService.get_employee(db, employee_id)
        db.delete(db_employee)
        db.commit()
        return True


# ========== PAYROLL SERVICES ==========
class PayrollService:
    
    @staticmethod
    def calculate_total_pay(salary: float, bonus: float, commission: float) -> float:
        return round(salary + bonus + commission, 2)
    
    @staticmethod
    def create_payroll(db: Session, payroll: schemas.PayrollCreate) -> models.Payroll:
        # Verificar que el empleado existe
        employee = db.query(models.Employee).filter(
            models.Employee.employee_id == payroll.employee_id
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        total_pay = PayrollService.calculate_total_pay(
            payroll.salary, payroll.bonus, payroll.commission
        )
        
        db_payroll = models.Payroll(
            **payroll.dict(),
            total_pay=total_pay
        )
        db.add(db_payroll)
        db.commit()
        db.refresh(db_payroll)
        return db_payroll
    
    @staticmethod
    def get_payroll(db: Session, payroll_id: int) -> models.Payroll:
        payroll = db.query(models.Payroll).filter(
            models.Payroll.payroll_id == payroll_id
        ).first()
        if not payroll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nómina no encontrada"
            )
        return payroll
    
    @staticmethod
    def get_payrolls_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[models.Payroll]:
        return db.query(models.Payroll).filter(
            models.Payroll.employee_id == employee_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_payroll(db: Session, payroll_id: int, payroll_update: schemas.PayrollUpdate) -> models.Payroll:
        db_payroll = PayrollService.get_payroll(db, payroll_id)
        
        update_data = payroll_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_payroll, field, value)
        
        # Recalcular total si cambió algún campo monetario
        if any(field in update_data for field in ['salary', 'bonus', 'commission']):
            db_payroll.total_pay = PayrollService.calculate_total_pay(
                db_payroll.salary, db_payroll.bonus, db_payroll.commission
            )
        
        db.commit()
        db.refresh(db_payroll)
        return db_payroll


class VacationService:
    
    @staticmethod
    def calculate_vacation_days_available(db: Session, employee_id: int) -> int:
        employee = db.query(models.Employee).filter(
            models.Employee.employee_id == employee_id
        ).first()
        
        if not employee:
            return 0
        
        # Calcular años de antigüedad
        today = date.today()
        years_worked = (today - employee.hire_date).days // 365
        
        # Fórmula según la ley mexicana: 12 días primer año, +2 días por año hasta 5 años
        # después +2 días cada 5 años
        if years_worked < 1:
            base_days = 12
        elif years_worked <= 5:
            base_days = 12 + (years_worked - 1) * 2
        else:
            base_days = 20 + ((years_worked - 5) // 5) * 2
        
        # Restar días ya utilizados en el año actual
        year_start = date(today.year, 1, 1)
        used_days = db.query(models.Vacation).filter(
            models.Vacation.employee_id == employee_id,
            models.Vacation.start_date >= year_start,
            models.Vacation.status == models.StatusEnum.APROBADO
        ).with_entities(models.Vacation.vacation_days).all()
        
        total_used = sum([days[0] for days in used_days])
        return max(0, base_days - total_used)
    
    @staticmethod
    def create_vacation(db: Session, vacation: schemas.VacationCreate) -> models.Vacation:
        # Verificar que el empleado existe
        employee = db.query(models.Employee).filter(
            models.Employee.employee_id == vacation.employee_id
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Calcular días disponibles
        available_days = VacationService.calculate_vacation_days_available(db, vacation.employee_id)
        
        if vacation.vacation_days > available_days:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Solo tiene {available_days} días disponibles"
            )
        
        remaining = available_days - vacation.vacation_days
        
        db_vacation = models.Vacation(
            **vacation.dict(),
            remaining_days=remaining
        )
        db.add(db_vacation)
        db.commit()
        db.refresh(db_vacation)
        return db_vacation
    
    @staticmethod
    def get_vacation(db: Session, vacation_id: int) -> models.Vacation:
        vacation = db.query(models.Vacation).filter(
            models.Vacation.vacation_id == vacation_id
        ).first()
        if not vacation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud de vacaciones no encontrada"
            )
        return vacation
    
    @staticmethod
    def get_vacations_by_employee(db: Session, employee_id: int) -> List[models.Vacation]:
        return db.query(models.Vacation).filter(
            models.Vacation.employee_id == employee_id
        ).all()
    
    @staticmethod
    def update_vacation(db: Session, vacation_id: int, vacation_update: schemas.VacationUpdate) -> models.Vacation:
        db_vacation = VacationService.get_vacation(db, vacation_id)
        
        update_data = vacation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vacation, field, value)
        
        db.commit()
        db.refresh(db_vacation)
        return db_vacation


class AdministrativeRecordService:
    
    @staticmethod
    def create_record(db: Session, record: schemas.AdministrativeRecordCreate) -> models.AdministrativeRecord:
        # Verificar que el empleado existe
        employee = db.query(models.Employee).filter(
            models.Employee.employee_id == record.employee_id
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        db_record = models.AdministrativeRecord(**record.dict())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    
    @staticmethod
    def get_record(db: Session, record_id: int) -> models.AdministrativeRecord:
        record = db.query(models.AdministrativeRecord).filter(
            models.AdministrativeRecord.record_id == record_id
        ).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro administrativo no encontrado"
            )
        return record
    
    @staticmethod
    def get_records_by_employee(db: Session, employee_id: int) -> List[models.AdministrativeRecord]:
        return db.query(models.AdministrativeRecord).filter(
            models.AdministrativeRecord.employee_id == employee_id
        ).order_by(models.AdministrativeRecord.created_at.desc()).all()
    
    @staticmethod
    def update_record(db: Session, record_id: int, record_update: schemas.AdministrativeRecordUpdate) -> models.AdministrativeRecord:
        db_record = AdministrativeRecordService.get_record(db, record_id)
        
        update_data = record_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_record, field, value)
        
        db.commit()
        db.refresh(db_record)
        return db_record


class AbsenceService:
    
    @staticmethod
    def create_absence(db: Session, absence: schemas.AbsenceCreate) -> models.Absence:
        # Verificar que el empleado existe
        employee = db.query(models.Employee).filter(
            models.Employee.employee_id == absence.employee_id
        ).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        db_absence = models.Absence(**absence.dict())
        db.add(db_absence)
        db.commit()
        db.refresh(db_absence)
        return db_absence
    
    @staticmethod
    def get_absence(db: Session, absence_id: int) -> models.Absence:
        absence = db.query(models.Absence).filter(
            models.Absence.absence_id == absence_id
        ).first()
        if not absence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de inasistencia no encontrado"
            )
        return absence
    
    @staticmethod
    def get_absences_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[models.Absence]:
        return db.query(models.Absence).filter(
            models.Absence.employee_id == employee_id
        ).order_by(models.Absence.start_date.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_absence(db: Session, absence_id: int, absence_update: schemas.AbsenceUpdate) -> models.Absence:
        db_absence = AbsenceService.get_absence(db, absence_id)
        
        update_data = absence_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_absence, field, value)
        
        db.commit()
        db.refresh(db_absence)
        return db_absence
    
    @staticmethod
    def get_absences_by_date_range(db: Session, employee_id: int, start_date: date, end_date: date) -> List[models.Absence]:
        return db.query(models.Absence).filter(
            models.Absence.employee_id == employee_id,
            models.Absence.start_date >= start_date,
            models.Absence.end_date <= end_date
        ).all()