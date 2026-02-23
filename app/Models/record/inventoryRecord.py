from sqlalchemy import Column, Integer, String, Time, ForeignKey, Float
from app.Database.database import Base
from sqlalchemy.orm import relationship
from datetime import date

class InventoryRecord(Base):
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    treatmentDate = Column(String, default=date.today)
    clientName = Column(String, nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    chemicalID = Column(Integer, ForeignKey("chemical.id"))
    chemical = relationship("Chemical")
    actualChemicalOnHand = Column(Float, nullable=False)
    
    def __repr__(self):
        return (
            f"<InventoryRecord(date={self.treatmentDate})>,"
            f"client={self.clientName},"
            f"chemical={self.chemical.name},"
            f"remaining={self.actualChemicalOnHand},"
        )
    