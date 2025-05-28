# app/routes/intent_infer.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class IntentInput(BaseModel):
    text: str

# 간단한 감정/의도 키워드 및 기호 세트
INTENT_KEYWORDS = ["설계", "어떻게", "이거 뭐야", "왜", "진짜?", "맞지?", "다음", "ㅋㅋ", "아니", "그니까"]
EMOJI_HINTS = ["ㅎㅎ", "ㅋㅋ", "ㅠㅠ", "😅", "😎"]

@router.post("/intent-infer")
def infer_intent(input: IntentInput):
    intents = []

    for word in INTENT_KEYWORDS:
        if word in input.text:
            intents.append({"intent": "question", "trigger": word})

    for emoji in EMOJI_HINTS:
        if emoji in input.text:
            intents.append({"intent": "emotional", "trigger": emoji})

    if "..." in input.text or input.text.endswith("?"):
        intents.append({"intent": "uncertainty", "trigger": "..."})

    if not intents:
        return {"inferred": False, "reason": "no strong signal"}

    return {"inferred": True, "intents": intents}
