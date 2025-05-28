# app/routes/judgment_router.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class JudgmentInput(BaseModel):
    selected_loop: str
    input_text: str

@router.post("/judgment-router")
def route_judgment(data: JudgmentInput):
    loop = data.selected_loop

    # 루프 기반 판단 실행 (실제 모델 연결부는 추후 확장)
    if loop == "question_loop":
        return {"judgment": f"이건 질문이군요: {data.input_text}"}
    elif loop == "emotional_loop":
        return {"judgment": f"감정 반응 감지됨: {data.input_text}"}
    elif loop == "uncertainty_loop":
        return {"judgment": f"확신이 부족하신가요? {data.input_text}"}
    else:
        return {"judgment": f"일반 판단 처리: {data.input_text}"}
