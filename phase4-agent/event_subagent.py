from typing import Any
from agent import Agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase3-rag"))
from retrieval import retrieval
from generation import generation
from judge import judge

async def get_rag_tool_definition() -> list[dict[str, Any]]:
    return [{
        "name": "answer_question_about_juans_birthday",
        "description": "Get answer to a question about Juan's birthday",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }}]
    
def answer_from_rag(query: str) -> str:
    chunks_retrieved = retrieval(query)
    result = generation(query, chunks_retrieved)
    judge_response: dict[str, Any] = judge(query, chunks_retrieved, result["answer"], result["chunks_used"])

    if judge_response["grounded"]:
        return result["answer"]
    else:
        return "ERROR: User query is out of scope"

async def call_event_tool(tool_use_block: Any) -> str:
    return answer_from_rag(tool_use_block.input["query"])

async def build_event_agent():
    tools_definitions = await get_rag_tool_definition()
    system_prompt = ("You have to give information related to the event. "
                    "Never mention 'chunks', 'documents', 'provided text', "
                    "or anything about how you retrieved the information. "
                    "Report findings factually and concisely; your output will "
                    "be read by another AI system, not the end user directly.")

    return Agent(tools_definitions, system_prompt, call_event_tool)
