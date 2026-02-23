from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.Models.admin.admin import Admin

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwdContext = CryptContext(schemes=['bcrypt'], deprecated="auto")


# pass functionalities
def hashPassword(password: str):
    try:
        return pwdContext.hash(password)
    except Exception as e:
        print(f"Error: hashed password unsuccessfull {e}")
        
        
# database
def verifyPassword(password: str, hashed: str):
    try:
        return pwdContext.verify(password, hashed)
    except Exception as e:
        print(f"Error: verify password failed {e}")

def authenticateAdmin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter_by(username=username).first()
    try:
        if not admin:
            return None
        if not verifyPassword(password, admin.passwordHash):
            return None
        return admin
    except Exception as e:
        print(f"Error: admin auth failed {e}")
        
# jwt
def createAccessToken(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode = data.copy()
    toEncode.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)