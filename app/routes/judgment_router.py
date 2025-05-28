from fastapi import APIRouter
from pydantic import BaseModel
import anthropic
import os

router = APIRouter()

# Claude API 연결
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def call_claude(prompt: str) -> str:
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=300,
            temperature=0.7,
            system="당신은 FLOCO 판단 루프의 판단 생성기입니다.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"[ERROR] Claude 호출 실패: {str(e)}"

class JudgmentInput(BaseModel):
    selected_loop: str
    input_text: str

@router.post("/judgment-router")
def route_judgment(data: JudgmentInput):
    loop = data.selected_loop
    user_input = data.input_text

    # 루프 타입에 따라 Claude 프롬프트 구성
    if loop == "question_loop":
        prompt = f"[질문 판단 루프]\n사용자 입력: {user_input}"
    elif loop == "emotional_loop":
        prompt = f"[감정 판단 루프]\n사용자 입력: {user_input}"
    elif loop == "uncertainty_loop":
        prompt = f"[불확실성 판단 루프]\n사용자 입력: {user_input}"
    else:
        prompt = f"[일반 판단 루프]\n사용자 입력: {user_input}"

    response = call_claude(prompt)
    return {"judgment": response}

