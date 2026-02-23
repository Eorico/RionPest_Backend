from datetime import date, time
from app.Models.chemical.Chemical import Chemical
from app.Models.technician.Technician import Technician
from app.Models.record.inventoryRecord import InventoryRecord
from sqlalchemy.orm import Session 

def getAddChemical(db: Session, name: str):
    chem = db.query(Chemical).filter_by(name=name).first()
    if not chem:
        chem = Chemical(name=name)
        db.add(chem)
        db.commit()
        db.refresh(chem)
        
    return chem

def getAddInventoryRecord(
    db: Session, treatmentDate: date, 
    clientName: str, startTime: time,
    endTime: time, chemicalName: str,
    actualOnHand: float
    ):
    chem = getAddChemical(db, chemicalName)
    
    record = InventoryRecord(
        treatmentDate=treatmentDate,
        clientName=clientName,
        startTime=startTime,
        endTime=endTime,
        chemId=chem.id,
        actualChemicalOnhand=actualOnHand
    )
    db.add(record)
    db.commit()
    db.refresh()
    return record

    