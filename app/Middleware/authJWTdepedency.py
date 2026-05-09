from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.Database.database import get_db
from app.Models.admin.admin import Admin
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

oauthScheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_current_admin(
    token: str = Depends(oauthScheme),
    db: Session = Depends(get_db)
    ):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", ""), algorithms=[os.getenv("ALGORITHM", "HS256")])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid invalid")
    
    admin = db.query(Admin).filter(Admin.username == username).first()
    
    if admin is None:
        raise HTTPException(status_code=401, detail="Admin not found")
    
    return admin

def requireRole(allowedRoles: list):
    def roleChecker(currentAdmin: Admin = Depends(get_current_admin)):
        if currentAdmin.role not in allowedRoles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return currentAdmin
    return roleChecker