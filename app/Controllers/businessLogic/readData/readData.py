from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def fetchAllRecords(db: Session):
    return db.query(InventoryRecord).all()
