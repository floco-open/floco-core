# memoryless_core.py

import json
import os
import anthropic

def load_loop_config(path="judgment_loop/loop_config.json"):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_triggered(user_input, config):
    for keyword in config["trigger_keywords"]:
        if keyword in user_input:
            return True
    return False

def is_transfer_triggered(user_input, config):
    """이관 키워드 감지"""
    if "transfer_keywords" not in config:
        return False
    for keyword in config["transfer_keywords"]:
        if keyword in user_input:
            return True
    return False

def call_claude(prompt: str) -> str:
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            temperature=0.7,
            system="당신은 FLOCO 판단 루프의 판단 생성기입니다.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"[ERROR] Claude 호출 실패: {str(e)}"

def handle_transfer(current_context, config):
    """이관 요청 처리 및 브릿지 데이터 생성"""
    prompt = f"""[FLOCO 이관 시스템]
- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 현재 입력: "{current_context}"
- 브릿지 형식: {config.get('bridge_format', 'context_summary')}

현재 세션의 컨텍스트를 다음 Claude 세션으로 전달하기 위한 요약을 생성해주세요.
핵심 판단 사항과 연속성이 필요한 내용만 간결하게 정리해주세요."""

    bridge_summary = call_claude(prompt)
    
    return f"""[FLOCO 이관 시스템 활성화]

🔄 **세션 브릿지 생성 완료**
- 루프: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 이관 요청: "{current_context}"

📦 **다음 Claude에게 전달할 컨텍스트**:
{bridge_summary}

💡 **사용법**: 위 내용을 복사해서 새로운 Claude 세션에 붙여넣어 주세요.

(무기억 루프: 판단 흐름만 전달되며, 과거 대화는 저장되지 않습니다)"""

def handle_input(user_input):
    config = load_loop_config()
    
    # 이관 요청 우선 확인
    if is_transfer_triggered(user_input, config):
        return handle_transfer(user_input, config)
    
    if not is_triggered(user_input, config):
        return "[FLOCO] 루프 미개방: 트리거 조건 미충족"

    # 실제 Claude 판단 실행
    prompt = f"""[FLOCO 판단 루프]
- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 사용자 입력: "{user_input}"

위 입력에 대해 FLOCO 구조에 따른 판단을 제공해주세요."""

    claude_response = call_claude(prompt)
    
    return f"""[FLOCO 판단 루프 개방됨]

- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 입력: "{user_input}"
- 판단 결과: {claude_response}

(무기억 루프: 과거 발화는 저장되지 않습니다)"""

# CLI 테스트용
if __name__ == "__main__":
    while True:
        user_input = input("입력: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print(handle_input(user_input))
