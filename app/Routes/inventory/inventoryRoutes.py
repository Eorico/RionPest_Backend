from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.InventCreate.RecordCreate import InvRecCreate
from app.schemas.inventResponse.RecordRespo import InvRecRespo
from app.schemas.InventUpdate.RecordUpdate import InvRecUpdate
from app.Controllers.inventory.inventoryController import InventoryController
from app.Database.database import get_db
from app.auth.authJWTdepedency import requireRole
from app.Models.record.inventoryRecord import InventoryRecord
from app.Controllers.businessLogic.deleteData.deleteData import (
    soft_delete, permanent_delete, restore_deleted_record
)

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

class InventoryRouter:
    pass

router = APIRouter(prefix='/inventory', tags=['Inventory'])

def get_controller(db: Session = Depends(get_db)):
    return InventoryController(db)

def map_to_respo(r:InventoryRecord) -> InvRecRespo:
    return InvRecRespo(
        id=r.id,
        admin_under=r.admin_under.username if hasattr(r.admin_under, 'username') else "Unknown",
        date=r.date,
        month=r.month,
        year=r.year,
        category=r.category,
        client_name=r.client_name,
        start_time=r.start_time,
        end_time=r.end_time,
        start_meridiem=r.start_meridiem,
        end_meridiem=r.end_meridiem,
        chemical_use=r.chemicals_use,
        actual_chemical_used=r.actual_chemicals_used
    )

@router.post('/', response_model=InvRecRespo, dependencies=[Depends(requireRole(["SuperAdmin","admin"]))])
@limiter.limit("10/minute")
def add_inventory(request: Request, record: InvRecCreate, controller: InventoryController = Depends(get_controller)):
    try: 
        new_record = controller.add_record(
            record.admin_under,
            record.date, record.month,
            record.year, record.category,
            record.client_name, record.start_time, 
            record.end_time, record.start_meridiem, record.end_meridiem, 
            record.chemical_use, record.actual_chemical_used
        )
        
        if new_record is None:
            raise HTTPException(status_code=500, detail="Controller returned none")
        
        return new_record
        
    except Exception as e: 
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/', response_model=list[InvRecRespo])
@limiter.limit("30/minute")
def get_inventory(request: Request, db: Session = Depends(get_db)):
    records = db.query(InventoryRecord).filter(InventoryRecord.is_deleted == False).all()
    try:
        return [map_to_respo(r) for r in records]
    except Exception as e:
        print(f"Error: get record unsuccessfull {e}")

@router.put('/{record_id}', response_model=InvRecRespo, 
            dependencies=[Depends(requireRole(["SuperAdmin","admin"]))])
@limiter.limit("20/minute")
def update_inventory(request: Request, record_id: int, payload: InvRecUpdate, controller: InventoryController = Depends(get_controller)):
    try:
         updated = controller.update_record(record_id, payload)
         if not updated:
             raise HTTPException(status_code=404, detail="Record not found or already deleted")
         return map_to_respo(updated)
    except Exception as e:
        print(f"Error: update record unsuccessfull {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/recycle-bin', response_model=list[InvRecRespo])
def get_recycle_bin(db: Session = Depends(get_db)):
    return db.query(InventoryRecord).filter(InventoryRecord.is_deleted == True).all()

@router.delete('/{record_id}')
def move_to_bin(record_id: int, db: Session = Depends(get_db)):
    if soft_delete(db, record_id):
        return {"message": "Moved to recycle bin"}
    raise HTTPException(status_code=404, detail="Record not found")

@router.post('/restore/{record_id}')
def restore(record_id: int, db: Session = Depends(get_db)):
    restore_deleted_record(db, rec_id=record_id)
    return {"message": "Record restored"}

@router.post('/restore-all')
@limiter.limit("3/minute")
def restore_all(request: Request, db: Session = Depends(get_db)):
    restore_deleted_record(db, restore_all=True)
    return {"message": "All record restored"}

@router.delete('/permanent/{record_id}')
@limiter.limit("5/minute")
def hard_delete(request: Request, record_id: int, db: Session = Depends(get_db)):
    permanent_delete(db, rec_id=record_id)
    return {"message": "Permanently deleted"}
        
@router.get('/report/{period}', response_model=list[InvRecRespo])
def report(period: str, controller: InventoryController = Depends(get_controller)):
    if period not in ['week', 'month', 'year']:
        raise HTTPException(status_code=400, detail="Invalid period")
    records = controller.get_report(period)
    return [map_to_respo(r) for r in records]