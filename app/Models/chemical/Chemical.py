from sqlalchemy import Column, Integer, String
from app.Database.database import Base

class Chemical(Base):
    __tablename__ = "chemicals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Chemicals(name={self.name})>"