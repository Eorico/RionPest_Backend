from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.Database.database import Base
from app.Enum.category import CategoryEnum

class InventoryRecord(Base):
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    admin_under = relationship("Admin", backref="inventory_records")
    
    date = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    category = Column(Enum(CategoryEnum), default=CategoryEnum.treatment, nullable=False)
    client_name = Column(String(100), nullable=False)
    
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    start_meridiem = Column(String(2), nullable=False)
    end_meridiem = Column(String(2), nullable=False)
    
    chemicals_use = relationship("ChemicalUsed", back_populates="parent_record", cascade="all, delete-orphan")
    actual_chemicals_used = relationship("ActualChemicalUsed", back_populates="parent_record", cascade="all, delete-orphan")
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    
class ChemicalUsed(Base):
    __tablename__ = "chemicals_use"
    
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory_records.id"))
    chemical_name = Column(String(100))
    quantity = Column(String(50))
    remarks = Column(String(255), nullable=True)
    parent_record = relationship("InventoryRecord", back_populates="chemicals_use")
    
class ActualChemicalUsed(Base):
    __tablename__ = "actual_chemicals_used"
    
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory_records.id"))
    actual_chemicals_name = Column(String(100))
    quantity = Column(String(50))
    remarks = Column(String(255), nullable=True)
    parent_record = relationship("InventoryRecord", back_populates="actual_chemicals_used")