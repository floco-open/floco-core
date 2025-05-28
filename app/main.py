# app/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from judgment_loop.memoryless_core import handle_input
from app.routes import meta
from app.routes import feedback
from app.routes import status

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
