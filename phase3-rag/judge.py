from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Any

load_dotenv()

def judge(query: str, chunks: list[tuple[str, str]], answer: str, chunks_used: list[dict[str, str]]) -> dict[str, Any]:
    client = Anthropic()

    tools = [
        {
            "name": "judge_answer_to_a_question_about_juans_birthday",
            "description": "Judge the answer to a question about Juan's birthday",
            "input_schema": {
                "type": "object",
                "properties": {
                    "grounded": {
                        "type": "boolean"
                    },
                    "reason": {
                        "type": "string",
                    }
                },
                "required": ["grounded", "reason"]
            }
        }
    ]

    new_query: str = "Available chunks:\n"
    
    for chunk_id, document in chunks:
        new_query += "[chunk_id: " + chunk_id + "]\n"
        new_query += document
    new_query += "\n"

    new_query += "Chunks used:\n"
    chunks_used_ids = [d["chunk_id"] for d in chunks_used]

    for chunk_id in chunks_used_ids:
        new_query += "[chunk_id: " + chunk_id + "]\n"
    new_query += "\n"    

    new_query += "Question:\n"
    new_query += query + "\n"

    new_query += "Answer:\n"
    new_query += answer + "\n"
    
    new_query += "Judge the answer to a question about Juan's birthday, tell if it's grounded or not (consider available chunks and chunks used) and why." + "\n" 

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "tool", "name": "judge_answer_to_a_question_about_juans_birthday"},
        system="Judge answers to questions about Juan's birthday",
        messages=[
            {"role": "user", "content": new_query}
        ]
    )

    return message.content[0].input


    