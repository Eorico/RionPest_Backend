from pydantic import BaseModel
from datetime import date, time

class InvRecRespo(BaseModel):
    id: int
    treatmentDate: date
    clientName: str
    startTime: time
    endTime: time
    chemicalName: str
    actualChemicalOnHand: float
    
    class Config:
        fromAttributes = True
