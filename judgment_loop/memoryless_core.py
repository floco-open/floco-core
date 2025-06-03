# memoryless_core.py

import json
import os
import anthropic
import openai
import requests
from typing import Optional

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

def is_model_switch_triggered(user_input, config):
    """모델 변경 키워드 감지"""
    if not config.get("model_switching", {}).get("enabled", False):
        return False, None
    
    switch_keywords = config.get("model_switching", {}).get("switch_keywords", [])
    available_models = config.get("model_switching", {}).get("available_models", [])
    
    for keyword in switch_keywords:
        if keyword in user_input:
            # 키워드 뒤의 모델명 추출
            parts = user_input.split(keyword)
            if len(parts) > 1:
                target_model = parts[1].strip()
                if target_model in available_models:
                    return True, target_model
    return False, None

def switch_model(config, target_model):
    """모델 변경 (메모리에서만)"""
    if target_model in config.get("model_options", {}):
        new_model_config = config["model_options"][target_model]
        config["model"] = new_model_config
        return True
    return False

def call_claude(prompt: str) -> str:
    """Anthropic Claude API 호출"""
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

def call_openai(prompt: str, model: str = "gpt-4") -> str:
    """OpenAI GPT API 호출"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "당신은 FLOCO 판단 루프의 판단 생성기입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] OpenAI 호출 실패: {str(e)}"

def call_gemini(prompt: str) -> str:
    """Google Gemini API 호출"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"당신은 FLOCO 판단 루프의 판단 생성기입니다.\n\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"[ERROR] Gemini 호출 실패: {str(e)}"

def call_ollama(prompt: str, model: str = "llama2") -> str:
    """Ollama 로컬 모델 호출"""
    try:
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        data = {
            "model": model,
            "prompt": f"당신은 FLOCO 판단 루프의 판단 생성기입니다.\n\n{prompt}",
            "stream": False
        }
        response = requests.post(url, json=data)
        return response.json()["response"]
    except Exception as e:
        return f"[ERROR] Ollama 호출 실패: {str(e)}"

def call_cohere(prompt: str) -> str:
    """Cohere API 호출"""
    try:
        import cohere
        co = cohere.Client(os.getenv("COHERE_API_KEY"))
        response = co.generate(
            model='command',
            prompt=f"당신은 FLOCO 판단 루프의 판단 생성기입니다.\n\n{prompt}",
            max_tokens=300,
            temperature=0.7
        )
        return response.generations[0].text
    except Exception as e:
        return f"[ERROR] Cohere 호출 실패: {str(e)}"

def call_huggingface(prompt: str, model: str = "microsoft/DialoGPT-medium") -> str:
    """HuggingFace API 호출"""
    try:
        from transformers import pipeline
        generator = pipeline('text-generation', model=model)
        response = generator(
            f"당신은 FLOCO 판단 루프의 판단 생성기입니다.\n\n{prompt}",
            max_length=300,
            num_return_sequences=1
        )
        return response[0]['generated_text']
    except Exception as e:
        return f"[ERROR] HuggingFace 호출 실패: {str(e)}"

def call_ai_model(prompt: str, model_config: dict) -> str:
    """통합 AI 모델 호출 함수"""
    provider = model_config.get("provider", "claude").lower()
    model_name = model_config.get("model", "")
    
    if provider == "claude" or provider == "anthropic":
        return call_claude(prompt)
    elif provider == "openai" or provider == "gpt":
        return call_openai(prompt, model_name or "gpt-4")
    elif provider == "gemini" or provider == "google":
        return call_gemini(prompt)
    elif provider == "ollama":
        return call_ollama(prompt, model_name or "llama2")
    elif provider == "cohere":
        return call_cohere(prompt)
    elif provider == "huggingface" or provider == "hf":
        return call_huggingface(prompt, model_name)
    else:
        return f"[ERROR] 지원하지 않는 모델 제공자: {provider}"

