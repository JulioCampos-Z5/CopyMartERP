from passlib.context import CryptContext
from jose import JWTError, jwt 
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.auth.schemas import TokenData
from app.auth.models import RolEnum, DepartmentEnum

SECRET_KEY = "JindnsniuNkna"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> TokenData: 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        user_id = payload.get("user_id")
        rol = payload.get("rol")
        department = payload.get("department") 

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalid") 

        return TokenData(
            user_id=user_id,
            rol=RolEnum(rol),
            department=DepartmentEnum(department)
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalid")