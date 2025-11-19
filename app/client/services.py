from sqlalchemy.orm import Session
from app.client.models import Client, Branch, Area
from app.client.schemas import ClientCreate, BranchCreate, AreaCreate

def create_client(db: Session, client_data: ClientCreate):
    client = Client(**client_data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_clients(db: Session):
    return db.query(Client).all()

def create_branch(db: Session, branch_data: BranchCreate):
    branch = Branch(**branch_data.dict())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch

def get_branches(db: Session, client_id: int):
    return db.query(Branch).filter(Branch.client_id == client_id).all()

def create_area(db: Session, area_data: AreaCreate):
    area = Area(**area_data.dict())
    db.add(area)
    db.commit()
    db.refresh(area)
    return area

def get_areas(db: Session, branch_id: int):
    return db.query(Area).filter(Area.branch_id == branch_id).all()
