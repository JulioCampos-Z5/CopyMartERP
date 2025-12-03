from typing import List
from app.auth.models import User, RolEnum

# Módulos accesibles según el rol
MODULE_PERMISSIONS = {
    RolEnum.ADMIN: {
        "modules": ["rh", "ventas", "inventario", "rentas", "finance", "atencion_clientes", "soporte", "operaciones", "usuarios"],
        "read_only": []
    },
    RolEnum.GERENTE: {
        "modules": ["ventas", "inventario", "rentas", "finance", "atencion_clientes", "operaciones"],
        "read_only": ["rh"]
    },
    RolEnum.EMPLEADO: {
        "modules": ["ventas", "atencion_clientes"],
        "read_only": ["inventario"]
    },
}


def can_create(user: User) -> bool:
    return user.role in [RolEnum.ADMIN, RolEnum.GERENTE]

def can_edit(user: User) -> bool:
    return user.role in [RolEnum.ADMIN, RolEnum.GERENTE]

def can_delete(user: User) -> bool:
    return user.role in [RolEnum.ADMIN, RolEnum.GERENTE]

def can_view_module(user: User, module: str) -> bool:
    permission = MODULE_PERMISSIONS.get(user.role, {"modules": [], "read_only": []})
    return module in permission["modules"] or module in permission.get("read_only", [])

def can_edit_module(user: User, module: str) -> bool:
    if user.role == RolEnum.EMPLEADO:
        return False
    return True

def get_accesible_modules(user: User) -> list[str]:
    permission = MODULE_PERMISSIONS.get(user.role, {"modules": [], "read_only": []})
    return permission["modules"] + permission.get("read_only", [])

def can_create_rol(creator: User, rol_to_create: RolEnum) -> bool:
    if creator.role == RolEnum.ADMIN:
        return rol_to_create in [RolEnum.GERENTE, RolEnum.EMPLEADO]
    elif creator.role == RolEnum.GERENTE:
        return rol_to_create == RolEnum.EMPLEADO
    return False

def can_modify_user(modifier: User, target: User) -> bool:
    if modifier.role == RolEnum.ADMIN:
        return target.role in [RolEnum.GERENTE, RolEnum.EMPLEADO]
    elif modifier.role == RolEnum.GERENTE:
        return target.role == RolEnum.EMPLEADO
    return False

def can_modify_password(modifier: User, target: User) -> bool:
    return can_modify_user(modifier, target)

def can_modify_email(modifier: User, target: User) -> bool:
    return can_modify_user(modifier, target)