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

@router.post('/', response_model=InvRecRespo, dependencies=[Depends(requireRole(["SuperAdmin","admin"]))])
def addInventory(record: InvRecCreate, controller: InventoryController = Depends(get_controller)):
    try: 
        new_record = controller.add_record(
            record.date, record.month, record.year, record.category,record.client_name, 
            record.start_time, record.end_time, record.meridiem, record.chemical_use, 
            record.actual_chemical_used
        )
        
        if new_record is None:
            raise HTTPException(status_code=500, detail="Controller returned none")
        
        return new_record
        
    except Exception as e: 
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/', response_model=list[InvRecRespo])
def get_inventory(controller: InventoryController = Depends(get_controller)):
    records = controller.get_record()
    try:
        return [
            InvRecRespo(
                id=r.id,
                date=r.date,
                month=r.month,
                year=r.year,
                category=r.category,
                client_name=r.client_name,
                start_time=r.start_time,
                end_time=r.end_time,
                meridiem=r.meridiem,
                chemical_use=r.chemicals_use,
                actual_chemical_used=r.actual_chemicals_used
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
            date=record.date,
            month=record.month,
            year=record.year,
            client_name=record.client_name,
            start_time=record.start_time,
            end_time=record.end_time,
            meridiem=record.meridiem,
            chemical_use=record.chemicals_use,
            actual_chemical_used=record.actual_chemicals_used
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
            date=r.date,
            month=r.month,
            year=r.year,
            category=r.category,
            client_name=r.client_name,
            start_time=r.start_time,
            end_time=r.end_time,
            meridiem=r.meridiem,
            chemical_use=r.chemicals_use,
            actual_chemical_used=r.actual_chemicals_used
        ) for r in records
    ]