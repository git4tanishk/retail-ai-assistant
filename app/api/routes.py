
import traceback

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat import ask_question

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = ask_question(request.question)
        return ChatResponse(answer=answer)

    except Exception as error:
        print("\n========== CHAT API ERROR ==========")
        traceback.print_exc()
        print("====================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error
