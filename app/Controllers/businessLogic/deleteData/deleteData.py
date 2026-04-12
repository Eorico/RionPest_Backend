from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

# delete records must go to the recycle bin
def soft_delete(db: Session, rec_id: int):
    record = db.get(InventoryRecord, rec_id)
    if record:
        record.is_deleted = True
        db.commit()
        return True
    return False
# permanently delete
def permanent_delete(db: Session, rec_id: int = None, delete_all: bool = False):
    if delete_all:
        records = db.query(InventoryRecord).filter(InventoryRecord.is_deleted == True).all()
        for record in records:
            db.delete(record)
    else:
        record = db.query(InventoryRecord).filter(
            InventoryRecord.id == rec_id,
            InventoryRecord.is_deleted == True
        ).first()
        
        if record:
            db.delete(record)
        else:
            return False, "Record not found"
        
    db.commit()
    return True, "Permanently deleted"
# restore deleted records
def restore_deleted_record(db: Session, rec_id: int = None, restore_all: bool = False):
    if restore_all:
        db.query(InventoryRecord).filter(InventoryRecord.is_deleted == True).update({"is_deleted": False})
    else:
        record = db.query(InventoryRecord).filter(InventoryRecord.id == rec_id, InventoryRecord.is_deleted == True).first()
        if record:
            record.is_deleted = False
    db.commit()
    return True