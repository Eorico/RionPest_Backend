from sqlalchemy.orm import Session
from datetime import time
from app.Services.inventory.inventoryService import inventory_service

from app.Schemas.inventUpdate.RecordUpdate import InvRecUpdate

class InventoryController:
    def __init__(self, db: Session):
        self.db = db
        
    def add_record(
        self, admin_under: str, date: int, month: int, year: int, category: str,client_name: str,
        start_time: time, end_time: time, start_meridiem: str, end_meridiem: str, chemical_use: list,
        actual_chemical_used: list
    ):
        return inventory_service.create_record(
            self.db, admin_under, date, month, 
            year, category, client_name, start_time, 
            end_time, start_meridiem, end_meridiem,
            chemical_use, actual_chemical_used,
        )
        
    def get_record(self):
        return inventory_service.get_active_records(self.db)
    
    def update_record(self, rec_id: int, payload: InvRecUpdate):
        return inventory_service.update_record(
            self.db, 
            rec_id, 
            date=payload.date,
            month=payload.month,
            year=payload.year,
            category=payload.category,
            client_name=payload.client_name,
            start_time=payload.start_time,
            end_time=payload.end_time,
            start_meridiem=payload.start_meridiem,
            end_meridiem=payload.end_meridiem,
            chemical_use=payload.chemical_use,
            actual_chemical_used=payload.actual_chemical_used
        )
    
    def get_report(self, period: str):
        return inventory_service.generate_report(self.db, period)
    
    def hard_delete(self, rec_id: int = None, all_records: bool = None):
        return inventory_service.permanent_delete(self.db, rec_id=rec_id, delete_all=all_records)
    
    def move_to_recycle_bin(self, rec_id: int):
        return inventory_service.soft_delete(self.db, rec_id)
    
    def restore(self, rec_id: int = None, all_records: bool = False):
        return inventory_service.restore_deleted_record(self.db, rec_id=rec_id, restore_all=all_records)