from datetime import date, time
from app.Models.record.inventoryRecord import InventoryRecord
from sqlalchemy.orm import Session 

def get_add_inventory_record(
    db: Session, Date: date, 
    client_name: str, start_time: time,
    end_time: time, chemical_name: str,
    actual_chemical_on_hand: float
    ):
    
    record = InventoryRecord(
        Date=Date,
        client_name=client_name,
        start_time=start_time,
        end_time=end_time,
        chemical_name=chemical_name,
        actual_chemical_on_hand=actual_chemical_on_hand
    )
    db.add(record)
    db.commit()
    db.refresh()
    return record

    