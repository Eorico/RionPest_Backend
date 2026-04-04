from pydantic import BaseModel
from datetime import date, time
from app.category.category import CategoryEnum

class InvRecCreate(BaseModel):
    Date: date
    category: CategoryEnum = CategoryEnum.treatment
    client_name: str
    start_time: time
    end_time: time
    chemical_name: str
    actual_chemical_on_hand: float