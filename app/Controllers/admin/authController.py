from sqlalchemy.orm import Session
from app.auth.authService import authenticate_admin, create_access_token

class AuthController:
    def __init__(self, db: Session):
        self.db = db
        
    def login(self, username: str, password: str):
        try:
            admin = authenticate_admin(self.db, username, password)
            if not admin:
                return None
            
            token = create_access_token({ 
                "sub" : admin.username,
                "role": admin.role
            })
            
            return token
        except Exception as e:
            print(f"Error: Login failed {e}")