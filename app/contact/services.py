from sqlalchemy.orm import Session
from .models import Contact
from .schemas import ContactCreate, ContactUpdate
from datetime import datetime

def get_contacts(db: Session):
    return db.query(Contact).all()


def get_contact_by_name(db: Session, name: str):
    return db.query(Contact).filter(Contact.name.ilike(f"%{name}%")).first()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.contact_id == contact_id).first()


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        company=contact.company,
        rol=contact.rol,
        is_client=contact.is_client,
        is_active=True,
        created_at=datetime.utcnow()
    )

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def change_status(db: Session, contact_id: int, is_active: bool):
    db_contact = get_contact_by_id(db, contact_id)
    if not db_contact:
        return None
    
    db_contact.is_active = is_active
    db.commit()
    db.refresh(db_contact)
    return db_contact