def handle_transfer(current_context, config):
    """이관 요청 처리 및 브릿지 데이터 생성"""
    prompt = f"""[FLOCO 이관 시스템]
- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 현재 입력: "{current_context}"
- 브릿지 형식: {config.get('bridge_format', 'context_summary')}

현재 세션의 컨텍스트를 다음 Claude 세션으로 전달하기 위한 요약을 생성해주세요.
핵심 판단 사항과 연속성이 필요한 내용만 간결하게 정리해주세요."""

    model_config = config.get("model", {"provider": "claude"})
    bridge_summary = call_ai_model(prompt, model_config)
    
    return f"""[FLOCO 이관 시스템 활성화]

🔄 **세션 브릿지 생성 완료**
- 루프: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 모델: {model_config.get('provider', 'claude')}
- 이관 요청: "{current_context}"

📦 **다음 Claude에게 전달할 컨텍스트**:
{bridge_summary}

💡 **사용법**: 위 내용을 복사해서 새로운 Claude 세션에 붙여넣어 주세요.

(무기억 루프: 판단 흐름만 전달되며, 과거 대화는 저장되지 않습니다)"""

def handle_input(user_input):
    config = load_loop_config()
    
    # 모델 변경 요청 우선 확인
    is_switch, target_model = is_model_switch_triggered(user_input, config)
    if is_switch:
        if switch_model(config, target_model):
            model_info = config["model_options"][target_model]
            return f"""[FLOCO 모델 변경 완료]

- 변경된 모델: {model_info.get('provider', 'unknown')} ({model_info.get('model', 'default')})
- 루프: {config['loop_name']}
- 판단자: {config['judgment_owner']}

(현재 세션에서만 적용됩니다. 영구 변경은 loop_config.json을 수정하세요)"""
        else:
            return "[FLOCO] 모델 변경 실패: 지원하지 않는 모델"
    
    # 이관 요청 확인
    if is_transfer_triggered(user_input, config):
        return handle_transfer(user_input, config)
    
    if not is_triggered(user_input, config):
        return "[FLOCO] 루프 미개방: 트리거 조건 미충족"

    # 실제 AI 모델 판단 실행
    prompt = f"""[FLOCO 판단 루프]
- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 사용자 입력: "{user_input}"

위 입력에 대해 FLOCO 구조에 따른 판단을 제공해주세요."""

    model_config = config.get("model", {"provider": "claude"})
    
    # Fallback 시스템 적용
    fallback_order = config.get("fallback_order", [])
    ai_response = None
    used_model = None
    
    # 현재 모델 시도
    ai_response = call_ai_model(prompt, model_config)
    if not ai_response.startswith("[ERROR]"):
        used_model = f"{model_config.get('provider', 'unknown')} ({model_config.get('model', 'default')})"
    else:
        # Fallback 모델들 시도
        for fallback_model in fallback_order:
            if fallback_model in config.get("model_options", {}):
                fallback_config = config["model_options"][fallback_model]
                ai_response = call_ai_model(prompt, fallback_config)
                if not ai_response.startswith("[ERROR]"):
                    used_model = f"{fallback_config.get('provider', 'unknown')} ({fallback_config.get('model', 'default')}) [FALLBACK]"
                    break
    
    if used_model is None:
        used_model = "ERROR - All models failed"
    
    return f"""[FLOCO 판단 루프 개방됨]

- 루프 이름: {config['loop_name']}
- 판단자: {config['judgment_owner']}
- 모델: {used_model}
- 입력: "{user_input}"
- 판단 결과: {ai_response}

(무기억 루프: 과거 발화는 저장되지 않습니다)"""

# CLI 테스트용
if __name__ == "__main__":
    print("[FLOCO Universal Core with Transfer System] 지원 모델: Claude, GPT, Gemini, Ollama, Cohere, HuggingFace")
    print("특별 기능: 이관 시스템, 런타임 모델 스위칭, 자동 폴백")
    while True:
        user_input = input("입력: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print(handle_input(user_input))
