from fastapi import FastAPI
from app.Routes.inventory.inventoryRoutes import router as inventory_router
from app.Routes.admin.admin import router as admin_router
from app.Database.database import Base, engine

#tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pest Control Inventory System")

@app.get("/")
def health_check():
    return {"status": "online", "message": "Rion System Backend is Running"}

app.include_router(inventory_router)
app.include_router(admin_router)