# app/routes/verbal_beat.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class BeatInput(BaseModel):
    response: str

@router.post("/verbal-beat")
def apply_beat(data: BeatInput):
    text = data.response
    length = len(text)

    # 기본 쉼표 삽입 (리듬 맞춤)
    if length > 50:
        text = text.replace(" ", ", ", 2)  # 앞부분 쉼표 추가
    elif length < 20:
        text += "..."  # 짧은 응답은 여운

    # 문장 끝에 긴장감 부여
    if text.endswith("."):
        text = text[:-1] + "…"

    return {
        "rhythmic_response": text,
        "length": length
    }
