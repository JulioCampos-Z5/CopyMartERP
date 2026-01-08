from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from typing import List, Optional

from .schemas import (
    ClientCreate, ClientUpdate,
    BranchCreate, BranchUpdate,
    AreaCreate, AreaUpdate,
)
from .models import Client, Branch, Area
from ..contact.models import Contact



## Crear un cliente con domicilio, sucursales y areas
class ClientService:

    @staticmethod
    def create_client(db: Session, client_data: ClientCreate, user_id: int) -> Client:
        contact_id = None
        
        # Si viene contact_id, validar que existe
        if client_data.contact_id:
            contact = db.query(Contact).filter(Contact.contact_id == client_data.contact_id).first()
            if not contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Contacto no encontrado"
                )
            contact_id = client_data.contact_id
        
        # Si vienen datos de contacto en el cliente, crear el contacto automáticamente
        elif client_data.contact_name:
            new_contact = Contact(
                name=client_data.contact_name,
                phone=client_data.contact_phone,
                email=client_data.contact_email,
                company=client_data.name,
                rol=client_data.contact_rol,
                is_client=True
            )
            db.add(new_contact)
            db.flush()
            contact_id = new_contact.contact_id

        new_client = Client(
            name=client_data.name,
            comercial_name=client_data.comercial_name,
            rfc=client_data.rfc,
            contact_id=contact_id,
            user_id=user_id,
            address=client_data.address,
            colonia=client_data.colonia,
            zip_code=client_data.zip_code,
            city=client_data.city
        )
        db.add(new_client)
        db.flush()

        # Crea sucursales si vienen
        if client_data.branches:
            for branch_data in client_data.branches:

                new_branch = Branch(
                    client_id=new_client.client_id,
                    name=branch_data.name,
                    is_main=branch_data.is_main,
                    address=branch_data.address,
                    colonia=branch_data.colonia,
                    zip_code=branch_data.zip_code,
                    city=branch_data.city
                )
                db.add(new_branch)
                db.flush()

                # Crea areas dentro de sucursal
                if branch_data.areas:
                    for area_name in branch_data.areas:
                        db.add(Area(branch_id=new_branch.branch_id, name=area_name))

        db.commit()
        db.refresh(new_client)
        return new_client

    @staticmethod
    def get_client_by_id(db: Session, client_id: int) -> Optional[Client]:
        return db.query(Client).options(
            joinedload(Client.branches).joinedload(Branch.areas),
            joinedload(Client.contact)
        ).filter(Client.client_id == client_id).first()

    @staticmethod
    def get_all_clients(db: Session, skip: int = 0, limit: int = 100,
                        is_active: Optional[bool] = None) -> List[Client]:

        query = db.query(Client).options(
            joinedload(Client.branches).joinedload(Branch.areas),
            joinedload(Client.contact)
        )

        if is_active is not None:
            query = query.filter(Client.is_active == is_active)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_client(db: Session, client_id: int, client_data: ClientUpdate) -> Client:
        client = db.query(Client).filter(Client.client_id == client_id).first()

        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Valida contacto si se actualiza
        if client_data.contact_id is not None:
            contact = db.query(Contact).filter(Contact.contact_id == client_data.contact_id).first()
            if not contact:
                raise HTTPException(status_code=404, detail="Contacto no encontrado")

        # Si vienen datos de contacto, actualizar o crear el contacto
        if client_data.contact_name:
            if client.contact_id:
                # Actualizar contacto existente
                contact = db.query(Contact).filter(Contact.contact_id == client.contact_id).first()
                if contact:
                    contact.name = client_data.contact_name
                    if client_data.contact_phone:
                        contact.phone = client_data.contact_phone
                    if client_data.contact_email:
                        contact.email = client_data.contact_email
                    if client_data.contact_rol:
                        contact.rol = client_data.contact_rol
            else:
                # Crear nuevo contacto
                new_contact = Contact(
                    name=client_data.contact_name,
                    phone=client_data.contact_phone,
                    email=client_data.contact_email,
                    company=client.name,
                    rol=client_data.contact_rol,
                    is_client=True
                )
                db.add(new_contact)
                db.flush()
                client.contact_id = new_contact.contact_id

        # Actualizar campos del cliente (excluyendo los campos de contacto)
        update_data = client_data.model_dump(
            exclude_unset=True,
            exclude={'contact_name', 'contact_phone', 'contact_email', 'contact_rol'}
        )

        for field, value in update_data.items():
            setattr(client, field, value)

        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete_client(db: Session, client_id: int) -> bool:
        client = db.query(Client).filter(Client.client_id == client_id).first()

        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        client.is_active = False
        db.commit()
        return True


class BranchService:

    @staticmethod
    def create_branch(db: Session, branch_data: BranchCreate) -> Branch:

        client = db.query(Client).filter(Client.client_id == branch_data.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        new_branch = Branch(
            client_id=branch_data.client_id,
            name=branch_data.name,
            is_main=branch_data.is_main,
            address=branch_data.address,
            colonia=branch_data.colonia,
            zip_code=branch_data.zip_code,
            city=branch_data.city
        )
        db.add(new_branch)
        db.flush()

        # Crea areas si vienen
        if branch_data.areas:
            for area_name in branch_data.areas:
                db.add(Area(branch_id=new_branch.branch_id, name=area_name))

        db.commit()
        db.refresh(new_branch)
        return new_branch

    @staticmethod
    def get_branch_by_id(db: Session, branch_id: int) -> Optional[Branch]:
        return db.query(Branch).options(
            joinedload(Branch.areas)
        ).filter(Branch.branch_id == branch_id).first()

    @staticmethod
    def get_branches_by_client(db: Session, client_id: int) -> List[Branch]:
        return db.query(Branch).options(
            joinedload(Branch.areas)
        ).filter(Branch.client_id == client_id).all()

    @staticmethod
    def update_branch(db: Session, branch_id: int, branch_data: BranchUpdate) -> Branch:
        branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()

        if not branch:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")

        update_data = branch_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(branch, field, value)

        db.commit()
        db.refresh(branch)
        return branch

    @staticmethod
    def delete_branch(db: Session, branch_id: int) -> bool:
        branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()

        if not branch:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")

        db.delete(branch)
        db.commit()
        return True

class AreaService:

    @staticmethod
    def create_area(db: Session, area_data: AreaCreate) -> Area:

        branch = db.query(Branch).filter(Branch.branch_id == area_data.branch_id).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")

        new_area = Area(
            branch_id=area_data.branch_id,
            name=area_data.name
        )
        db.add(new_area)
        db.commit()
        db.refresh(new_area)
        return new_area

    @staticmethod
    def get_area_by_id(db: Session, area_id: int) -> Optional[Area]:
        return db.query(Area).filter(Area.area_id == area_id).first()

    @staticmethod
    def get_areas_by_branch(db: Session, branch_id: int) -> List[Area]:
        return db.query(Area).filter(Area.branch_id == branch_id).all()

    @staticmethod
    def update_area(db: Session, area_id: int, area_data: AreaUpdate) -> Area:
        area = db.query(Area).filter(Area.area_id == area_id).first()

        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")

        update_data = area_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(area, field, value)

        db.commit()
        db.refresh(area)
        return area

    @staticmethod
    def delete_area(db: Session, area_id: int) -> bool:
        area = db.query(Area).filter(Area.area_id == area_id).first()

        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")

        db.delete(area)
        db.commit()
        return True

