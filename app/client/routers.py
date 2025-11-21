from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.auth.routers import get_current_user
from app.client.schemas import (
    ClientCreate, ClientUpdate, ClientResponse, ClientListResponse,
    BranchCreate, BranchUpdate, BranchResponse,
    AreaCreate, AreaUpdate, AreaResponse
)
from app.client.services import ClientService, BranchService, AreaService

router = APIRouter()

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ClientService.create_client(db, client_data, current_user.user_id)


@router.get("/", response_model=List[ClientListResponse])
def get_all_clients(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    clients = ClientService.get_all_clients(db, skip, limit, is_active)

    result = []

    for c in clients:

        # calcular total de areas
        total_areas = 0
        for b in c.branches:
            total_areas += len(b.areas)

        result.append(
            ClientListResponse(
                client_id=c.client_id,
                name=c.name,
                rfc=c.rfc,

                address=c.address,
                colonia=c.colonia,
                zip_code=c.zip_code,
                city=c.city,

                is_active=c.is_active,
                created_at=c.created_at,
                total_branches=len(c.branches),
                total_areas=total_areas
            )
        )

    return result

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    client = ClientService.get_client_by_id(db, client_id)
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return client


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ClientService.update_client(db, client_id, client_data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ClientService.delete_client(db, client_id)
    return None


@router.post("/{client_id}/branches", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(
    client_id: int,
    branch_data: BranchCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if branch_data.client_id != client_id:
        raise HTTPException(
            status_code=400,
            detail="El client_id del body no coincide con el de la ruta"
        )

    return BranchService.create_branch(db, branch_data)


@router.get("/{client_id}/branches", response_model=List[BranchResponse])
def get_client_branches(
    client_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return BranchService.get_branches_by_client(db, client_id)


@router.get("/branches/{branch_id}", response_model=BranchResponse)
def get_branch(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    branch = BranchService.get_branch_by_id(db, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return branch


@router.patch("/branches/{branch_id}", response_model=BranchResponse)
def update_branch(
    branch_id: int,
    branch_data: BranchUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return BranchService.update_branch(db, branch_id, branch_data)


@router.delete("/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    BranchService.delete_branch(db, branch_id)
    return None


@router.post("/branches/{branch_id}/areas", response_model=AreaResponse, status_code=status.HTTP_201_CREATED)
def create_area(
    branch_id: int,
    area_data: AreaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if area_data.branch_id != branch_id:
        raise HTTPException(
            status_code=400,
            detail="El branch_id del body no coincide con el de la ruta"
        )

    return AreaService.create_area(db, area_data)


@router.get("/branches/{branch_id}/areas", response_model=List[AreaResponse])
def get_branch_areas(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return AreaService.get_areas_by_branch(db, branch_id)


@router.get("/areas/{area_id}", response_model=AreaResponse)
def get_area(
    area_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    area = AreaService.get_area_by_id(db, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return area


@router.patch("/areas/{area_id}", response_model=AreaResponse)
def update_area(
    area_id: int,
    area_data: AreaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return AreaService.update_area(db, area_id, area_data)


@router.delete("/areas/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(
    area_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    AreaService.delete_area(db, area_id)
    return None