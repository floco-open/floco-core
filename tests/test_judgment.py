# tests/test_judgment.py

from judgment_loop.memoryless_core import handle_input

def test_trigger_opens_loop():
    input_text = "설계 푸시좀 해줘"
    result = handle_input(input_text)
    assert "루프 개방됨" in result

def test_non_trigger_does_not_open_loop():
    input_text = "이건 그냥 잡담입니다"
    result = handle_input(input_text)
    assert "루프 미개방" in result

def test_response_contains_judgment_owner():
    input_text = "귀속 판단 해봐"
    result = handle_input(input_text)
    assert "고원후" in result
