from pydantic import BaseModel, ConfigDict
from datetime import date, time
from app.category.category import CategoryEnum

class InvRecRespo(BaseModel):
    id: int
    
    category: CategoryEnum
    
    Date: date
    client_name: str
    start_time: time
    end_time: time
    
    chemical_name: str
    actual_chemical_on_hand: float
    model_config = ConfigDict(from_attributes=True)