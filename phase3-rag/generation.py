from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Any

load_dotenv()

def generation(query: str, chunks: list[tuple[str, str]]) -> dict[str, Any]:
    client = Anthropic()

    tools = [
        {
            "name": "answer_question_about_juans_birthday",
            "description": "Get answer to a question about Juan's birthday",
            "input_schema": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string"
                    },
                    "chunks_used": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "chunk_id": {"type": "string"}
                            },
                            "required": ["chunk_id"]
                        }
                    }
                },
                "required": ["answer", "chunks_used"]
            }
        }
    ]

    new_query: str = ""

    for chunk_id, document in chunks:
        new_query += "[chunk_id: " + chunk_id + "]\n"
        new_query += document

    new_query += "Answer the question: " + query + "\n" 

    new_query += "Answer only using the provided chunks, not your own general knowledge, and cite the id(s) of whichever chunk(s) you use"

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "tool", "name": "answer_question_about_juans_birthday"},
        system=(
            "You are answering a question directly for a guest of Juan's birthday/baptism, "
            "on behalf of the event organizer. Answer naturally and conversationally, as if "
            "speaking to them directly. Never mention 'chunks', 'documents', 'provided text', "
            "or anything about how you retrieved the information. If the available information "
            "doesn't answer the question, say so briefly and naturally \u2014 e.g. 'I don't have "
            "that information' \u2014 without describing what you were or weren't given."
        ),
        messages=[
            {"role": "user", "content": new_query}
        ]
    )

    return message.content[0].input


    