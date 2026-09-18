from anthropic import Anthropic
from anthropic.types import Message
from typing import Any, Callable, Awaitable

class Agent:
    def __init__(self, tools: list[dict[str, Any]], system_prompt: str, tool_handler: Callable[[Any], Awaitable[str]]):
        self.tools = tools
        self.system_prompt = system_prompt
        self.tool_handler = tool_handler

    async def create_message(self, messages: list[dict[str, Any]]):
        anthropic_client = Anthropic()

        return anthropic_client.messages.create(
            model = "claude-sonnet-5",
            max_tokens = 4096,
            tools = self.tools,
            tool_choice = {"type": "auto"},
            system = (self.system_prompt),
            messages = messages
        )

    async def run(self, messages: list[dict]) -> Message:
        response = await self.create_message(messages)
        while response.stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            tools_results: list[dict[str, Any]] = []
            for tool_use_block in tool_use_blocks:
                r: dict[str,Any] = {}
                r["type"] = "tool_result"
                r["tool_use_id"] = tool_use_block.id
                r["content"] = await self.tool_handler(tool_use_block)
                tools_results.append(r)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tools_results})
            response = await self.create_message(messages)
        return response

