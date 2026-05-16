from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.sql import func
from app.Database.database import Base

class DocumentRecord(Base):
    __tablename__ = "documents"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=False)
    file_name  = Column(String(255), nullable=False)
    file_data  = Column(LONGBLOB, nullable=False)    
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 