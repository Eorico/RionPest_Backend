from sqlalchemy.orm import Session 
from app.Models.record.inventoryRecord import InventoryRecord

def updateInventoryUsage(
    db: Session, recId: int,
    treatmentDate=None,
    clientName=None,
    startTime=None,
    endTime=None,
    actualOnHand=None
    ):
    try:
        record = db.query(InventoryRecord).get(recId)
        
        if not record:
            return None
        
        if treatmentDate:
            record.treatmentDate = treatmentDate
        
        if clientName:
            record.clientName = clientName
            
        if startTime:
            record.startTime = startTime
        
        if endTime:
            record.endTime = endTime
            
        if actualOnHand is not None:
            record.actualChemicalOnHand = actualOnHand
        
        db.commit()
        db.refresh(record) 
        
        return record
    except Exception as e:
        return print(f"Updating inventory usage unsuccesfull: {e}")
     
   