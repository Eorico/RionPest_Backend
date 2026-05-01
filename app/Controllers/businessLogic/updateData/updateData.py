from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord, ChemicalUsed, ActualChemicalUsed
from app.Models.admin.admin import Admin

def update_inventory_usage(
    db: Session, rec_id: int,
    admin_username: str =None,
    date=None,
    month=None,
    year=None,
    category=None,
    client_name=None,
    start_time=None,
    end_time=None,
    meridiem=None,
    chemical_use: list = None,
    actual_chemical_used: list = None
    ):
    try:
        record = db.query(InventoryRecord).filter(
            InventoryRecord.id == rec_id,
            InventoryRecord.is_deleted == False
        ).first()
        
        if not record: return None
        
        if admin_username:
            admin = db.query(Admin).filter(Admin.username == admin_username).first()
            if admin:
                record.admin_id = admin.id
        
        if date: record.date = date 
        if month:record.month = month  
        if year: record.year = year    
        if category: record.category = category       
        if client_name: record.client_name = client_name  
        if start_time: record.start_time = start_time
        if end_time: record.end_time = end_time      
        if meridiem: record.meridiem = meridiem
        
        if chemical_use is not None:  
            record.chemicals.use.clear()
            record.chemicals_use = [
                ChemicalUsed(
                    chemical_name=c.chemical_name,
                    quantity=c.quantity,
                    remarks=c.remarks
                ) for c in chemical_use
            ]
            
        if actual_chemical_used is not None: 
            record.actual_chemicals_used.clear()
            record.actual_chemicals_used = [
                ActualChemicalUsed(
                    chemical_name=c.chemical_name,
                    quantity=c.quantity,
                    remarks=c.remarks
                ) for c in actual_chemical_used
            ]
        
        db.commit()
        db.refresh(record) 
        
        return record
    except Exception as e:
        db.rollback()
        print(f"Updating inventory usage unsuccesfull: {e}")
        return None