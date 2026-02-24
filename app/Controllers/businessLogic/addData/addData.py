from datetime import date, time
from app.Models.record.inventoryRecord import InventoryRecord
from sqlalchemy.orm import Session 

def getAddInventoryRecord(
    db: Session, treatmentDate: date, 
    clientName: str, startTime: time,
    endTime: time, chemicalName: str,
    actualOnHand: float
    ):
    
    record = InventoryRecord(
        treatmentDate=treatmentDate,
        clientName=clientName,
        startTime=startTime,
        endTime=endTime,
        chemicalName=chemicalName,
        actualChemicalOnhand=actualOnHand
    )
    db.add(record)
    db.commit()
    db.refresh()
    return record

    