from .core.database import SessionLocal
from .auth.models import User, RolEnum, DepartmentEnum
from .auth.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # Verificar si ya existe un admin
        existing_admin = db.query(User).filter(User.rol == RolEnum.ADMINISTRADOR).first()
        if existing_admin:
            print(f"⚠️  Ya existe un administrador: {existing_admin.email}")
            return
        
        # Crear usuario administrador
        admin_user = User(
            email="admin@copymart.com",
            full_name="Administrador CopyMart",
            password=get_password_hash("admin123"),
            rol=RolEnum.ADMINISTRADOR,
            department=DepartmentEnum.ADMINISTRACION,
            is_active=True,
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Usuario administrador creado exitosamente!")
        print(f"   Email: {admin_user.email}")
        print(f"   Contraseña: admin123")
        print(f"   Nombre: {admin_user.full_name}")
        print(f"   Rol: {admin_user.rol}")
        print(f"   Departamento: {admin_user.department}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()

