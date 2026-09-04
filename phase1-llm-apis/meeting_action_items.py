import argparse
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

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

parser = argparse.ArgumentParser(description="Meeting notes file")
parser.add_argument("filepath", help="Path to the file to analyze")
args = parser.parse_args()

try:
    with open(args.filepath) as f:
        content = f.read()
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "tool", "name": "extract_meeting_action_items"},
            temperature=0,
            system="Extract action items from the meeting notes.",
            messages=[
                {"role": "user", "content": content}
            ]
        )
        for a in message.content[0].input["action_items"]:
            if (a["owner"] is not None):
                print(f"- {a['task']} ({a['owner']})")
            else:
                print(f"- {a['task']} (unassigned)")
except FileNotFoundError:
    print(f"Error: file '{args.filepath}' not found.")