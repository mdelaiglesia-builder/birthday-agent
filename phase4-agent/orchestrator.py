from typing import Any
from agent import Agent
import guest_lookup_subagent
import event_subagent

def get_text(response) -> str:
    return " ".join(b.text for b in response.content if b.type == "text")

async def call_orchestrator_tool(tool_use_block: Any) -> str:
    if (tool_use_block.name == "ask_guest_subagent"):
        messages = [{"role": "user", "content": tool_use_block.input["question"]}]
        guest_agent = await guest_lookup_subagent.build_guest_agent()
        response = await guest_agent.run(messages)
        return get_text(response)
    elif (tool_use_block.name == "ask_event_subagent"):
        messages = [{"role": "user", "content": tool_use_block.input["question"]}]
        event_agent = await event_subagent.build_event_agent()
        response = await event_agent.run(messages)
        return get_text(response)

async def get_orchestrator_tool_definition() -> list[dict[str, Any]]:
    return [
        {
        "name": "ask_guest_subagent",
        "description": "Route a question to Guest Subagent",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string"
                }
            },
            "required": ["question"]
        }},
        { 
        "name": "ask_event_subagent",
        "description": "Route a question to Event Subagent",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string"
                }
            },
            "required": ["question"]
        }
        }]

async def build_orchestrator_agent() -> Agent:
    tools_definitions = await get_orchestrator_tool_definition()
    system_prompt = ("Your job is to decide which subagent to call. "
                     "Event Subagent: Has general information related to the event. "
                     "Guest Subagent: Handles guest RSVP lookups and status updates.")

    return Agent(tools_definitions, system_prompt, call_orchestrator_tool)
