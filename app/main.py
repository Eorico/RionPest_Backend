from fastapi import FastAPI
from app.Routes.inventory.inventoryRoutes import router
from app.Database.database import base, engine

#tables
base.metadata.create_all(bind=engine)

app = FastAPI(title="Pest Control Inventory System")

app.include_router(router)