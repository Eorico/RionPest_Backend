from pydantic import BaseModel, ConfigDict
from typing import Optional

class ChemicalUseBased(BaseModel):
    chemical_name: str
    quantity: str 
    remarks: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
