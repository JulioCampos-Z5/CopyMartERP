from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routers import router as user_router
from equipment.routers import router as equipment_router
from rent.routers import router as rent_router
from sale.routers import router as sale_router
from billing.routers import router as billing_router
from client.routers import router as client_router
from ticket.routers import router as ticket_router
from monthlyplan.routers import service_type_router, monthlyplan_router
from contact.routers import router as contact_router
from sparepart.routers import router as sparepart_router
from purchase.routers import router as purchase_router
from print.routers import router as print_router
from rh.routers import router as rh_router


from core.database import Base, engine

# Importar TODOS los modelos para que se registren con SQLAlchemy
from auth import models as auth_models
from client import models as client_models
from contact import models as contact_models
from equipment import models as equipment_models
from rent import models as rent_models
from sale import models as sale_models
from billing import models as billing_models
from sparepart import models as sparepart_models
from purchase import models as purchase_models
from print import models as print_models
from rh import models as rh_models
from ticket import models as ticket_models
from monthlyplan import models as monthlyplan_models

app = FastAPI(title="API de Usuarios")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api")
app.include_router(equipment_router, prefix="/api")
app.include_router(client_router, prefix="/api/clients", tags=["clients"])
app.include_router(rent_router, prefix="/api")
app.include_router(sale_router, prefix="/api")
app.include_router(billing_router, prefix="/api")
app.include_router(ticket_router, prefix="/api")
app.include_router(service_type_router, prefix="/api")
app.include_router(monthlyplan_router, prefix="/api")
app.include_router(contact_router, prefix="/api")
app.include_router(sparepart_router, prefix="/api")
app.include_router(purchase_router, prefix="/api")
app.include_router(print_router, prefix="/api")
app.include_router(rh_router, prefix="/api")



@app.get("/")
def root():
    return {"message": "Copy mart Api,  "}

Base.metadata.create_all(bind=engine)
