from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import time
from app.category.category import CategoryEnum
from app.schemas.chemicalBase.chemBase import ChemicalUseBased
from app.schemas.actualChemBase.actualChemBase import ActualChemicalUsedBased
from typing import List

class InvRecRespo(BaseModel):
    id: int
    
    admin_under: str
    
    date: int
    month: int
    year: int
    
    category: CategoryEnum
    client_name: str
    
    start_time: time
    end_time: time
    meridiem: str
    
    chemical_use: List[ChemicalUseBased] = Field(alias="chemicals_use")
    actual_chemical_used: List[ActualChemicalUsedBased] = Field(alias="actual_chemicals_used")
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    @field_validator("admin_under", mode="before")
    @classmethod
    def get_username_from_admin(cls, v):
        if hasattr(v, "username"):
            return v.username
        return v