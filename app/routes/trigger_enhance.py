# app/routes/trigger_enhance.py

from fastapi import APIRouter
from pydantic import BaseModel
import re

router = APIRouter()

class TriggerInput(BaseModel):
    text: str

# 상황 기반 트리거 단어 외 패턴 (의도 강조 표현, 반복, 강세 등)
SOFT_TRIGGERS = ["...", "그니까", "근데 말이야", "하긴", "맞다", "아 맞아", "뭐더라"]

@router.post("/trigger-enhance")
def enhanced_trigger(input: TriggerInput):
    for soft in SOFT_TRIGGERS:
        if soft in input.text:
            return {
                "trigger": True,
                "reason": f"soft trigger matched: {soft}",
                "method": "contextual"
            }

    if re.search(r"(음+|어+|맞+|헐+)", input.text):
        return {
            "trigger": True,
            "reason": "pattern matched (vocal hesitation or emphasis)",
            "method": "regex"
        }

    return {"trigger": False, "reason": "no match"}
