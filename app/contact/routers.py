from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.contact.schemas import ContactCreate, ContactRead
from app.contact import services

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.get("/", response_model=List[ContactRead])
def list_contacts(db: Session = Depends(get_db)):
    return services.get_contacts(db)


@router.get("/search", response_model=ContactRead)
def search_contact(name: str, db: Session = Depends(get_db)):
    contact = services.get_contact_by_name(db, name)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = services.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactRead)
def create_contact_endpoint(contact: ContactCreate, db: Session = Depends(get_db)):
    return services.create_contact(db, contact)


@router.put("/{contact_id}/status", response_model=ContactRead)
def change_contact_status(contact_id: int, is_active: bool, db: Session = Depends(get_db)):
    updated = services.change_status(db, contact_id, is_active)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated
