from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ActualChemicalUsedBased(BaseModel):
    chemical_name: str = Field(alias="actual_chemicals_name")
    quantity: str 
    remarks: Optional[str] = None
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
