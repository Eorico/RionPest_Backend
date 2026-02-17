from pydantic import BaseModel

class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"