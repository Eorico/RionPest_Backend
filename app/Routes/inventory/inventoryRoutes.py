from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.InventCreate.RecordCreate import InvRecCreate
from app.schemas.inventResponse.RecordRespo import InvRecRespo
from app.Controllers.inventory.inventoryController import InventoryController
from app.Database.database import getDb
from app.auth.authJWTdepedency import getCurrentAdmin

router = APIRouter(prefix='/inventory', tags=['Inventory'])

def getController(db: Session = Depends(getDb)):
    return InventoryController(db)

@router.post('/', response_model=InvRecRespo, dependencies=[Depends(getCurrentAdmin)])
def addInventory(record: InvRecCreate, controller: InventoryController = Depends(getDb)):
    try: 
        return controller.addRecord(
            record.techName, record.chemName, 
            record.usageLt, record.recDate
        )
    except Exception as e: 
        print(f"Error: adding a product {e}")

@router.get('/', response_model=list[InvRecRespo])
def getInventory(controller: InventoryController = Depends(getController)):
    records = controller.getRecord()
    try:
        return [
            InvRecRespo(
                id=r.id,
                techName=r.technician.name,
                chemName=r.chemical.name,
                usageLt=r.usageLiters,
                recDate=r.recordDate
            ) for r in records
        ]
    except Exception as e:
        print(f"Error: get record unsuccessfull {e}")

@router.put('/{recordId}', response_model=InvRecRespo)
def updateInventory(recordId: int, usageLt: float, controller: InventoryController = Depends(getController)):
    record = controller.updateRecord(recordId, usageLt)
    try:
        if not record:
            raise HTTPException(status_code=404, detail="Recod not found!")
        return InvRecRespo(
            id=record.id,
            techName=record.technician.name,
            chemName=record.chemical.name,
            usageLt=record.usageLiters,
            recDate=record.recordDate
        )
    except Exception as e:
        print(f"Error: putting record unsuccessfull {e}")
    
@router.get('/{period}')
def deleteInventory(recordId: int, controller: InventoryController = Depends(getController)):
    success = controller.deleteRecord(recordId)
    try:
        if not success:
            raise HTTPException(status_code=404, detail="Record not found!")
        return { "message" : "Record deleted successfully" }
    except Exception as e:
        print(f"Error: deleting product unsuccessfull {e}")
        
@router.get('/report/{period}', response_model=list[InvRecRespo])
def report(period: str, controller: InventoryController = Depends(getController)):
    if period not in ['week', 'month', 'year']:
        raise HTTPException(status_code=400, detail="Invalid period")
    records = controller.getReport(period)
    return [
        InvRecRespo(
            id=r.id,
            techName=r.technician.name,
            chemName=r.chemical.name,
            usageLt=r.usageLiters,
            recDate=r.recordDate
        ) for r in records
    ]