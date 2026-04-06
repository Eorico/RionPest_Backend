from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
from app.category.category import CategoryEnum
from app.schemas.chemicalBase.chemBase import ChemicalUseBased
from app.schemas.actualChemBase.actualChemBase import ActualChemicalUsedBased
from typing import List

class InvRecCreate(BaseModel):
    date: int
    month: int
    year: int
    
    category: CategoryEnum = CategoryEnum.treatment
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