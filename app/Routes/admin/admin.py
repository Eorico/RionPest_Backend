from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Database.database import getDb
from app.Controllers.admin.authController import AuthController
from app.schemas.admin.LoginRequest import LoginRequest
from app.schemas.admin.TokenResponse import TokenResponse

router = APIRouter(prefix='/auth', tags=["Auth"])

def getController(db: Session = Depends(getDb)):
    try:
        return AuthController(db)
    except Exception as e:
        print(f"Error: Admin Controller failed {e}")
        
@router.post('/login', response_model=TokenResponse)
def login(data: LoginRequest, controller: AuthController = Depends(getController)): 
    try:
        token = controller.login(data.username, data.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return { "access_token": token }
    except Exception as e:
        print(f"Error: Login Failed {e}")
    