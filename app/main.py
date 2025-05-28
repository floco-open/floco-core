# app/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from judgment_loop.memoryless_core import handle_input

app = FastAPI()

class InputData(BaseModel):
    message: str

@app.post("/judgment")
async def judgment(data: InputData):
    result = handle_input(data.message)
    return {"response": result}
