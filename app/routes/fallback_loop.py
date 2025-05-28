# app/routes/fallback_loop.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FallbackInput(BaseModel):
    last_response: str
    user_feedback: str  # 예: "이건 좀 이상해", "다시 말해줘", "아닌데?"

FALLBACK_TRIGGERS = ["이상해", "무슨 말이야", "이해 안 돼", "다시", "아닌데", "틀렸어", "다르게"]

@router.post("/fallback-loop")
def fallback_handler(data: FallbackInput):
    for word in FALLBACK_TRIGGERS:
        if word in data.user_feedback:
            return {
                "fallback_triggered": True,
                "reason": f"user flagged issue with '{word}'",
                "action": "retry_or_handover"
            }

    return {
        "fallback_triggered": False,
        "reason": "no fallback conditions met"
    }
