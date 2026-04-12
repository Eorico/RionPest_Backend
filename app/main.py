from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.Routes.inventory.inventoryRoutes import router as inventory_router
from app.Routes.admin.admin import router as admin_router
from app.Database.database import Base, engine

limiter = Limiter(key_func=get_remote_address)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pest Control Inventory System")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def health_check():
    return {"status": "online", "message": "Rion System Backend is Running"}

app.include_router(inventory_router)
app.include_router(admin_router)