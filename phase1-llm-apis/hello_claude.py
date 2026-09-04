from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

tools = [
    {
        "name": "extract_person",
        "description": "Extract a person's name and role from text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "role": {"type": "string"}
            },
            "required": ["name", "role"]
        }
    }
]

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_person"},
    temperature=0,
    system="Extract the person's name and role from the text. Respond with ONLY valid JSON, no other text, in the form: {\"name\": \"...\", \"role\": \"...\"}",
    messages=[
        {"role": "user", "content": "Hi, I'm Matías, an engineering manager transitioning into AI engineering."}
    ]
)

tool_use_block = message.content[0]
print(tool_use_block.input)
print(tool_use_block.input["name"])