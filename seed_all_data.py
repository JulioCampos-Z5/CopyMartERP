"""
Script para generar datos de ejemplo completos en la base de datos
Incluye: Contactos, Clientes, Sucursales, Áreas, Ventas, Rentas, Equipos, Refacciones
Ejecutar con: python seed_all_data.py
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.equipment.models import Brand, Supplier, Equipment, TypeColor, LocationStatus
from app.client.models import Client, Branch, Area
from app.contact.models import Contact
from app.sale.models import Sale, SaleStatus
from app.rent.models import Rent, ContractStatus
from app.sparepart.models import Sparepart
from app.purchase.models import Purchase, PurchaseStatus, PurchaseType
from app.billing.models import Billing, BillingStatus, BillingType
from datetime import date, timedelta
import random

def create_sample_data():
    db = SessionLocal()
    
    try:
        # ============ CONTACTOS ============
        print("📞 Creando contactos...")
        contacts_data = [
            {"name": "Juan Pérez", "phone": "555-1234", "email": "juan.perez@empresa.com", "company": "Acme Corp", "rol": "Gerente General"},
            {"name": "María González", "phone": "555-2345", "email": "maria.gonzalez@techsol.com", "company": "TechSolutions", "rol": "Directora de TI"},
            {"name": "Carlos Rodríguez", "phone": "555-3456", "email": "carlos.rodriguez@innovate.com", "company": "Innovate SA", "rol": "Jefe de Compras"},
            {"name": "Ana Martínez", "phone": "555-4567", "email": "ana.martinez@global.com", "company": "Global Services", "rol": "Coordinadora de Operaciones"},
            {"name": "Luis Hernández", "phone": "555-5678", "email": "luis.hernandez@comercial.com", "company": "Comercial del Norte", "rol": "Gerente de Sucursal"},
            {"name": "Laura Sánchez", "phone": "555-6789", "email": "laura.sanchez@sistemas.com", "company": "Sistemas Integrales", "rol": "Administradora"},
            {"name": "Roberto Torres", "phone": "555-7890", "email": "roberto.torres@office.com", "company": "Office Solutions", "rol": "Director Comercial"},
            {"name": "Patricia Flores", "phone": "555-8901", "email": "patricia.flores@digital.com", "company": "Digital Print", "rol": "Jefa de Producción"},
            {"name": "Fernando Díaz", "phone": "555-9012", "email": "fernando.diaz@consulting.com", "company": "Consulting Group", "rol": "Consultor Senior"},
            {"name": "Isabel Ramírez", "phone": "555-0123", "email": "isabel.ramirez@finance.com", "company": "Finance Corp", "rol": "Directora Financiera"}
        ]
        
        contacts = []
        for contact_data in contacts_data:
            existing = db.query(Contact).filter(Contact.email == contact_data["email"]).first()
            if not existing:
                contact = Contact(**contact_data)
                db.add(contact)
                db.flush()
                contacts.append(contact)
                print(f"  ✓ Contacto: {contact.name}")
            else:
                contacts.append(existing)
        
        db.commit()
        
        # ============ CLIENTES ============
        print("\n👥 Creando clientes...")
        clients_data = [
            {
                "name": "Acme Corporation SA de CV",
                "comercial_name": "Acme Corp",
                "rfc": "ACM120815AB1",
                "address": "Av. Insurgentes Sur 1234",
                "colonia": "Del Valle",
                "zip_code": "03100",
                "city": "Ciudad de México",
                "contact_id": contacts[0].contact_id if len(contacts) > 0 else None
            },
            {
                "name": "TechSolutions México SA",
                "comercial_name": "TechSolutions",
                "rfc": "TSM150920CD2",
                "address": "Blvd. Díaz Ordaz 567",
                "colonia": "Santa María",
                "zip_code": "64650",
                "city": "Monterrey",
                "contact_id": contacts[1].contact_id if len(contacts) > 1 else None
            },
            {
                "name": "Innovate SA de CV",
                "comercial_name": "Innovate",
                "rfc": "INN180315EF3",
                "address": "Av. Chapultepec 890",
                "colonia": "Juárez",
                "zip_code": "06600",
                "city": "Ciudad de México",
                "contact_id": contacts[2].contact_id if len(contacts) > 2 else None
            },
            {
                "name": "Global Services International",
                "comercial_name": "Global Services",
                "rfc": "GSI190710GH4",
                "address": "Av. Constitución 456",
                "colonia": "Centro",
                "zip_code": "44100",
                "city": "Guadalajara",
                "contact_id": contacts[3].contact_id if len(contacts) > 3 else None
            },
            {
                "name": "Comercial del Norte SA",
                "comercial_name": "Comercial Norte",
                "rfc": "CDN200215IJ5",
                "address": "Calzada del Valle 234",
                "colonia": "Del Valle",
                "zip_code": "66220",
                "city": "San Pedro Garza García",
                "contact_id": contacts[4].contact_id if len(contacts) > 4 else None
            },
            {
                "name": "Sistemas Integrales SA de CV",
                "comercial_name": "Sistemas Integrales",
                "rfc": "SIS210512KL6",
                "address": "Paseo de la Reforma 789",
                "colonia": "Polanco",
                "zip_code": "11560",
                "city": "Ciudad de México",
                "contact_id": contacts[5].contact_id if len(contacts) > 5 else None
            },
            {
                "name": "Office Solutions México",
                "comercial_name": "Office Solutions",
                "rfc": "OSM220815MN7",
                "address": "Av. Universidad 321",
                "colonia": "Copilco",
                "zip_code": "04360",
                "city": "Ciudad de México",
                "contact_id": contacts[6].contact_id if len(contacts) > 6 else None
            },
            {
                "name": "Digital Print SA",
                "comercial_name": "Digital Print",
                "rfc": "DPR230920OP8",
                "address": "Calle Industria 567",
                "colonia": "Industrial",
                "zip_code": "45150",
                "city": "Zapopan",
                "contact_id": contacts[7].contact_id if len(contacts) > 7 else None
            }
        ]
        
        clients = []
        for client_data in clients_data:
            existing = db.query(Client).filter(Client.rfc == client_data["rfc"]).first()
            if not existing:
                client = Client(**client_data)
                db.add(client)
                db.flush()
                clients.append(client)
                print(f"  ✓ Cliente: {client.comercial_name}")
            else:
                clients.append(existing)
        
        db.commit()
        
        # ============ SUCURSALES Y ÁREAS ============
        print("\n🏢 Creando sucursales y áreas...")
        for i, client in enumerate(clients):
            # Sucursal principal
            branch = Branch(
                client_id=client.client_id,
                is_main=True,
                name="Oficina Principal",
                address=client.address,
                colonia=client.colonia,
                zip_code=client.zip_code,
                city=client.city
            )
            db.add(branch)
            db.flush()
            print(f"  ✓ Sucursal: {branch.name} - {client.comercial_name}")
            
            # Áreas para sucursal principal
            areas_names = ["Administración", "Contabilidad", "Recursos Humanos", "Ventas", "Operaciones"]
            for area_name in areas_names[:random.randint(2, 4)]:
                area = Area(
                    branch_id=branch.branch_id,
                    name=area_name
                )
                db.add(area)
        
        db.commit()
        
        # ============ MARCAS ============
        print("\n🏷️ Creando marcas...")
        brands_data = [
            {"name": "Canon", "prefix": "CAN"},
            {"name": "HP", "prefix": "HP"},
            {"name": "Xerox", "prefix": "XER"},
            {"name": "Ricoh", "prefix": "RIC"},
            {"name": "Konica Minolta", "prefix": "KM"},
            {"name": "Brother", "prefix": "BRO"},
            {"name": "Epson", "prefix": "EPS"},
            {"name": "Samsung", "prefix": "SAM"}
        ]
        
        brands = []
        for brand_data in brands_data:
            existing = db.query(Brand).filter(Brand.name == brand_data["name"]).first()
            if not existing:
                brand = Brand(**brand_data)
                db.add(brand)
                db.flush()
                brands.append(brand)
                print(f"  ✓ Marca: {brand.name}")
            else:
                brands.append(existing)
        
        db.commit()
        
        # ============ PROVEEDORES ============
        print("\n📦 Creando proveedores...")
        suppliers_data = [
            {"name": "Distribuidora TecnoOffice"},
            {"name": "Suministros Industriales SA"},
            {"name": "ImportMex"},
            {"name": "Global Office Solutions"},
            {"name": "Proveedora Nacional"}
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            existing = db.query(Supplier).filter(Supplier.name == supplier_data["name"]).first()
            if not existing:
                supplier = Supplier(**supplier_data)
                db.add(supplier)
                db.flush()
                suppliers.append(supplier)
                print(f"  ✓ Proveedor: {supplier.name}")
            else:
                suppliers.append(existing)
        
        db.commit()
        
        # ============ EQUIPOS ============
        print("\n🖨️ Creando equipos...")
        equipments_data = [
            {"brand_id": brands[0].brand_id, "model": "imageRUNNER ADVANCE C5535i", "serie": "FKG12345", "model_toner": "C-EXV49", "type": TypeColor.COLOR, "supplier_id": suppliers[0].supplier_id, "cost": 125000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[0].brand_id, "model": "imageRUNNER 2525i", "serie": "FKG12346", "model_toner": "C-EXV33", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[0].supplier_id, "cost": 45000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[0].brand_id, "model": "imageRUNNER C3025i", "serie": "FKG12347", "model_toner": "C-EXV54", "type": TypeColor.COLOR, "supplier_id": suppliers[0].supplier_id, "cost": 85000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[1].brand_id, "model": "LaserJet Pro MFP M428fdw", "serie": "VNB5Q12345", "model_toner": "CF259A", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[1].supplier_id, "cost": 15000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[1].brand_id, "model": "Color LaserJet Pro M479fdw", "serie": "VNB5Q12346", "model_toner": "CF410A", "type": TypeColor.COLOR, "supplier_id": suppliers[1].supplier_id, "cost": 22000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[1].brand_id, "model": "LaserJet Enterprise M607dn", "serie": "VNB5Q12347", "model_toner": "CF237A", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[1].supplier_id, "cost": 28000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[2].brand_id, "model": "VersaLink C405", "serie": "XER123456", "model_toner": "106R03532", "type": TypeColor.COLOR, "supplier_id": suppliers[2].supplier_id, "cost": 35000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[2].brand_id, "model": "WorkCentre 3335", "serie": "XER123457", "model_toner": "106R03621", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[2].supplier_id, "cost": 12000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[2].brand_id, "model": "VersaLink B405", "serie": "XER123458", "model_toner": "106R03585", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[2].supplier_id, "cost": 18000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[3].brand_id, "model": "MP C3004ex", "serie": "RIC123456", "model_toner": "841817", "type": TypeColor.COLOR, "supplier_id": suppliers[3].supplier_id, "cost": 65000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[3].brand_id, "model": "MP 305+", "serie": "RIC123457", "model_toner": "841769", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[3].supplier_id, "cost": 9500.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[4].brand_id, "model": "bizhub C258", "serie": "KM123456", "model_toner": "TN-324K", "type": TypeColor.COLOR, "supplier_id": suppliers[3].supplier_id, "cost": 55000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[4].brand_id, "model": "bizhub 4050", "serie": "KM123457", "model_toner": "TN-512", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[3].supplier_id, "cost": 18000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[4].brand_id, "model": "bizhub C368", "serie": "KM123458", "model_toner": "TN-328K", "type": TypeColor.COLOR, "supplier_id": suppliers[3].supplier_id, "cost": 95000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[5].brand_id, "model": "MFC-L5900DW", "serie": "BRO123456", "model_toner": "TN-880", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[4].supplier_id, "cost": 8500.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[6].brand_id, "model": "WorkForce Pro WF-C5790", "serie": "EPS123456", "model_toner": "T9451", "type": TypeColor.COLOR, "supplier_id": suppliers[4].supplier_id, "cost": 16000.00, "location_status": LocationStatus.BODEGA},
            {"brand_id": brands[7].brand_id, "model": "ProXpress M4020ND", "serie": "SAM123456", "model_toner": "MLT-D203L", "type": TypeColor.MONOCROMO, "supplier_id": suppliers[0].supplier_id, "cost": 7500.00, "location_status": LocationStatus.BODEGA}
        ]
        
        equipments = []
        for eq_data in equipments_data:
            existing = db.query(Equipment).filter(Equipment.serie == eq_data["serie"]).first()
            if not existing:
                equipment = Equipment(**eq_data, invoice=f"FAC-2024-{len(equipments)+1:03d}")
                db.add(equipment)
                db.flush()
                equipments.append(equipment)
                print(f"  ✓ Equipo: {equipment.model}")
            else:
                equipments.append(existing)
        
        db.commit()
        
        # ============ VENTAS ============
        print("\n💰 Creando ventas...")
        if len(clients) > 0 and len(equipments) >= 5:
            sales_data = [
                {
                    "client_id": clients[0].client_id,
                    "item_id": equipments[0].item_id,
                    "sale_price": 145000.00,
                    "sale_status": SaleStatus.ENTREGADA,
                    "invoice_number": "V-2024-001",
                    "is_foreign": False
                },
                {
                    "client_id": clients[1].client_id,
                    "item_id": equipments[1].item_id,
                    "sale_price": 52000.00,
                    "sale_status": SaleStatus.CONFIRMADA,
                    "invoice_number": "V-2024-002",
                    "is_foreign": False
                },
                {
                    "client_id": clients[2].client_id,
                    "item_id": equipments[2].item_id,
                    "sale_price": 95000.00,
                    "sale_status": SaleStatus.PENDIENTE,
                    "invoice_number": None,
                    "is_foreign": True
                },
                {
                    "client_id": clients[3].client_id,
                    "item_id": equipments[3].item_id,
                    "sale_price": 18500.00,
                    "sale_status": SaleStatus.ENTREGADA,
                    "invoice_number": "V-2024-003",
                    "is_foreign": False
                },
                {
                    "client_id": clients[4].client_id,
                    "item_id": equipments[7].item_id,
                    "sale_price": 14000.00,
                    "sale_status": SaleStatus.CONFIRMADA,
                    "invoice_number": "V-2024-004",
                    "is_foreign": False
                }
            ]
            
            for sale_data in sales_data:
                # Evitar duplicados por invoice_number si existe, o por (client_id, item_id) si no hay factura
                exists_q = db.query(Sale).filter(Sale.client_id == sale_data["client_id"], Sale.item_id == sale_data["item_id"])
                if sale_data.get("invoice_number"):
                    exists_q = db.query(Sale).filter(Sale.invoice_number == sale_data["invoice_number"]) 
                if exists_q.first():
                    continue
                sale = Sale(**sale_data)
                db.add(sale)
                # Actualizar estado del equipo
                equip = db.query(Equipment).filter(Equipment.item_id == sale_data["item_id"]).first()
                if equip and sale_data["sale_status"] == SaleStatus.ENTREGADA:
                    equip.location_status = LocationStatus.VENDIDO
                print(f"  ✓ Venta: {sale.invoice_number or 'Sin factura'}")
            
            db.commit()
        
        # ============ RENTAS ============
        print("\n📅 Creando rentas...")
        if len(clients) > 2 and len(equipments) >= 12:
            rents_data = [
                {
                    "client_id": clients[0].client_id,
                    "item_id": equipments[4].item_id,
                    "rent": 3500.00,
                    "contract_status": ContractStatus.VIGENTE,
                    "contract_number": "R-2024-001",
                    "is_foreign": False
                },
                {
                    "client_id": clients[1].client_id,
                    "item_id": equipments[5].item_id,
                    "rent": 4200.00,
                    "contract_status": ContractStatus.VIGENTE,
                    "contract_number": "R-2024-002",
                    "is_foreign": False
                },
                {
                    "client_id": clients[3].client_id,
                    "item_id": equipments[6].item_id,
                    "rent": 2800.00,
                    "contract_status": ContractStatus.PENDIENTE,
                    "contract_number": "R-2024-003",
                    "is_foreign": True
                },
                {
                    "client_id": clients[5].client_id,
                    "item_id": equipments[9].item_id,
                    "rent": 7500.00,
                    "contract_status": ContractStatus.VIGENTE,
                    "contract_number": "R-2024-004",
                    "is_foreign": False
                },
                {
                    "client_id": clients[6].client_id,
                    "item_id": equipments[11].item_id,
                    "rent": 6200.00,
                    "contract_status": ContractStatus.VIGENTE,
                    "contract_number": "R-2024-005",
                    "is_foreign": False
                },
                {
                    "client_id": clients[7].client_id,
                    "item_id": equipments[14].item_id,
                    "rent": 1800.00,
                    "contract_status": ContractStatus.SIN_FIRMAR,
                    "contract_number": "R-2024-006",
                    "is_foreign": False
                }
            ]
            
            for rent_data in rents_data:
                exists_q = db.query(Rent)
                if rent_data.get("contract_number"):
                    exists_q = exists_q.filter(Rent.contract_number == rent_data["contract_number"]) 
                else:
                    exists_q = exists_q.filter(Rent.client_id == rent_data["client_id"], Rent.item_id == rent_data["item_id"]) 
                if exists_q.first():
                    continue
                rent = Rent(**rent_data)
                db.add(rent)
                # Actualizar estado del equipo
                equip = db.query(Equipment).filter(Equipment.item_id == rent_data["item_id"]).first()
                if equip and rent_data["contract_status"] == ContractStatus.VIGENTE:
                    equip.location_status = LocationStatus.ASIGNADO
                print(f"  ✓ Renta: {rent.contract_number}")
            
            db.commit()
        
        # ============ REFACCIONES ============
        print("\n🔧 Creando refacciones...")
        spareparts_data = [
            {"code": "TNR-C-EXV49-K", "name": "Toner Canon C-EXV49 Negro", "color": "K", "brand": "Canon", "equipment": "imageRUNNER ADVANCE C5535i", "supplier": "Canon México", "description": "Toner original negro de alto rendimiento"},
            {"code": "TNR-C-EXV49-C", "name": "Toner Canon C-EXV49 Cyan", "color": "C", "brand": "Canon", "equipment": "imageRUNNER ADVANCE C5535i", "supplier": "Canon México", "description": "Toner original cyan"},
            {"code": "TNR-C-EXV49-M", "name": "Toner Canon C-EXV49 Magenta", "color": "M", "brand": "Canon", "equipment": "imageRUNNER ADVANCE C5535i", "supplier": "Canon México", "description": "Toner original magenta"},
            {"code": "TNR-C-EXV49-Y", "name": "Toner Canon C-EXV49 Amarillo", "color": "Y", "brand": "Canon", "equipment": "imageRUNNER ADVANCE C5535i", "supplier": "Canon México", "description": "Toner original amarillo"},
            {"code": "TNR-C-EXV33", "name": "Toner Canon C-EXV33 Negro", "color": "K", "brand": "Canon", "equipment": "imageRUNNER 2525i", "supplier": "Canon México", "description": "Toner monocromo de alto rendimiento"},
            {"code": "TNR-CF259A", "name": "Toner HP 59A Negro", "color": "K", "brand": "HP", "equipment": "LaserJet Pro MFP M428fdw", "supplier": "HP Inc.", "description": "Toner original HP 59A"},
            {"code": "TNR-CF410A-SET", "name": "Set Toner HP 410A Color", "color": "COLOR", "brand": "HP", "equipment": "Color LaserJet Pro M479fdw", "supplier": "HP Inc.", "description": "Set completo de 4 colores"},
            {"code": "TNR-106R03532", "name": "Toner Xerox 106R03532 Negro", "color": "K", "brand": "Xerox", "equipment": "VersaLink C405", "supplier": "Xerox Mexicana", "description": "Toner original Xerox"},
            {"code": "TNR-106R03621", "name": "Toner Xerox 106R03621", "color": "K", "brand": "Xerox", "equipment": "WorkCentre 3335", "supplier": "Xerox Mexicana", "description": "Toner monocromo estándar"},
            {"code": "TNR-841817", "name": "Toner Ricoh MP C3004ex Negro", "color": "K", "brand": "Ricoh", "equipment": "MP C3004ex", "supplier": "Ricoh México", "description": "Toner negro original"},
            {"code": "TNR-TN324K", "name": "Toner Konica Minolta TN-324 Negro", "color": "K", "brand": "Konica Minolta", "equipment": "bizhub C258", "supplier": "Konica Minolta", "description": "Toner negro de alto rendimiento"},
            {"code": "TNR-TN324C", "name": "Toner Konica Minolta TN-324 Cyan", "color": "C", "brand": "Konica Minolta", "equipment": "bizhub C258", "supplier": "Konica Minolta", "description": "Toner cyan original"},
            {"code": "TNR-TN324M", "name": "Toner Konica Minolta TN-324 Magenta", "color": "M", "brand": "Konica Minolta", "equipment": "bizhub C258", "supplier": "Konica Minolta", "description": "Toner magenta original"},
            {"code": "TNR-TN324Y", "name": "Toner Konica Minolta TN-324 Amarillo", "color": "Y", "brand": "Konica Minolta", "equipment": "bizhub C258", "supplier": "Konica Minolta", "description": "Toner amarillo original"},
            {"code": "DRUM-DR512", "name": "Drum Unit Konica Minolta DR-512", "color": "NA", "brand": "Konica Minolta", "equipment": "bizhub 4050", "supplier": "Konica Minolta", "description": "Unidad de imagen DR-512"},
            {"code": "TNR-TN880", "name": "Toner Brother TN-880 Super Alto Rendimiento", "color": "K", "brand": "Brother", "equipment": "MFC-L5900DW", "supplier": "Brother México", "description": "Toner de super alto rendimiento"},
            {"code": "MANT-KIT-M428", "name": "Kit de Mantenimiento HP M428", "color": "NA", "brand": "HP", "equipment": "LaserJet Pro MFP M428fdw", "supplier": "HP Inc.", "description": "Kit de mantenimiento completo"},
            {"code": "FUSER-CANON-C5535", "name": "Fusor Canon imageRUNNER C5535i", "color": "NA", "brand": "Canon", "equipment": "imageRUNNER ADVANCE C5535i", "supplier": "Canon México", "description": "Fusor original Canon"},
            {"code": "TNR-T9451", "name": "Toner Epson T9451 Negro", "color": "K", "brand": "Epson", "equipment": "WorkForce Pro WF-C5790", "supplier": "Epson México", "description": "Cartucho de tinta negro"},
            {"code": "TNR-T9452-SET", "name": "Set Tintas Epson T9452-T9454 Color", "color": "COLOR", "brand": "Epson", "equipment": "WorkForce Pro WF-C5790", "supplier": "Epson México", "description": "Set de tintas color CMY"}
        ]
        
        for part_data in spareparts_data:
            existing = db.query(Sparepart).filter(Sparepart.code == part_data["code"]).first()
            if not existing:
                sparepart = Sparepart(**part_data)
                db.add(sparepart)
                print(f"  ✓ Refacción: {sparepart.name}")
        
        db.commit()
        
        # ============ COMPRAS ============
        print("\n🛒 Creando compras...")
        # Mapear algunas refacciones por código para referencias rápidas
        parts_by_code = {p.code: p for p in db.query(Sparepart).all()}
        sample_user = contacts[0] if contacts else None

        purchases_seed = [
            {
                "sparepart_code": "TNR-C-EXV49-K",
                "name": "Compra Toner Canon Negro C-EXV49",
                "amount": 6,
                "quality": "Original",
                "justification": "Stock para clientes de color",
                "type": PurchaseType.INTERNA,
                "shipping_method": "Estafeta",
                "shipping_cost": 450.00,
                "shipping_code": "EST-2024-0001",
                "status": PurchaseStatus.EN_TRANSITO,
                "comments": "En ruta a almacén"
            },
            {
                "sparepart_code": "TNR-CF259A",
                "name": "Compra Toner HP 59A Negro",
                "amount": 10,
                "quality": "Original",
                "justification": "Reponer inventario sucursal CDMX",
                "type": PurchaseType.VENTA,
                "shipping_method": "DHL",
                "shipping_cost": 380.00,
                "shipping_code": "DHL-2024-1023",
                "status": PurchaseStatus.EN_CURSO,
                "comments": "Pendiente confirmación de proveedor"
            },
            {
                "sparepart_code": "TNR-TN324K",
                "name": "Compra Toner KM TN-324 Negro",
                "amount": 4,
                "quality": "Original",
                "justification": "Contrato de renta vigente",
                "type": PurchaseType.INTERNA,
                "shipping_method": "Paquetexpress",
                "shipping_cost": 290.00,
                "shipping_code": "PQX-2024-7777",
                "status": PurchaseStatus.SOLICITUD_GUIA_ALMACEN,
                "comments": "Solicitada guía de envío"
            },
            {
                "sparepart_code": "DRUM-DR512",
                "name": "Compra Drum Unit DR-512",
                "amount": 2,
                "quality": "Original",
                "justification": "Mantenimiento preventivo",
                "type": PurchaseType.INTERNA,
                "shipping_method": "FedEx",
                "shipping_cost": 520.00,
                "shipping_code": "FDX-2024-8890",
                "status": PurchaseStatus.FALTA_FACTURA,
                "comments": "Esperando factura del proveedor"
            },
            {
                "sparepart_code": "TNR-106R03532",
                "name": "Compra Toner Xerox 106R03532",
                "amount": 5,
                "quality": "Original",
                "justification": "Pedido para cliente corporativo",
                "type": PurchaseType.VENTA,
                "shipping_method": "Redpack",
                "shipping_cost": 310.00,
                "shipping_code": "RDP-2024-4455",
                "status": PurchaseStatus.POR_REVISAR,
                "comments": "Revisión de calidad a la llegada"
            }
        ]

        for p in purchases_seed:
            part = parts_by_code.get(p["sparepart_code"])
            if not part or not sample_user:
                continue
            exists = db.query(Purchase).filter(Purchase.shipping_code == p["shipping_code"]).first()
            if exists:
                continue
            purchase = Purchase(
                sparepart_id=part.sparepart_id,
                user_id=sample_user.contact_id,
                name=p["name"],
                amount=p["amount"],
                quality=p.get("quality"),
                justification=p.get("justification"),
                type=p["type"],
                shipping_method=p.get("shipping_method"),
                shipping_cost=p.get("shipping_cost"),
                shipping_code=p.get("shipping_code"),
                status=p["status"],
                comments=p.get("comments"),
            )
            db.add(purchase)
            print(f"  ✓ Compra: {purchase.name} ({purchase.shipping_code})")

        db.commit()

        # ============ FACTURACIÓN ============
        print("\n📄 Creando facturación...")
        # Tomar algunas ventas y rentas existentes
        sales = db.query(Sale).all()
        rents = db.query(Rent).all()

        # Seleccionar sucursal/área primera de cada cliente cuando exista
        def get_branch_area_for_client(cid):
            branch = db.query(Branch).filter(Branch.client_id == cid).first()
            area = db.query(Area).filter(Area.branch_id == branch.branch_id).first() if branch else None
            return (branch.branch_id if branch else None, area.area_id if area else None)

        today = date.today()
        billings_seed = []

        # Facturas por ventas (una pagada, una pendiente)
        if sales:
            for idx, s in enumerate(sales[:3]):
                branch_id, area_id = get_branch_area_for_client(s.client_id)
                status = BillingStatus.PAGADO if idx == 0 else BillingStatus.PENDIENTE
                billings_seed.append({
                    "billing_type": BillingType.VENTA,
                    "sale_id": s.sale_id,
                    "client_id": s.client_id,
                    "branch_id": branch_id,
                    "area_id": area_id,
                    "invoice_number": f"FV-2024-{100+idx}",
                    "amount": float(s.sale_price or 0),
                    "target_date": today,
                    "due_date": today + timedelta(days=15),
                    "payment_date": today if status == BillingStatus.PAGADO else None,
                    "status": status,
                    "follow_up": False,
                    "payment_term": 15,
                    "comment": "Factura de venta generada por seed"
                })

        # Facturas por rentas vigentes
        if rents:
            for idx, r in enumerate(rents[:4]):
                branch_id, area_id = get_branch_area_for_client(r.client_id)
                billings_seed.append({
                    "billing_type": BillingType.RENTA,
                    "rent_id": r.rent_id,
                    "client_id": r.client_id,
                    "branch_id": branch_id,
                    "area_id": area_id,
                    "invoice_number": None,
                    "amount": float(r.rent or 0),
                    "target_date": today,
                    "due_date": today + timedelta(days=10),
                    "payment_date": None,
                    "status": BillingStatus.PENDIENTE,
                    "follow_up": True if idx % 2 == 0 else False,
                    "payment_term": 10,
                    "comment": "Factura de renta mensual generada por seed"
                })

        for b in billings_seed:
            # Evitar duplicados por combinación tipo + referencia + fechas
            exists_q = db.query(Billing).filter(
                Billing.client_id == b["client_id"],
                Billing.billing_type == b["billing_type"],
                Billing.target_date == b["target_date"],
                Billing.amount == b["amount"]
            )
            if b.get("sale_id"):
                exists_q = exists_q.filter(Billing.sale_id == b["sale_id"]) 
            if b.get("rent_id"):
                exists_q = exists_q.filter(Billing.rent_id == b["rent_id"]) 
            if exists_q.first():
                continue

            billing = Billing(
                billing_type=b["billing_type"],
                rent_id=b.get("rent_id"),
                sale_id=b.get("sale_id"),
                client_id=b["client_id"],
                branch_id=b.get("branch_id"),
                area_id=b.get("area_id"),
                invoice_number=b.get("invoice_number"),
                amount=b["amount"],
                target_date=b["target_date"],
                due_date=b["due_date"],
                payment_date=b.get("payment_date"),
                status=b["status"],
                follow_up=b.get("follow_up", False),
                payment_term=b.get("payment_term"),
                payment_day=None,
                comment=b.get("comment"),
                is_active=True,
                created_by=None
            )
            db.add(billing)
            print(f"  ✓ Billing: {billing.billing_type.value} ${billing.amount} (cliente {billing.client_id})")

        db.commit()

        print("\n✅ ¡Datos de ejemplo creados exitosamente!")
        
        # Mostrar resumen
        print(f"\n📊 Resumen:")
        print(f"   Contactos: {db.query(Contact).count()}")
        print(f"   Clientes: {db.query(Client).count()}")
        print(f"   Sucursales: {db.query(Branch).count()}")
        print(f"   Áreas: {db.query(Area).count()}")
        print(f"   Marcas: {db.query(Brand).count()}")
        print(f"   Proveedores: {db.query(Supplier).count()}")
        print(f"   Equipos: {db.query(Equipment).count()}")
        print(f"   Ventas: {db.query(Sale).count()}")
        print(f"   Rentas: {db.query(Rent).count()}")
        print(f"   Refacciones: {db.query(Sparepart).count()}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de datos de ejemplo completos...\n")
    create_sample_data()
