# app/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from judgment_loop.memoryless_core import handle_input
from app.routes import meta
from app.routes import feedback
from app.routes import status
from app.routes import trigger_enhance
from app.routes import intent_infer
from app.routes import loop_selector
from app.routes import fallback_loop
from app.routes import meta_monitor
from app.routes import reinforcement_hook

app = FastAPI()

class InputData(BaseModel):
    message: str

@app.post("/judgment")
async def judgment(data: InputData):
    result = handle_input(data.message)
    return {"response": result}

app.include_router(meta.router)
app.include_router(feedback.router)
app.include_router(status.router)
app.include_router(trigger_enhance.router)
app.include_router(intent_infer.router)
app.include_router(loop_selector.router)
app.include_router(fallback_loop.router)
app.include_router(meta_monitor.router)
app.include_router(reinforcement_hook.router)
