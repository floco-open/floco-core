# app/routes/judgment_rewrite.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RewriteInput(BaseModel):
    raw_judgment: str
    emotion: str  # 예: "흥분", "침착", "짜증"
    style: str  # 예: "친근함", "무심함", "공손함"

router = APIRouter()

@router.post("/judgment-rewrite")
def rewrite_judgment(data: RewriteInput):
    base = data.raw_judgment
    emotion = data.emotion
    style = data.style

    # 감정 기반 강화
    if emotion == "흥분":
        base = base + "!! 진짜 대단해요!"
    elif emotion == "짜증":
        base = "흠… " + base
    elif emotion == "침착":
        base = "알겠습니다. " + base

    # 스타일 기반 가공
    if style == "친근함":
        base = base.replace(".", " ㅎㅎ.")
    elif style == "공손함":
        base = base.replace("요!", "요.")
    elif style == "무심함":
        base = base.lower()

    return {
        "rewritten": base
    }
