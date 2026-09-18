from typing import Any
from fastmcp import Client
from dotenv import load_dotenv
import psycopg2
from mcp_server import mcp
import pytest
import asyncio
from anthropic import Anthropic
from anthropic.types import Message
from agent import Agent
import os
import orchestrator

load_dotenv()

# @pytest.mark.asyncio
# async def test_list_mcp_tools():
#     tools_definitions = await get_mcp_tools_definition()
#     tools_definitions.append(await get_rag_tool_definition())
#     assert len(tools_definitions) == 4, "Not three tool definitions"
#     assert any(td["name"] == "get_guest" for td in tools_definitions)
#     assert any(td["name"] == "update_status" for td in tools_definitions)
#     assert any(td["name"] == "list_by_status" for td in tools_definitions)
#     assert any(td["name"] == "answer_question_about_juans_birthday" for td in tools_definitions)

# def get_guest_status(full_name: str) -> str:
#     with psycopg2.connect(os.environ["POSTGRESQL_DATABASE"]) as conn:
#         with conn.cursor() as cur:
#             cur.execute('SELECT status FROM "Invitations" WHERE full_name = %s', (full_name,))
#             row = cur.fetchone()
#     conn.close()
#     return row[0]

# def set_guest_status(full_name: str, status: str) -> None:
#     with psycopg2.connect(os.environ["POSTGRESQL_DATABASE"]) as conn:
#         with conn.cursor() as cur:
#             cur.execute('UPDATE "Invitations" SET status = %s WHERE full_name = %s', (status, full_name))
#     conn.close()

# @pytest.mark.asyncio
# async def test_create_message_with_mcp_tools():
#     original_status = get_guest_status("Tomás Roselli")
#     try:
#         messages = [{"role": "user", "content": "Tomás Roselli confirmed his attendance"}]
#         response = await run_agent(messages)
#         assert response.stop_reason == "end_turn"
#         assert get_guest_status("Tomás Roselli") == "confirmed"
#         print(response.content)
#     finally:
#         set_guest_status("Tomás Roselli", original_status)

@pytest.mark.asyncio
async def test_answer_from_rag_grounded():
    messages = [{"role": "user", "content": "where do people park?"}]
    agent = await orchestrator.build_orchestrator_agent()
    response = await agent.run(messages)
    assert response.stop_reason == "end_turn"
    assert any(word in get_text(response) for word in ["Parroquia San Ignacio de Loyola", "Molina Ciudad"])
    print(get_text(response))

# def test_answer_from_rag_ungrounded(monkeypatch):
#     monkeypatch.setattr("agent.judge", lambda *args, **kwargs: {"grounded": False, "reason": "test"})
#     answer = answer_from_rag("where do people park?")
#     assert answer == "ERROR: User query is out of scope"

@pytest.mark.asyncio
async def test_headcount():
    messages = [{"role": "user", "content": "How many guests have confirmed?"}]
    agent = await orchestrator.build_orchestrator_agent()
    response = await agent.run(messages)
    assert response.stop_reason == "end_turn"
    assert any(word in get_text(response) for word in ["RSVP", "confirmed"])
    print(get_text(response))

# @pytest.mark.asyncio
# async def test_follow_up():
#     messages = [{"role": "user", "content": "draft follow-up messages for everyone who hasn't responded yet"}]
#     response = await run_agent(messages)
#     assert response.stop_reason == "end_turn"
#     print(response.content)

# @pytest.mark.asyncio
# async def test_follow_up():
#     messages = [{"role": "user", "content": "draft personalized invite messages for everyone who hasn't been invited yet"}]
#     response = await run_agent(messages)
#     assert response.stop_reason == "end_turn"
#     print(response.content)

def get_text(response) -> str:
    return " ".join(b.text for b in response.content if b.type == "text")

# @pytest.mark.asyncio
# async def test_checklist():
#     messages = [{"role": "user", "content": "Give me a day-of checklist, including how many guests have confirmed so far and the event logistics."}]
#     response = await run_agent(messages)
#     assert response.stop_reason == "end_turn"
#     text = get_text(response)  # the helper from the grounded RAG test
#     assert any(word in text for word in ["confirmed", "guest"])  # guest-data side
#     assert any(word in text for word in ["food", "schedule", "venue", "party"])  # RAG side
#     print(response.content)

