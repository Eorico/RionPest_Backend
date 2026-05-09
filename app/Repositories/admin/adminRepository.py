from sqlalchemy.orm import Session

from app.Models.admin.admin import Admin


class AdminRepository:

    def get_by_username(self, db: Session, username: str) -> Admin | None:
        return db.query(Admin).filter_by(username=username).first()

    def get_by_id(self, db: Session, admin_id: int) -> Admin | None:
        return db.get(Admin, admin_id)

    def create(self, db: Session, admin: Admin) -> Admin:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    def save(self, db: Session) -> None:
        db.commit()


admin_repo = AdminRepository()