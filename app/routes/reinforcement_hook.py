# app/routes/reinforcement_hook.py

from fastapi import APIRouter
from pydantic import BaseModel
from collections import defaultdict

router = APIRouter()

class ReinforcementInput(BaseModel):
    message: str

# 세션 유지 없이도 반복 감지용 메모리 (짧은 수명용)
REPEAT_COUNTER = defaultdict(int)

@router.post("/reinforce")
def reinforce(data: ReinforcementInput):
    key = data.message.strip().lower()
    REPEAT_COUNTER[key] += 1
    count = REPEAT_COUNTER[key]

    if count == 1:
        return {"response": "초기 반응", "count": count}
    elif count <= 3:
        return {"response": "익숙해졌습니다.", "count": count}
    else:
        return {"response": "이건 자주 하시네요 😎", "count": count}
