from fastapi import FastAPI
from app.Routes.inventory import inventoryRoutes
from app.Database.database import Base, engine

#tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pest Control Inventory System")

app.include_router(inventoryRoutes)