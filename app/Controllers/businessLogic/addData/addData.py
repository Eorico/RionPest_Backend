from datetime import time
from app.Models.record.inventoryRecord import InventoryRecord, ChemicalUsed, ActualChemicalUsed
from app.Models.admin.admin import Admin
from sqlalchemy.orm import Session, joinedload 

def get_add_inventory_record(
    db: Session, admin_username: str, date: int, 
    month: int, year: int, category: str,
    client_name: str, start_time: time,
    end_time: time, start_meridiem: str, end_meridiem: str, chemical_use: list,
    actual_chemical_used: list
    ):
    
    admin = db.query(Admin).filter(Admin.username == admin_username).first()
    if not admin:
        raise Exception(f"Admin '{admin_username}' not found in database.")
    
    new_record = InventoryRecord(
        admin_id=admin.id,
        admin_under=admin,
        date=date,
        month=month,
        year=year,
        category=category,
        client_name=client_name,
        start_time=start_time,
        end_time=end_time,
        start_meridiem=start_meridiem,
        end_meridiem=end_meridiem
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    for item in chemical_use:
        entry = ChemicalUsed(
            inventory_id=new_record.id,
            chemical_name=item.chemical_name,
            quantity=item.quantity,
            remarks=getattr(item, 'remarks', None)
        )    
        db.add(entry)
        
    for item in actual_chemical_used:
        entry = ActualChemicalUsed(
            inventory_id=new_record.id,
            actual_chemicals_name=item.chemical_name,
            quantity=item.quantity,
            remarks=getattr(item, 'remarks', None)
        )    
        db.add(entry)
        
    db.commit()
    final_record = db.query(InventoryRecord).options(
        joinedload(InventoryRecord.chemicals_use),
        joinedload(InventoryRecord.actual_chemicals_used)
    ).filter(InventoryRecord.id == new_record.id).first()

    return final_record

    