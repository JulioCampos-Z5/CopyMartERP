from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from ticket.schemas import TicketCreate, TicketUpdate, TicketResponse, TicketListResponse
from ticket.services import TicketService
from ticket.models import ReportStatus

router = APIRouter(prefix="/tickets", tags=["Tickets"])

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