from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def deleteInventoryRecord(db: Session, recId:int):
    record = db.query(InventoryRecord).get(recId)
    if record:
        db.delete(record)
        db.commit()
        return True
    return False