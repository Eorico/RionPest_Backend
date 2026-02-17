from sqlalchemy import Column, Integer, String
from app.Database.database import Base

class Admin(Base):
    __table__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    usename = Column(String(50), unique=True, nullable=False)
    passwordHash = Column(String(555), nullable=False)
    
    