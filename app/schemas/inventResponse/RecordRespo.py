from pydantic import BaseModel
from datetime import date

class InvRecCreate(BaseModel):
    id: str
    techName: str
    chemName: str
    usageLt: float
    recDate: date
    
    class Config:
        ormMode = True
