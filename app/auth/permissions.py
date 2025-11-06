from typing import List
from app.auth.models import User, RolEnum, DepartmentEnum

MODULE_PERMISSIONS = {
    DepartmentEnum.RH: {
        "modules": ["rh"],
        "read_only": []
    },
    DepartmentEnum.ADMINISTRACION: {
        "modules": ["ventas", "inventario", "rentas", "finance"],  
    },
    DepartmentEnum.COMERCIAL: { 
        "modules": ["ventas", "atencion_clientes", "rentas", "soporte"],
        "read_only": []
    },
    DepartmentEnum.OPERACIONES: {
        "modules": ["operaciones"],
        "read_only": []
    },
} 


def can_create(user: User) -> bool:
    return user.rol in [RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]

def can_edit(user: User) -> bool:
    return user.rol in [RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]

def can_delete(user: User) -> bool:
    return user.rol in [RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]

def can_view_module(user: User, module: str) -> bool:
    permission = MODULE_PERMISSIONS.get(user.department, {"modules": [], "read_only": []})
    return module in permission["modules"] or module in permission["read_only"]

def can_edit_module(user: User, module: str) -> bool:
    if user.rol == RolEnum.USUARIO:
        return False
    return True

def get_accesible_modules(user: User) -> list[str]:
    permission = MODULE_PERMISSIONS.get(user.department, {"modules": [], "read_only": []})
    return permission["modules"] + permission["read_only"]

def can_create_rol(creator: User, rol_to_create: RolEnum) -> bool:
    if creator.rol == RolEnum.ADMINISTRADOR:
        return rol_to_create in [RolEnum.GERENCIA, RolEnum.USUARIO]
    elif creator.rol == RolEnum.GERENCIA:
        return rol_to_create == RolEnum.USUARIO
    return False

def can_modify_user(modifier: User, target: User) -> bool:
    if modifier.rol == RolEnum.ADMINISTRADOR:
        return target.rol in [RolEnum.GERENCIA, RolEnum.USUARIO]
    elif modifier.rol == RolEnum.GERENCIA:
        return target.rol == RolEnum.USUARIO
    return False

def can_modify_password(modifier: User, target: User) -> bool:
    return can_modify_user(modifier, target)

def can_modify_email(modifier: User, target: User) -> bool:
    return can_modify_user(modifier, target)