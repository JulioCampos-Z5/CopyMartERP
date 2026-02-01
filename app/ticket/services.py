from sqlalchemy.orm import Session
from sqlalchemy import desc
from ticket.models import Ticket, ReportStatus
from ticket.schemas import TicketCreate, TicketUpdate
from datetime import datetime
from fastapi import HTTPException, status

class TicketService:
    
    @staticmethod
    def create_ticket(db: Session, ticket_data: TicketCreate, user_id: int) -> Ticket:
        #Crea nuevo ticket
        ticket = Ticket(
            **ticket_data.model_dump(),
            created_by=user_id
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket
    
    @staticmethod
    def get_ticket_by_id(db: Session, ticket_id: int) -> Ticket:
        #ticket por id
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )
        return ticket
    
    @staticmethod
    def get_all_tickets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        client_id: int = None,
        branch_id: int = None,
        report_status: ReportStatus = None
    ):
        #obtiene todos los ticket por el id 
        query = db.query(Ticket)
        
        if client_id:
            query = query.filter(Ticket.client_id == client_id)
        if branch_id:
            query = query.filter(Ticket.branch_id == branch_id)
        if report_status:
            query = query.filter(Ticket.report_status == report_status)
        
        query = query.order_by(desc(Ticket.created_at))
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int,
        ticket_data: TicketUpdate
    ) -> Ticket:
        
        #actualiza todos los tickets
        ticket = TicketService.get_ticket_by_id(db, ticket_id)
        
        update_data = ticket_data.model_dump(exclude_unset=True)
        
        # Si se actualiza a "listo", agregar fecha de finalización
        if "report_status" in update_data:
            if update_data["report_status"] == ReportStatus.LISTO:
                update_data["completed_at"] = datetime.utcnow()
            # Si cambia de listo a otro estado, quitar fecha de finalización
            elif ticket.report_status == ReportStatus.LISTO:
                update_data["completed_at"] = None
        
        for field, value in update_data.items():
            setattr(ticket, field, value)
        
        db.commit()
        db.refresh(ticket)
        return ticket
    
    @staticmethod
    def delete_ticket(db: Session, ticket_id: int) -> bool:
        """Eliminar un ticket"""
        ticket = TicketService.get_ticket_by_id(db, ticket_id)
        db.delete(ticket)
        db.commit()
        return True
    
    @staticmethod
    def get_tickets_by_user(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ):
        #obtener ticket por un usuario en especifico
        return db.query(Ticket)\
            .filter(Ticket.created_by == user_id)\
            .order_by(desc(Ticket.created_at))\
            .offset(skip)\
            .limit(limit)\
            .all()