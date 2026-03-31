from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def fetch_all_records(db: Session):
    return db.query(InventoryRecord).all()
