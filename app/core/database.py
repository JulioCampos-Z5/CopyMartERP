from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MariaDB/MySQL
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/copymart"

# PostgreSQL 
#DATABASE_URL = "postgresql://usuario:password@localhost:5432/copymart_erp"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()