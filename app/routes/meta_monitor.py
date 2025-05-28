# app/routes/meta_monitor.py

from fastapi import APIRouter
from pydantic import BaseModel
import time

router = APIRouter()

class MetaInput(BaseModel):
    message: str
    timestamp: float  # UNIX time (초 단위)
    previous_timestamp: float  # 직전 발화 시간

EMOTION_KEYWORDS = {
    "흥분": ["와", "대박", "진짜", "헐", "미쳤"],
    "짜증": ["아놔", "뭐냐", "씨", "짜증", "노답"],
    "침착": ["음", "흠", "그렇군", "알겠어"]
}

@router.post("/meta-monitor")
def monitor_meta(data: MetaInput):
    interval = data.timestamp - data.previous_timestamp
    emotion_detected = "중립"

    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(k in data.message for k in keywords):
            emotion_detected = emotion
            break

    return {
        "emotion": emotion_detected,
        "gap_seconds": interval,
        "focus_state": "몰입" if interval < 2 else "느슨함"
    }
