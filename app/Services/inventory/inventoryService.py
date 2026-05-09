from sqlalchemy.orm import Session

from app.Models.inventory.inventoryRecord import (
    ActualChemicalUsed,
    ChemicalUsed,
    InventoryRecord,
)
from app.Repositories.admin.adminRepository import admin_repo
from app.Repositories.inventory.inventoryRepository import inventory_repo


class InventoryService:

    #  Create                                                   
    def create_record(
        self,
        db: Session,
        admin_username: str,
        date: int,
        month: int,
        year: int,
        category: str,
        client_name: str,
        start_time: str,
        end_time: str,
        start_meridiem: str,
        end_meridiem: str,
        chemical_use: list,
        actual_chemical_used: list,
    ) -> InventoryRecord:

        admin = admin_repo.get_by_username(db, admin_username)
        if not admin:
            raise ValueError(f"Admin '{admin_username}' not found in database.")

        new_record = InventoryRecord(
            admin_id=admin.id,
            admin_under=admin,
            date=date,
            month=month,
            year=year,
            category=category,
            client_name=client_name,
            start_time=start_time,
            end_time=end_time,
            start_meridiem=start_meridiem,
            end_meridiem=end_meridiem,
        )

        inventory_repo.create(db, new_record)

        for item in chemical_use:
            inventory_repo.add_chemical(
                db,
                ChemicalUsed(
                    inventory_id=new_record.id,
                    chemical_name=item.chemical_name,
                    quantity=item.quantity,
                    remarks=getattr(item, "remarks", None),
                ),
            )

        for item in actual_chemical_used:
            inventory_repo.add_actual_chemical(
                db,
                ActualChemicalUsed(
                    inventory_id=new_record.id,
                    actual_chemicals_name=item.chemical_name,
                    quantity=item.quantity,
                    remarks=getattr(item, "remarks", None),
                ),
            )

        inventory_repo.save(db)

        return inventory_repo.get_with_chemicals(db, new_record.id)

 
    #  Read                                                     
    def get_all_records(self, db: Session) -> list[InventoryRecord]:
        return inventory_repo.get_all(db)

    def get_active_records(self, db: Session) -> list[InventoryRecord]:
        return inventory_repo.get_active(db)

    def generate_report(self, db: Session, period: str) -> list[InventoryRecord]:
        return inventory_repo.get_by_period(db, period)

    #  Update                                                             
    def update_record(
        self,
        db: Session,
        rec_id: int,
        admin_username: str = None,
        date=None,
        month=None,
        year=None,
        category=None,
        client_name=None,
        start_time=None,
        end_time=None,
        start_meridiem=None,
        end_meridiem=None,
        chemical_use: list = None,
        actual_chemical_used: list = None,
    ) -> InventoryRecord | None:

        try:
            record = inventory_repo.get_active_by_id(db, rec_id)
            if not record:
                return None

            if admin_username:
                admin = admin_repo.get_by_username(db, admin_username)
                if admin:
                    record.admin_id = admin.id

            if date is not None: record.date = date
            if month is not None: record.month = month
            if year is not None: record.year = year
            if category is not None: record.category = category
            if client_name is not None: record.client_name = client_name
            if start_time is not None: record.start_time = start_time
            if end_time is not None: record.end_time = end_time
            if start_meridiem is not None: record.start_meridiem = start_meridiem
            if end_meridiem is not None: record.end_meridiem = end_meridiem

            if chemical_use is not None:
                record.chemicals_use.clear()
                inventory_repo.flush(db)
                record.chemicals_use = [
                    ChemicalUsed(
                        inventory_id=record.id,
                        chemical_name=c.chemical_name,
                        quantity=c.quantity,
                        remarks=c.remarks or "",
                    )
                    for c in chemical_use
                ]

            if actual_chemical_used is not None:
                record.actual_chemicals_used.clear()
                inventory_repo.flush(db)
                record.actual_chemicals_used = [
                    ActualChemicalUsed(
                        inventory_id=record.id,
                        actual_chemicals_name=c.chemical_name,
                        quantity=c.quantity,
                        remarks=c.remarks or "",
                    )
                    for c in actual_chemical_used
                ]

            inventory_repo.save(db)
            inventory_repo.refresh(db, record)
            return record

        except Exception as e:
            inventory_repo.rollback(db)
            print(f"Error: update record unsuccessful — {e}")
            return None

    #  Delete / Restore                                                  
    def soft_delete(self, db: Session, rec_id: int) -> bool:
        record = inventory_repo.get_by_id(db, rec_id)
        if record:
            record.is_deleted = True
            inventory_repo.save(db)
            return True
        return False

    def permanent_delete(
        self, db: Session, rec_id: int = None, delete_all: bool = False
    ) -> tuple[bool, str]:

        if delete_all:
            for record in inventory_repo.get_all_deleted(db):
                inventory_repo.delete(db, record)
        else:
            record = inventory_repo.get_deleted_by_id(db, rec_id)
            if not record:
                return False, "Record not found"
            inventory_repo.delete(db, record)

        inventory_repo.save(db)
        return True, "Permanently deleted"

    def restore_record(
        self, db: Session, rec_id: int = None, restore_all: bool = False
    ) -> bool:

        if restore_all:
            inventory_repo.bulk_restore(db)
        else:
            record = inventory_repo.get_deleted_by_id(db, rec_id)
            if record:
                record.is_deleted = False

        inventory_repo.save(db)
        return True

inventory_service = InventoryService()