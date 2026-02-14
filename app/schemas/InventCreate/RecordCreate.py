from pydantic import BaseModel
from datetime import date

class InvRecCreate(BaseModel):
    techName: str
    chemName: str
    usageLt: float
    recDate: date
