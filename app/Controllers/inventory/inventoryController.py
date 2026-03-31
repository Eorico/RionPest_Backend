from sqlalchemy.orm import Session
from datetime import date, time
from app.Controllers.businessLogic.addData.addData import get_add_inventory_record
from app.Controllers.businessLogic.readData.readData import fetch_all_records
from app.Controllers.businessLogic.deleteData.deleteData import delete_inventory_record
from app.Controllers.businessLogic.generateReport.generateReport import generate_report
from app.Controllers.businessLogic.updateData.updateData import update_inventory_usage

class InventoryController:
    def __init__(self, db: Session):
        self.db = db
        
    def add_record(
        self, Date: date, client_name: str,
        start_time: time, end_time: time, chemical_name: str,
        actual_chemical_on_hand: float
    ):
        return get_add_inventory_record(
            self.db, Date, client_name, start_time, end_time,
            chemical_name, actual_chemical_on_hand,
        )
        
    def get_record(self):
        return fetch_all_records(self.db)
    
    def update_record(self, rec_id: int, actual_chemical_on_hand: float):
        return update_inventory_usage(self.db, rec_id, actual_chemical_on_hand)
    
    def delete_record(self, rec_id: int):
        return delete_inventory_record(self.db, rec_id)
    
    def get_report(self, period: str):
        return generate_report(self.db, period)