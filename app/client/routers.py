from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.client.schemas import (
    ClientCreate, ClientRead, 
    BranchCreate, BranchRead, 
    AreaCreate, AreaRead
)
from app.client.services import (
    create_client, get_clients, 
    create_branch, get_branches, 
    create_area, get_areas
)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientRead)
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.get("/", response_model=List[ClientRead])
def list_clients(db: Session = Depends(get_db)):
    return get_clients(db)


@router.post("/branches/", response_model=BranchRead)
def add_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return create_branch(db, branch)

@router.get("/branches/{client_id}", response_model=List[BranchRead])
def list_branches(client_id: int, db: Session = Depends(get_db)):
    return get_branches(db, client_id)

@router.post("/areas/", response_model=AreaRead)
def add_area(area: AreaCreate, db: Session = Depends(get_db)):
    return create_area(db, area)

@router.get("/areas/{branch_id}", response_model=List[AreaRead])
def list_areas(branch_id: int, db: Session = Depends(get_db)):
    return get_areas(db, branch_id)
