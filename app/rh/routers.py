from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db 
from . import schemas, services

router = APIRouter(prefix="/rh", tags=["RH"])

@router.post("/employees", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo empleado
    
    - user_id: ID del usuario asociado
    - nss: 
    - rfc: 
    - curp: 
    """
    return services.EmployeeService.create_employee(db, employee)


@router.get("/employees", response_model=List[schemas.EmployeeResponse])
def get_employees(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros"),
    is_active: Optional[bool] = Query(None, description="Filtrar por empleados activos/inactivos"),
    db: Session = Depends(get_db)
):
    """Listar todos los empleados con paginación y filtros"""
    return services.EmployeeService.get_employees(db, skip, limit, is_active)


@router.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un empleado específico por su ID"""
    return services.EmployeeService.get_employee(db, employee_id)


@router.get("/employees/user/{user_id}", response_model=schemas.EmployeeResponse)
def get_employee_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtener empleado por ID de usuario"""
    employee = services.EmployeeService.get_employee_by_user_id(db, user_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró un empleado asociado a este usuario"
        )
    return employee


@router.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar información de un empleado"""
    return services.EmployeeService.update_employee(db, employee_id, employee_update)


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un empleado (usar con precaución)"""
    services.EmployeeService.delete_employee(db, employee_id)
    return None


# ========== PAYROLL ENDPOINTS ==========
@router.post("/payrolls", response_model=schemas.PayrollResponse, status_code=status.HTTP_201_CREATED)
def create_payroll(
    payroll: schemas.PayrollCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva nómina
    
    El total se calcula automáticamente: salary + bonus + commission
    """
    return services.PayrollService.create_payroll(db, payroll)


@router.get("/payrolls/{payroll_id}", response_model=schemas.PayrollResponse)
def get_payroll(
    payroll_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una nómina específica por ID"""
    return services.PayrollService.get_payroll(db, payroll_id)


@router.get("/employees/{employee_id}/payrolls", response_model=List[schemas.PayrollResponse])
def get_employee_payrolls(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener todas las nóminas de un empleado específico"""
    return services.PayrollService.get_payrolls_by_employee(db, employee_id, skip, limit)


@router.put("/payrolls/{payroll_id}", response_model=schemas.PayrollResponse)
def update_payroll(
    payroll_id: int,
    payroll_update: schemas.PayrollUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una nómina
    
    El total se recalcula automáticamente si se modifican salary, bonus o commission
    """
    return services.PayrollService.update_payroll(db, payroll_id, payroll_update)


# ========== VACATION ENDPOINTS ==========
@router.post("/vacations", response_model=schemas.VacationResponse, status_code=status.HTTP_201_CREATED)
def create_vacation(
    vacation: schemas.VacationCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una solicitud de vacaciones
    
    Se valida automáticamente que el empleado tenga días disponibles
    basándose en la Ley Federal del Trabajo de México
    """
    return services.VacationService.create_vacation(db, vacation)


@router.get("/vacations/{vacation_id}", response_model=schemas.VacationResponse)
def get_vacation(
    vacation_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una solicitud de vacaciones específica"""
    return services.VacationService.get_vacation(db, vacation_id)


@router.get("/employees/{employee_id}/vacations", response_model=List[schemas.VacationResponse])
def get_employee_vacations(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todas las solicitudes de vacaciones de un empleado"""
    return services.VacationService.get_vacations_by_employee(db, employee_id)


@router.get("/employees/{employee_id}/vacation-days")
def get_available_vacation_days(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Calcular días de vacaciones disponibles
    
    Basado en antigüedad según la Ley Federal del Trabajo
    """
    available = services.VacationService.calculate_vacation_days_available(db, employee_id)
    return {
        "employee_id": employee_id,
        "available_days": available
    }


@router.put("/vacations/{vacation_id}", response_model=schemas.VacationResponse)
def update_vacation(
    vacation_id: int,
    vacation_update: schemas.VacationUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una solicitud de vacaciones
    
    Común para aprobar/rechazar solicitudes
    """
    return services.VacationService.update_vacation(db, vacation_id, vacation_update)


# ========== ADMINISTRATIVE RECORD ENDPOINTS ==========
@router.post("/administrative-records", response_model=schemas.AdministrativeRecordResponse, status_code=status.HTTP_201_CREATED)
def create_administrative_record(
    record: schemas.AdministrativeRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un registro administrativo
    
    Tipos: retroalimentación escrita, amonestación, acta administrativa, 
    entrevista por ausentismo
    """
    return services.AdministrativeRecordService.create_record(db, record)


@router.get("/administrative-records/{record_id}", response_model=schemas.AdministrativeRecordResponse)
def get_administrative_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un registro administrativo específico"""
    return services.AdministrativeRecordService.get_record(db, record_id)


@router.get("/employees/{employee_id}/administrative-records", response_model=List[schemas.AdministrativeRecordResponse])
def get_employee_administrative_records(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los registros administrativos de un empleado
    
    Ordenados por fecha de creación (más reciente primero)
    """
    return services.AdministrativeRecordService.get_records_by_employee(db, employee_id)


@router.put("/administrative-records/{record_id}", response_model=schemas.AdministrativeRecordResponse)
def update_administrative_record(
    record_id: int,
    record_update: schemas.AdministrativeRecordUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un registro administrativo"""
    return services.AdministrativeRecordService.update_record(db, record_id, record_update)


# ========== ABSENCE ENDPOINTS ==========
@router.post("/absences", response_model=schemas.AbsenceResponse, status_code=status.HTTP_201_CREATED)
def create_absence(
    absence: schemas.AbsenceCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar una inasistencia
    
    Tipos: enfermedad, ausentismo, permiso personal, otro
    """
    return services.AbsenceService.create_absence(db, absence)


@router.get("/absences/{absence_id}", response_model=schemas.AbsenceResponse)
def get_absence(
    absence_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un registro de inasistencia específico"""
    return services.AbsenceService.get_absence(db, absence_id)


@router.get("/employees/{employee_id}/absences", response_model=List[schemas.AbsenceResponse])
def get_employee_absences(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las inasistencias de un empleado
    
    Ordenadas por fecha (más reciente primero)
    """
    return services.AbsenceService.get_absences_by_employee(db, employee_id, skip, limit)


@router.get("/employees/{employee_id}/absences/range", response_model=List[schemas.AbsenceResponse])
def get_employee_absences_by_range(
    employee_id: int,
    start_date: date = Query(..., description="Fecha inicial (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Fecha final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Obtener inasistencias de un empleado en un rango de fechas"""
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha final debe ser posterior a la fecha inicial"
        )
    return services.AbsenceService.get_absences_by_date_range(db, employee_id, start_date, end_date)


@router.put("/absences/{absence_id}", response_model=schemas.AbsenceResponse)
def update_absence(
    absence_id: int,
    absence_update: schemas.AbsenceUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un registro de inasistencia
    
    Común para justificar faltas o cambiar estado
    """
    return services.AbsenceService.update_absence(db, absence_id, absence_update)


# ========== ESTADÍSTICAS Y REPORTES ==========
@router.get("/employees/{employee_id}/summary")
def get_employee_summary(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un resumen completo del empleado
    
    Incluye información de vacaciones, inasistencias, registros administrativos
    """
    employee = services.EmployeeService.get_employee(db, employee_id)
    
    # Obtener días de vacaciones disponibles
    vacation_days = services.VacationService.calculate_vacation_days_available(db, employee_id)
    
    # Contar inasistencias del año actual
    year_start = date(date.today().year, 1, 1)
    year_end = date.today()
    absences_this_year = services.AbsenceService.get_absences_by_date_range(
        db, employee_id, year_start, year_end
    )
    
    # Contar registros administrativos
    admin_records = services.AdministrativeRecordService.get_records_by_employee(db, employee_id)
    
    # Obtener última nomina
    last_payroll = services.PayrollService.get_payrolls_by_employee(db, employee_id, skip=0, limit=1)
    
    return {
        "employee": {
            "id": employee.employee_id,
            "user_id": employee.user_id,
            "full_name": "Obtener del user",
            "nss": employee.nss,
            "rfc": employee.rfc,
            "hire_date": employee.hire_date,
            "is_active": employee.is_active
        },
        "vacation_stats": {
            "available_days": vacation_days,
            "pending_requests": len([v for v in services.VacationService.get_vacations_by_employee(db, employee_id) 
                                     if v.status == schemas.StatusEnum.PENDIENTE])
        },
        "absence_stats": {
            "total_this_year": len(absences_this_year),
            "justified": len([a for a in absences_this_year if a.is_justified]),
            "unjustified": len([a for a in absences_this_year if not a.is_justified])
        },
        "administrative_records": {
            "total": len(admin_records),
            "by_type": {}  # Podrías agregar un contador por tipo
        },
        "last_payroll": last_payroll[0] if last_payroll else None
    }


@router.get("/stats/department/{department}")
def get_department_stats(
    department: str,
    db: Session = Depends(get_db)
):

    return {
        "message": "Implementar según necesidades específicas",
        "department": department
    }