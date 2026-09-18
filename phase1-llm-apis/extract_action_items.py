from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def extract_action_items(notes_text: str) -> list[dict]:
    client = Anthropic()

    tools = [
        {
            "name": "extract_meeting_action_items",
            "description": "Extract a meeting's action items",
            "input_schema": {
                "type": "object",
                "properties": {
                    "action_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string"},
                                "owner": {"type": ["string", "null"]}
                            },
                            "required": ["task", "owner"]
                        }
                    }
                },
                "required": ["action_items"]
            }
        }
    ]

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "tool", "name": "extract_meeting_action_items"},
        system="Extract action items from the meeting notes.",
        messages=[
            {"role": "user", "content": notes_text}
        ]
    )

    return message.content[0].input["action_items"]