from sqlalchemy.orm import Session
from app.Services.admin.adminService import admin_service

class AdminController:
    def __init__(self, db: Session):
        self.db = db
        
    def login(self, username: str, password: str):
        try:
            admin = admin_service.authenticate_admin(self.db, username, password)
            if not admin:
                return None
            
            token = admin_service.create_access_token({ 
                "sub" : admin.username,
                "role": admin.role
            })
            
            return token
        except Exception as e:
            print(f"Error: Login failed {e}")