from sqlalchemy import Column, Integer, String, Time, Float, Date
from app.Database.database import Base
from sqlalchemy.orm import relationship
from datetime import date

class InventoryRecord(Base):
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    treatmentDate = Column(Date, default=date.today)
    clientName = Column(String(100), nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    chemicalName = Column(String(100), nullable=False)
    actualChemicalOnHand = Column(Float, nullable=False)
    
    def __repr__(self):
        return (
            f"<InventoryRecord(date={self.treatmentDate})>,"
            f"client={self.clientName},"
            f"chemical={self.chemicalName.name},"
            f"remaining={self.actualChemicalOnHand},"
        )
    