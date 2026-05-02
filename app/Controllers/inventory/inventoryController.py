from sqlalchemy.orm import Session
from datetime import time
from app.Controllers.businessLogic.addData.addData import get_add_inventory_record
from app.Controllers.businessLogic.readData.readData import fetch_all_records
from app.Controllers.businessLogic.generateReport.generateReport import generate_report
from app.Controllers.businessLogic.updateData.updateData import update_inventory_usage
from app.Controllers.businessLogic.deleteData.deleteData import (
    soft_delete, permanent_delete, restore_deleted_record
)

from app.schemas.InventUpdate.RecordUpdate import InvRecUpdate

class InventoryController:
    def __init__(self, db: Session):
        self.db = db
        
    def add_record(
        self, admin_under: str, date: int, month: int, year: int, category: str,client_name: str,
        start_time: time, end_time: time, start_meridiem: str, end_meridiem: str, chemical_use: list,
        actual_chemical_used: list
    ):
        return get_add_inventory_record(
            self.db, admin_under, date, month, 
            year, category, client_name, start_time, 
            end_time, start_meridiem, end_meridiem,
            chemical_use, actual_chemical_used,
        )
        
    def get_record(self):
        return fetch_all_records(self.db)
    
    def update_record(self, rec_id: int, payload: InvRecUpdate):
        return update_inventory_usage(
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
        return generate_report(self.db, period)
    
    def hard_delete(self, rec_id: int = None, all_records: bool = None):
        return permanent_delete(self.db, rec_id=rec_id, delete_all=all_records)
    
    def move_to_recycle_bin(self, rec_id: int):
        return soft_delete(self.db, rec_id)
    
    def restore(self, rec_id: int = None, all_records: bool = False):
        return restore_deleted_record(self.db, rec_id=rec_id, restore_all=all_records)