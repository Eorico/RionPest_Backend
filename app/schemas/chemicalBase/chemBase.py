from pydantic import BaseModel, ConfigDict

class ChemicalUseBased(BaseModel):
    chemical_name: str
    quantity: str 
    model_config = ConfigDict(from_attributes=True)
