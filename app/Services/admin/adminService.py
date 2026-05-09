import os
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.Models.admin.admin import Admin
from app.Repositories.admin.adminRepository import admin_repo

#  Environment                                     
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

_raw_expire = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def _parse_expire(raw: str | None) -> int:
    try:
        return int(raw) if raw else os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "")
    except (ValueError, TypeError):
        return os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "")

#  Service                                                        
class AdminService:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._secret_key: str = os.getenv("SECRET_KEY", "")
        self._algorithm: str = os.getenv("ALGORITHM", "HS256")
        self._token_expire_minutes: int = _parse_expire(_raw_expire)

    #  Password                                             
    def hash_password(self, password: str) -> str | None:
        try:
            return self._pwd_context.hash(password)
        except Exception as e:
            print(f"Error: hashing password unsuccessful — {e}")
            return None

    def verify_password(self, plain: str, hashed: str) -> bool:
        try:
            return self._pwd_context.verify(plain, hashed)
        except Exception as e:
            print(f"Error: verify password failed — {e}")
            return False

    #  Authentication                                               
    def authenticate_admin(
        self, db: Session, username: str, password: str
    ) -> Admin | None:
        try:
            admin = admin_repo.get_by_username(db, username)
            if not admin:
                return None
            if not self.verify_password(password, admin.password_hash):
                return None
            return admin
        except Exception as e:
            print(f"Error: admin authentication failed — {e}")
            return None

    #  JWT                                                     
    def create_access_token(self, data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self._token_expire_minutes)
        payload = {**data, "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)


admin_service = AdminService()