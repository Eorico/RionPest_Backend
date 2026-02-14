from datetime import date
from app.Models.chemical.Chemical import Chemical
from app.Models.technician.Technician import Technician
from app.Models.record.inventoryRecord import InventoryRecord
from sqlalchemy.orm import Session 

def getAddTechnician(db: Session, name: str):
    tech = db.query(Technician).filter_by(name=name).first()
    if not tech:
        tech = Technician(name=name)
        db.add(tech)
        db.commit()
        db.refresh(tech)
        
    return tech

def getAddChemical(db: Session, name: str):
    chem = db.query(Chemical).filter_by(name=name).first()
    if not chem:
        chem = Chemical(name=name)
        db.add(chem)
        db.commit()
        db.refresh(chem)
        
    return chem

def getAddInventoryRecord(
    db: Session, techName: str, 
    chemName: str, usageLt: float,
    recDate: date
    ):
    tech = getAddTechnician(db, techName)
    chem = getAddChemical(db, chemName)
    
    record = InventoryRecord(
        techId=tech.id,
        chemId=chem.id,
        usageLt=usageLt,
        recDate=recDate
    )
    db.add(record)
    db.commit()
    db.refresh()
    return record

    