from sqlalchemy.orm import Session
from app.Models.document.documentRecord import DocumentRecord

class DocumentRepository:
    def save_document(
        self,
        db:Session,
        title:str,
        file_name:str,
        file_data:bytes
    ) -> DocumentRecord:
        
        doc = DocumentRecord(
            title=title,
            file_name=file_name,
            file_data=file_data,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    
    def get_all(self, db: Session) -> list[DocumentRecord]:
        return db.query(DocumentRecord).order_by(DocumentRecord.created_at.desc()).all()

    def get_by_id(self, db: Session, doc_id: int) -> DocumentRecord | None:
        doc = db.get(DocumentRecord, doc_id)
        if doc and isinstance(doc.file_data, str):
            # Some MySQL drivers return LONGBLOB as hex string — convert back
            doc.file_data = bytes.fromhex(doc.file_data)
        return doc

    def delete(self, db: Session, doc_id: int) -> bool:
        doc = db.get(DocumentRecord, doc_id)
        if not doc:
            return False
        db.delete(doc)
        db.commit()
        return True

document_repo = DocumentRepository()