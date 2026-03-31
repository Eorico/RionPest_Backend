from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def update_inventory_usage(
    db: Session, rec_id: int,
    Date=None,
    client_name=None,
    start_time=None,
    end_time=None,
    actual_chemical_on_hand=None
    ):
    try:
        record = db.query(InventoryRecord).get(rec_id)
        
        if not record:
            return None
        
        if Date:
            record.date = Date
        
        if client_name:
            record.client_name = client_name
            
        if start_time:
            record.start_time = start_time
        
        if end_time:
            record.end_time = end_time
            
        if actual_chemical_on_hand is not None:
            record.actual_chemical_on_hand = actual_chemical_on_hand
        
        db.commit()
        db.refresh(record) 
        
        return record
    except Exception as e:
        return print(f"Updating inventory usage unsuccesfull: {e}")
     
   