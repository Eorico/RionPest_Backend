from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.Database.database import get_db
from app.Controllers.admin.authController import AuthController
from app.schemas.admin.LoginRequest import LoginRequest
from app.schemas.admin.TokenResponse import TokenResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix='/auth', tags=["Auth"])

def get_controller(db: Session = Depends(get_db)):
    try:
        return AuthController(db)
    except Exception as e:
        print(f"Error: Admin Controller failed {e}")
        
@router.post('/login', response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)): 
    try:
        # Initialize the controller inside the route or via dependency
        controller = AuthController(db)
        token = controller.login(data.username, data.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return { "access_token": token }
    except Exception as e:
        print(f"Error: Login Failed {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    