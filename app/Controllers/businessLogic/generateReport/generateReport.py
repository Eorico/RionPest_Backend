from sqlalchemy.orm import Session 
from datetime import date, timedelta
from app.Models.record.inventoryRecord import InventoryRecord

def generateReport(db: Session, period: str):
    today = date.today()
    query = db.query(InventoryRecord)
    
    if period == "week":
        start = today - timedelta(days=7)
        query = query.filter(InventoryRecord.recordDate >= start)
        
    elif period == "month":
        query = query.filter(
            InventoryRecord.recordDate.month == today.month,
            InventoryRecord.recordDate.year == today.year
        )
    
    elif period == "year":
        query = query.filter(InventoryRecord.recordDate.year == today.year)
        
    return query.all()
