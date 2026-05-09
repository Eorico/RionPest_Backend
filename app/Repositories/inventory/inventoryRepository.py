from datetime import date, timedelta

from sqlalchemy.orm import Session, joinedload

from app.Models.inventory.inventoryRecord import (
    ActualChemicalUsed,
    ChemicalUsed,
    InventoryRecord,
)


class InventoryRepository:

    #  Base queries                                     
    def get_all(self, db: Session) -> list[InventoryRecord]:
        return db.query(InventoryRecord).all()

    def get_active(self, db: Session) -> list[InventoryRecord]:
        return (
            db.query(InventoryRecord)
            .filter(InventoryRecord.is_deleted == False)
            .all()
        )

    def get_by_id(self, db: Session, rec_id: int) -> InventoryRecord | None:
        return db.get(InventoryRecord, rec_id)

    def get_active_by_id(self, db: Session, rec_id: int) -> InventoryRecord | None:
        return (
            db.query(InventoryRecord)
            .filter(
                InventoryRecord.id == rec_id,
                InventoryRecord.is_deleted == False,
            )
            .first()
        )

    def get_deleted_by_id(self, db: Session, rec_id: int) -> InventoryRecord | None:
        return (
            db.query(InventoryRecord)
            .filter(
                InventoryRecord.id == rec_id,
                InventoryRecord.is_deleted == True,
            )
            .first()
        )

    def get_all_deleted(self, db: Session) -> list[InventoryRecord]:
        return (
            db.query(InventoryRecord)
            .filter(InventoryRecord.is_deleted == True)
            .all()
        )

    def get_with_chemicals(self, db: Session, rec_id: int) -> InventoryRecord | None:
        return (
            db.query(InventoryRecord)
            .options(
                joinedload(InventoryRecord.chemicals_use),
                joinedload(InventoryRecord.actual_chemicals_used),
            )
            .filter(InventoryRecord.id == rec_id)
            .first()
        )

   
    #  Report filters                
    def get_by_period(self, db: Session, period: str) -> list[InventoryRecord]:
        today = date.today()
        query = db.query(InventoryRecord)

        if period == "week":
            start = today - timedelta(days=7)
            query = query.filter(InventoryRecord.date >= start)
        elif period == "month":
            query = query.filter(
                InventoryRecord.date.month == today.month,
                InventoryRecord.date.year == today.year,
            )
        elif period == "year":
            query = query.filter(InventoryRecord.date.year == today.year)

        return query.all()

    #  Writes                       
    def create(self, db: Session, record: InventoryRecord) -> InventoryRecord:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def add_chemical(self, db: Session, entry: ChemicalUsed) -> None:
        db.add(entry)

    def add_actual_chemical(self, db: Session, entry: ActualChemicalUsed) -> None:
        db.add(entry)

    def save(self, db: Session) -> None:
        db.commit()

    def flush(self, db: Session) -> None:
        db.flush()

    def refresh(self, db: Session, record: InventoryRecord) -> None:
        db.refresh(record)

    def delete(self, db: Session, record: InventoryRecord) -> None:
        db.delete(record)

    def rollback(self, db: Session) -> None:
        db.rollback()

    def bulk_restore(self, db: Session) -> None:
        db.query(InventoryRecord).filter(
            InventoryRecord.is_deleted == True
        ).update({"is_deleted": False})


inventory_repo = InventoryRepository()