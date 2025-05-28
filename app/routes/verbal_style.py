# app/routes/verbal_style.py

from fastapi import APIRouter
from pydantic import BaseModel
from collections import Counter

router = APIRouter()

class StyleInput(BaseModel):
    user_message: str

STYLE_COUNTER = Counter()

@router.post("/verbal-style")
def detect_style(data: StyleInput):
    msg = data.user_message

    if "ㅋㅋ" in msg:
        STYLE_COUNTER["친근함"] += 1
    if msg.endswith(".") or msg.endswith("요."):
        STYLE_COUNTER["공손함"] += 1
    if msg.islower():
        STYLE_COUNTER["무심함"] += 1

    # 우세 스타일 선택
    if STYLE_COUNTER:
        dominant = STYLE_COUNTER.most_common(1)[0][0]
    else:
        dominant = "중립"

    return {
        "style": dominant,
        "profile": dict(STYLE_COUNTER)
    }
