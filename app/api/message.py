from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import User, Message
from app.core.auth import get_current_user
from app.schemas.message import MessageRequest
from app.crud.pdf import query_chroma
from app.core.llm_client import client_llm

router = APIRouter()

router = APIRouter(
    prefix="/messages",
    tags=["Message"],
)


@router.get("/{document_id}")
async def get_messages(
    document_id: int = Path(..., description="ID of the document"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = db.query(Message).filter(Message.document_id == document_id).all()
    return messages


@router.post("/")
async def ask_document(
    request: MessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_message = Message(
            document_id=request.document_id, content=request.question, role="user"
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)

        results = query_chroma(current_user.id, request.document_id, request.question)
        if not results.get("documents"):
            return {"message": "No relevant documents found"}

        context_text = "\n\n".join(results["documents"][0])
        prompt = f"""
        You are an AI assistant that answers questions based on the content of a PDF document.

        === PDF CONTENT ===
        {context_text}

        === QUESTION ===
        {request.question}

        Provide a concise and clear answer.
        """
        messages = [{"role": "user", "content": prompt}]
        response = client_llm.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=messages,
            temperature=0.3,
            max_tokens=400,
        )
        ai_content = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "No response")
        )

        ai_message = Message(
            document_id=request.document_id, content=ai_content, role="assistant"
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        return {
            "question": request.question,
            "answer": response,
            "context_used": context_text[:300],
        }
    except Exception as e:
        return {"error": str(e)}
