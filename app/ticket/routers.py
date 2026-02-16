from fastapi import APIRouter, Depends, status, Query, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import uuid
from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from ticket.schemas import TicketCreate, TicketUpdate, TicketResponse, TicketListResponse
from ticket.services import TicketService
from ticket.models import ReportStatus

router = APIRouter(prefix="/tickets", tags=["Tickets"])

UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads" / "tickets"


@router.post("/evidence/upload", status_code=status.HTTP_201_CREATED)
async def upload_ticket_evidence(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    original_name = Path(file.filename or "evidence").name
    safe_name = f"{uuid.uuid4().hex}_{original_name}"
    destination = UPLOADS_DIR / safe_name

    content = await file.read()
    with destination.open("wb") as output_file:
        output_file.write(content)

    return {
        "file_path": f"uploads/tickets/{safe_name}",
        "filename": original_name
    }


@router.get("/evidence/{filename}")
def get_ticket_evidence(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    file_path = UPLOADS_DIR / Path(filename).name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Archivo no encontrado")
    return FileResponse(path=file_path, filename=file_path.name)

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #Crea nuevo ticket 
    return TicketService.create_ticket(db, ticket, current_user.user_id)

@router.get("/", response_model=List[TicketListResponse])
def get_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    client_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    report_status: Optional[ReportStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.get_all_tickets(
        db, 
        skip=skip, 
        limit=limit,
        client_id=client_id,
        branch_id=branch_id,
        report_status=report_status
    )

@router.get("/my-tickets", response_model=List[TicketListResponse])
def get_my_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.get_tickets_by_user(
        db, 
        current_user.user_id,
        skip=skip,
        limit=limit
    )

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.get_ticket_by_id(db, ticket_id)

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.update_ticket(db, ticket_id, ticket_update)

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    TicketService.delete_ticket(db, ticket_id)
    return None