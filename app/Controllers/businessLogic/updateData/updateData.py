from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def updateInventoryUsage(db: Session, recId: int, usageLt: float):
    record = db.query(InventoryRecord).get(recId)
    if record:
        record.usageLiters = usageLt
        db.commit()
        db.refresh(record)
    return record