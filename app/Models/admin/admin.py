from sqlalchemy import Column, Integer, String
from app.Database.database import Base

# ROLE BASE ACCESS CONTROL TYPE - APPROACH

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    usename = Column(String(50), unique=True, nullable=False)
    passwordHash = Column(String(555), nullable=False)
    role = Column(String(50), default="admin")
    
    def __repr__(self):
        return f"<Admin(username={self.usename}, role={self.role})>"