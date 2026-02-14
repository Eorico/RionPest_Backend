from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.Database.database import Base
from sqlalchemy.orm import relationship
from datetime import date

class InventoryRecord(Base):
    __table__ = "inventory_records"
    id = Column(Integer, primary_key=True, index=True)
    technicianID = Column(Integer, ForeignKey("technicians.id"))
    chemicalID = Column(Integer, ForeignKey("chemicals.id"))
    usageLiters = Column(Float, nullable=False)
    recordDate = Column(Date, default=date.today)
    
    technician = relationship("Technician")
    chemical = relationship("Chemical")
    
    def __repr__(self):
        return f"<InventoryRecord(tech={self.technician.name}, chem={self.chemical.name}, usage={self.usageLiters}L)>"
    