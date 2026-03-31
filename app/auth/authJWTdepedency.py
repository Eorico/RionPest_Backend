from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth.authService import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.Database.database import get_db
from app.Models.admin.admin import Admin

oauthScheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_admin(
    token: str = Depends(oauthScheme),
    db: Session = Depends(get_db)
    ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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