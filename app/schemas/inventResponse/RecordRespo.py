from pydantic import BaseModel, ConfigDict
from datetime import date, time

class InvRecRespo(BaseModel):
    id: int
    treatmentDate: date
    clientName: str
    startTime: time
    endTime: time
    chemicalName: str
    actualChemicalOnHand: float
    model_config = ConfigDict(from_attributes=True)
