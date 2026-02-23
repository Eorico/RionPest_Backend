from pydantic import BaseModel
from datetime import date, time

class InvRecCreate(BaseModel):
    treatmentDate: date
    clientName: str
    startTime: time
    endTime: time
    chemicalName: str
    actualChemicalOnHand: float