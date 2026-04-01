from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.InventCreate.RecordCreate import InvRecCreate
from app.schemas.inventResponse.RecordRespo import InvRecRespo
from app.Controllers.inventory.inventoryController import InventoryController
from app.Database.database import get_db
from app.auth.authJWTdepedency import requireRole
from app.Models.record.inventoryRecord import InventoryRecord
from app.Controllers.businessLogic.deleteData.deleteData import (
    soft_delete, permanent_delete, restore_deleted_record
)


router = APIRouter(prefix='/inventory', tags=['Inventory'])

def get_controller(db: Session = Depends(get_db)):
    return InventoryController(db)

@router.post('/', response_model=InvRecRespo, dependencies=[Depends(requireRole(["admin"]))])
def addInventory(record: InvRecCreate, controller: InventoryController = Depends(get_controller)):
    try: 
        return controller.add_record(
            record.Date, record.client_name, 
            record.start_time, record.end_time, record.chemical_name, 
            record.actual_chemical_on_hand
        )
    except Exception as e: 
        print(f"Error: adding a product {e}")

@router.get('/', response_model=list[InvRecRespo])
def get_inventory(controller: InventoryController = Depends(get_controller)):
    records = controller.get_record()
    try:
        return [
            InvRecRespo(
                id=r.id,
                treatmentDate=r.date,
                clientName=r.client_name,
                startTime=r.start_time,
                endTime=r.end_time,
                chemicalName=r.chemical_name.name,
                actualChemicalOnHand=r.actual_chemical_on_hand
            ) for r in records
        ]
    except Exception as e:
        print(f"Error: get record unsuccessfull {e}")

@router.put('/{recordId}', response_model=InvRecRespo, dependencies=[Depends(requireRole(["admin"]))])
def update_inventory(rec_id: int, usage_lt: float, controller: InventoryController = Depends(get_controller)):
    record = controller.update_record(rec_id, usage_lt)
    try:
        if not record:
            raise HTTPException(status_code=404, detail="Recod not found!")
        return InvRecRespo(
            id=record.id,
            treatmentDate=record.date,
            clientName=record.client_name,
            startTime=record.start_time,
            endTime=record.end_time,
            chemicalName=record.chemical_name.name,
            actualChemicalOnHand=record.actual_chemical_on_hand
        )
    except Exception as e:
        print(f"Error: putting record unsuccessfull {e}")
    
@router.get('/recycle-bin', response_model=list[InvRecRespo])
def get_recycle_bin(db: Session = Depends(get_db)):
    return db.query(InventoryRecord).filter(InventoryRecord.is_deleted == True).all()

@router.delete('{recordId}')
def move_to_bin(recordId: int, db: Session = Depends(get_db)):
    if soft_delete(db, recordId):
        return {"message": "Moved to recycle bin"}
    raise HTTPException(status_code=404, detail="Record not found")

@router.post('/restore/{recordId}')
def restore(recordId: int, db: Session = Depends(get_db)):
    restore_deleted_record(db, rec_id=recordId)
    return {"message": "Record restored"}

@router.post('/restore-all')
def restore_all(db: Session = Depends(get_db)):
    restore_deleted_record(db, restore_all=True)
    return {"message": "All record restored"}

@router.delete('/permanent/{recordId}')
def hard_delete(recordId: int, db: Session = Depends(get_db)):
    permanent_delete(db, rec_id=recordId)
    return {"message": "Permanently deleted"}
        
@router.get('/report/{period}', response_model=list[InvRecRespo])
def report(period: str, controller: InventoryController = Depends(get_controller)):
    if period not in ['week', 'month', 'year']:
        raise HTTPException(status_code=400, detail="Invalid period")
    records = controller.get_report(period)
    return [
        InvRecRespo(
            id=r.id,
            treatmentDate=r.date,
            clientName=r.client_name,
            startTime=r.start_time,
            endTime=r.end_time,
            chemicalName=r.chemical_name.name,
            actualChemicalOnHand=r.actual_chemical_on_hand
        ) for r in records
    ]