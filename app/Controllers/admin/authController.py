from sqlalchemy.orm import Session
from app.auth.authService import authenticateAdmin, createAccessToken

class AuthController:
    def __init__(self, db: Session):
        self.db = db
        
    def login(self, username: str, password: str):
        try:
            admin = authenticateAdmin(self.db, username, password)
            if not admin:
                return None
            
            token = createAccessToken({ 
                "sub" : admin.usename,
                "role": admin.role
            })
            
            return token
        except Exception as e:
            print(f"Error: Login failed {e}")