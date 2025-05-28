# app/routes/emergency_break.py

from fastapi import APIRouter
from pydantic import BaseModel
import time

router = APIRouter()

class EmergencyInput(BaseModel):
    error_count: int
    emotion: str
    gap_seconds: float

@router.post("/emergency-break")
def emergency_handler(data: EmergencyInput):
    if data.error_count >= 3:
        return {"break": True, "reason": "반복 판단 실패"}
    
    if data.emotion in ["짜증", "흥분"] and data.gap_seconds < 1:
        return {"break": True, "reason": "감정 과열 + 과도한 판단 속도"}

    return {"break": False, "reason": "안정 상태"}
