from sqlalchemy.orm import Session
from datetime import date
from app.Controllers.businessLogic.addData.addData import getAddInventoryRecord
from app.Controllers.businessLogic.readData.readData import fetchAllRecords
from app.Controllers.businessLogic.deleteData.deleteData import deleteInventoryRecord
from app.Controllers.businessLogic.generateReport.generateReport import generateReport
from app.Controllers.businessLogic.updateData.updateData import updateInventoryUsage

class InventoryController:
    def __init__(self, db: Session):
        self.db = db
        
    def addRecord(
        self, techName: str, chemName: str,
        usageLt: float, recDate: date
    ):
        return getAddInventoryRecord(
            self.db, techName, chemName, usageLt, recDate,
        )
        
    def getRecord(self):
        return fetchAllRecords(self.db)
    
    def updateRecord(self, recId: int, usageLt: float):
        return updateInventoryUsage(self.db, recId, usageLt)
    
    def deleteRecord(self, recId: int):
        return deleteInventoryRecord(self.db, recId)
    
    def getReport(self, period: str):
        return generateReport(self.db, period)