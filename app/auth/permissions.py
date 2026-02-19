from typing import List
from fastapi import HTTPException, status
from auth.models import User, RolEnum, DepartmentEnum

# Mapeo de endpoints/rutas a áreas de permisos
ROUTE_TO_AREA = {
    "/sales": "ventas",
    "/rents": "rentas",
    "/clients": "clientes",
    "/inventory": "inventario",
    "/warehouse": "almacen",
    "/purchases": "compras",
    "/billing": "cobranza",
    "/invoicing": "facturacion",
    "/production": "produccion",
    "/tickets": "ordenes_servicio",
    "/rh": "recursos_humanos",
    "/users": "usuarios",
}

# Mapeo legacy para compatibilidad con departamentos
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


# ==================== SISTEMA DE PERMISOS GRANULARES ====================

def has_permission(user: User, area: str, action: str) -> bool:
    """
    Verifica si un usuario tiene un permiso específico en un área.
    
    Args:
        user: Usuario a verificar
        area: Área del sistema (ventas, rentas, clientes, etc.)
        action: Acción a verificar (view, create, edit, delete)
    
    Returns:
        bool: True si el usuario tiene el permiso, False en caso contrario
    """
    # Verificar permisos granulares (aplica a TODOS los roles incluyendo administradores)
    if user.permissions and isinstance(user.permissions, dict):
        area_perms = user.permissions.get(area, {})
        if isinstance(area_perms, dict):
            return area_perms.get(action, False)
    
    return False


def require_permission(area: str, action: str):
    """
    Decorador/dependencia para verificar permisos en endpoints.
    
    Usage:
        @router.get("/")
        def get_sales(
            current_user: User = Depends(get_current_user),
            _: None = Depends(require_permission("ventas", "view"))
        ):
            ...
    """
    from fastapi import Depends
    from auth.routers import get_current_user
    
    def check_permission(current_user: User = Depends(get_current_user)) -> None:
        if not has_permission(current_user, area, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permiso para {action} en el área de {area}"
            )
        return None
    return check_permission


def get_user_areas(user: User) -> List[str]:
    """Retorna la lista de áreas a las que el usuario tiene acceso."""
    if user.permissions and isinstance(user.permissions, dict):
        return list(user.permissions.keys())
    
    return []


def get_user_permissions(user: User, area: str) -> dict:
    """Retorna los permisos específicos de un usuario en un área."""
    if user.permissions and isinstance(user.permissions, dict):
        return user.permissions.get(area, {"view": False, "create": False, "edit": False, "delete": False})
    
    return {"view": False, "create": False, "edit": False, "delete": False}


# ==================== FUNCIONES LEGACY (Compatibilidad) ====================

def can_create(user: User) -> bool:
    """Legacy: Verifica si el usuario puede crear (basado en rol)"""
    return user.rol in [RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]

def can_edit(user: User) -> bool:
    """Legacy: Verifica si el usuario puede editar (basado en rol)"""
    return user.rol in [RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]

def can_delete(user: User) -> bool:
    """Legacy: Verifica si el usuario puede eliminar (basado en rol)"""
    return user.rol in [RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]

def can_view_module(user: User, module: str) -> bool:
    """Legacy: Verifica si el usuario puede ver un módulo (basado en departamento)"""
    # Administradores pueden ver todo
    if user.rol == RolEnum.ADMINISTRADOR:
        return True
    
    # Verificar permisos granulares si existen
    if user.permissions and isinstance(user.permissions, dict):
        area_perms = user.permissions.get(module, {})
        if isinstance(area_perms, dict):
            return area_perms.get("view", False)
    
    # Fallback a sistema legacy por departamento
    permission = MODULE_PERMISSIONS.get(user.department, {"modules": [], "read_only": []})
    return module in permission["modules"] or module in permission["read_only"]

def can_edit_module(user: User, module: str) -> bool:
    """Legacy: Verifica si el usuario puede editar un módulo"""
    # Administradores pueden editar todo
    if user.rol == RolEnum.ADMINISTRADOR:
        return True
    
    # Verificar permisos granulares si existen
    if user.permissions and isinstance(user.permissions, dict):
        area_perms = user.permissions.get(module, {})
        if isinstance(area_perms, dict):
            return area_perms.get("edit", False)
    
    # Fallback a rol
    return user.rol in [RolEnum.GERENCIA]

def get_accesible_modules(user: User) -> list[str]:
    """Retorna los módulos accesibles para el usuario"""
    if user.rol == RolEnum.ADMINISTRADOR:
        return list(ROUTE_TO_AREA.values())
    
    # Usar permisos granulares si existen
    if user.permissions and isinstance(user.permissions, dict):
        return list(user.permissions.keys())
    
    # Fallback a sistema legacy por departamento
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
