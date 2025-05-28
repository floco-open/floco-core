# app/routes/verbal_trigger.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TriggerInput(BaseModel):
    last_user_input: str
    silence_duration: float  # 초 단위
    user_emotion: str  # 예: "침묵", "당황", "집중", "무관심"

@router.post("/verbal-trigger")
def decide_trigger(data: TriggerInput):
    should_speak = False
    reason = ""

    if data.silence_duration > 5 and data.user_emotion in ["침묵", "당황"]:
        should_speak = True
        reason = "침묵 + 감정 변화 감지"

    elif "?" in data.last_user_input:
        should_speak = True
        reason = "질문 형태 감지"

    elif data.user_emotion == "무관심":
        should_speak = False
        reason = "무반응 유지"

    return {
        "speak_now": should_speak,
        "reason": reason
    }
