from pydantic import BaseModel, ConfigDict, Field

class ActualChemicalUsedBased(BaseModel):
    chemical_name: str = Field(alias="actual_chemicals_name")
    quantity: str 
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
