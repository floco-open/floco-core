# memoryless_core.py

import json

def load_loop_config(path="judgment_loop/loop_config.json"):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_triggered(user_input, config):
    for keyword in config["trigger_keywords"]:
        if keyword in user_input:
            return True
    return False

def handle_input(user_input):
    config = load_loop_config()
    
    if not is_triggered(user_input, config):
        return "[FLOCO] 루프 미개방: 트리거 조건 미충족"

    # 무기억 판단 예시
    response = f"""
[FLOCO 판단 루프 개방됨]

- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 입력: "{user_input}"
- 판단 결과: [아직 판단 엔진 연결 전 상태]

(무기억 루프: 과거 발화는 저장되지 않습니다)
"""
    return response.strip()

# CLI 테스트용
if __name__ == "__main__":
    while True:
        user_input = input("입력: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print(handle_input(user_input))
