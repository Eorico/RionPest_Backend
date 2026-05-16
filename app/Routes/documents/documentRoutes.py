from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.Database.database import get_db
from app.Repositories.document.documentRepository import document_repo

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/")
async def upload_document(
    title:     str        = Form(...),
    file_name: str        = Form(...),
    file:      UploadFile = File(...),
    db:        Session    = Depends(get_db),
):
    file_data = await file.read()
    doc = document_repo.save_document(db, title, file_name, file_data)
    return {
        "id":         doc.id,
        "title":      doc.title,
        "file_name":  doc.file_name,
        "created_at": str(doc.created_at),
    }


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = document_repo.get_all(db)
    return [
        {
            "id":         d.id,
            "title":      d.title,
            "file_name":  d.file_name,
            "created_at": str(d.created_at),
        }
        for d in docs
    ]


@router.get("/{doc_id}/download")
def download_document(doc_id: int, db: Session = Depends(get_db)):
    doc = document_repo.get_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return Response(
        content=doc.file_data,
        media_type="application/vnd.openxmlformats-officedocument"
                   ".wordprocessingml.document",
        headers={"Content-Disposition":
                 f'attachment; filename="{doc.file_name}"'},
    )


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    if document_repo.delete(db, doc_id):
        return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Not found")