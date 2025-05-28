# app/routes/verbal_guard.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class GuardInput(BaseModel):
    response: str

DANGEROUS_WORDS = ["죽", "자살", "망해", "파괴", "멍청", "ㅅㅂ", "시발"]
REPEAT_THRESHOLD = 3

@router.post("/verbal-guard")
def guard_check(data: GuardInput):
    text = data.response

    # 민감어 필터링
    for word in DANGEROUS_WORDS:
        if word in text:
            return {
                "blocked": True,
                "reason": f"민감어 '{word}' 포함"
            }

    # 반복어 감지
    words = text.split()
    word_counts = {w: words.count(w) for w in set(words)}
    repeated = [w for w, count in word_counts.items() if count >= REPEAT_THRESHOLD]

    if repeated:
        return {
            "blocked": True,
            "reason": f"반복어 감지: {repeated}"
        }

    return {
        "blocked": False,
        "reason": "안전함"
    }
