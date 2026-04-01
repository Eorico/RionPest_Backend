from sqlalchemy import Column, Integer, String, Time, Float, Date, Boolean
from app.Database.database import Base
from datetime import date
import enum

class InventoryCategory(enum.Enum):
    treatment = "treatment"
    inspection = "inspection"

class InventoryRecord(Base):
    __tablename__ = "inventory_records"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=date.today)
    client_name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    chemical_name = Column(String(100), nullable=False)
    actual_chemical_on_hand = Column(Float, nullable=False)
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return (
            f"<InventoryRecord(date={self.date})>,"
            f"client={self.client_name},"
            f"chemical={self.chemical_name.name},"
            f"remaining={self.actual_chemical_on_hand},"
        )
    