from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def update_inventory_usage(
    db: Session, rec_id: int,
    Date=None,
    month=None,
    year=None,
    category=None,
    client_name=None,
    start_time=None,
    end_time=None,
    meridiem=None,
    chemical_use=None,
    actual_chemical_used=None
    ):
    try:
        record = db.query(InventoryRecord).get(rec_id)
        
        if not record:
            return None
        
        if Date:
            record.date = Date
            
        if month:
            record.month = month
            
        if year:
            record.year = year
            
        if category:
            record.category = category
        
        if client_name:
            record.client_name = client_name
            
        if start_time:
            record.start_time = start_time
        
        if end_time:
            record.end_time = end_time
            
        if meridiem:
            record.meridiem = meridiem
            
        if chemical_use is not None:
            record.chemicals_use = actual_chemical_used
            
        if actual_chemical_used is not None:
            record.actual_chemicals_used = actual_chemical_used
        
        db.commit()
        db.refresh(record) 
        
        return record
    except Exception as e:
        return print(f"Updating inventory usage unsuccesfull: {e}")
     
   