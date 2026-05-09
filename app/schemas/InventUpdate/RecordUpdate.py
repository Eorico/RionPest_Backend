from pydantic import BaseModel, ConfigDict, Field
from datetime import time
from app.Enum.category import CategoryEnum
from app.Schemas.chemicalBase.chemBase import ChemicalUseBased
from app.Schemas.actualChemBase.actualChemBase import ActualChemicalUsedBased
from typing import List, Optional

class InvRecUpdate(BaseModel):
    date: Optional[int] = None
    month: Optional[int]  = None
    year: Optional[int]  = None
    category: Optional[CategoryEnum] = None
    client_name: Optional[str]  = None
    start_time: Optional[time]  = None
    end_time: Optional[time]  = None
    start_meridiem: Optional[str]  = None
    end_meridiem: Optional[str] = None

    # Use the same aliases as InvRecCreate so the frontend payload is consistent
    chemical_use: Optional[List[ChemicalUseBased]] = Field(
        default=None, alias="chemicals_use"
    )
    actual_chemical_used: Optional[List[ActualChemicalUsedBased]] = Field(
        default=None, alias="actual_chemicals_used"
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )