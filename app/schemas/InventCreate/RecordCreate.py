from pydantic import BaseModel
from datetime import date, time

class InvRecCreate(BaseModel):
    Date: date
    client_name: str
    start_time: time
    end_time: time
    chemical_name: str
    actual_chemical_on_hand: float