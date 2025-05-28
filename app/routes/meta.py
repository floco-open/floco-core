# app/routes/meta.py

from fastapi import APIRouter
from judgment_loop.memoryless_core import load_loop_config

router = APIRouter()

@router.get("/meta")
def get_loop_meta():
    config = load_loop_config()
    return {
        "loop_name": config.get("loop_name"),
        "judgment_owner": config.get("judgment_owner"),
        "memory": config.get("memory"),
        "trigger_keywords": config.get("trigger_keywords"),
        "output_format": config.get("output_format")
    }
