
from fastmcp import Client
from mcp_server import mcp
from typing import Any
from agent import Agent

async def get_mcp_tools_definition() -> list[dict[str, Any]]:
    async with Client(mcp) as client: tools = await client.list_tools()
    tools_definition: list[dict[str, Any]] = []
    for t in tools:
        d: dict[str,Any] = {}
        d["name"] = t.name
        d["description"] = t.description
        d["input_schema"] = t.input_schema
        tools_definition.append(d)
    
    return tools_definition

async def call_guest_tool(tool_use_block: Any) -> str:
    async with Client(mcp) as mcp_client:
        result = await mcp_client.call_tool(tool_use_block.name, tool_use_block.input)
    return str(result.data)

async def build_guest_agent():
    tools_definitions = await get_mcp_tools_definition()
    system_prompt = ("You handle guest RSVP lookups and status updates only. "
    "Report findings factually and concisely; your output will "
    "be read by another AI system, not the end user directly.")

    return Agent(tools_definitions, system_prompt, call_guest_tool)
