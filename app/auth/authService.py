from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.Models.admin.admin import Admin

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# pass functionalities
def hash_password(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error: hashed password unsuccessfull {e}")
        
        
# database
def verify_password(password: str, hashed: str):
    try:
        return pwd_context.verify(password, hashed)
    except Exception as e:
        print(f"Error: verify password failed {e}")

def authenticate_admin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter_by(username=username).first()
    try:
        if not admin:
            return None
        if not verify_password(password, admin.password_hash):
            return None
        return admin
    except Exception as e:
        print(f"Error: admin auth failed {e}")
        
# jwt
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)