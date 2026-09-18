from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase4-agent"))
import orchestrator
import agent
import asyncio

app = FastAPI()

class AskRequest(BaseModel):
    message: str

def get_text(response) -> str:
    return " ".join(b.text for b in response.content if b.type == "text")

@app.post("/ask")
async def ask(request: AskRequest):
    messages = [{"role": "user", "content": request.message}]
    agent = await orchestrator.build_orchestrator_agent()
    response = await agent.run(messages)
    return {"agent": get_text(response)}