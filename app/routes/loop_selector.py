# app/routes/loop_selector.py

from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class LoopSelectInput(BaseModel):
    inferred_intents: list[str]  # intent-infer 결과에서 받은 의도 리스트

# 루프 우선순위 테이블 (예시 기준)
PRIORITY = {
    "question": 1,
    "emotional": 2,
    "uncertainty": 3,
    "command": 0  # 추후 확장
}

@router.post("/loop-selector")
def select_loop(data: LoopSelectInput):
    if not data.inferred_intents:
        return {"selected_loop": None, "reason": "no intent"}

    # 정렬: 우선순위 기준
    sorted_intents = sorted(data.inferred_intents, key=lambda i: PRIORITY.get(i, 99))
    chosen = sorted_intents[0]

    return {
        "selected_loop": f"{chosen}_loop",
        "reason": f"intent '{chosen}' has highest priority"
    }
