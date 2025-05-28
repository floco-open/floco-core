# app/routes/feedback.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Feedback(BaseModel):
    message: str
    response_quality: int  # 1~5점

@router.post("/feedback")
def submit_feedback(data: Feedback):
    # 실제 서비스에서는 DB나 파일 저장 가능
    return {
        "message": "피드백 감사합니다.",
        "received": data.message,
        "score": data.response_quality
    }
