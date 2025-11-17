from fastapi import APIRouter, UploadFile, File, Path, Depends, HTTPException, status
from app.core.settings import PDF_SAMPLE_PATH
from app.crud.pdf import process_pdf_chunks, query_chroma
from app.core.llm_client import client_llm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Document, User, Message
from app.core.auth import get_current_user
from app.core.chroma_client import client
from app.schemas.document import DocumentResponse
from typing import List
import os

router = APIRouter()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/documents",
    tags=["Document"],
)


@router.get("/", response_model=List[DocumentResponse])
async def get_all_documents(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents


@router.get("/messages/{document_id}")
async def get_messages(
    document_id: int = Path(..., description="ID of the document"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = db.query(Message).filter(Message.document_id == document_id).all()
    return messages


@router.delete("/{id}")
async def delete_document(
    id: int = Path(..., description="ID of the document"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = db.query(Document).filter(Document.id == id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {id} not found",
        )

    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this document",
        )

    if document.file_path and os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            print(f"Failed to delete file: {e}")

    collection_name = f"user_{document.user_id}_doc_{document.id}_pdf"
    try:
        client.delete_collection(collection_name)
    except Exception as e:
        print(f"Failed to delete Chroma collection: {e}")

    db.delete(document)
    db.commit()

    return {"message": f"Document {id} and all its data have been successfully deleted"}


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")

        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        doc = Document(
            user_id=current_user.id, name=file.filename, file_path=file_location
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        chunks_count = process_pdf_chunks(file_location, current_user.id, doc.id)

        return {
            "message": "PDF uploaded and vector data successfully created",
            "document": {"id": doc.id, "name": doc.name},
            "chunks_stored": chunks_count,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
