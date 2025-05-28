# app/routes/status.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {
        "status": "FLOCO is running",
        "version": "1.0"
    }
