from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def delete_inventory_record(db: Session, rec_id:int):
    record = db.query(InventoryRecord).get(rec_id)
    if record:
        db.delete(record)
        db.commit()
        return True
    return False