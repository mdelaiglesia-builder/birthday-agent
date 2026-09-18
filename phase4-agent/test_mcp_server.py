from mcp_server import mcp
import asyncio
from fastmcp import Client
import pytest
from fastmcp.exceptions import ToolError
from typing import Any, Literal, TypedDict

@pytest.mark.asyncio
async def test_get_guest():
    async with Client(mcp) as client:
        result = await client.call_tool("get_guest", {"name": "Noelia Lloret"})
        assert result.data[0]["full_name"] == "Noelia Lloret", "Existent guest not found"

@pytest.mark.asyncio
async def test_get_nonexistent_guest():
    async with Client(mcp) as client:
        result = await client.call_tool("get_guest", {"name": "Victor Cerqueiro"})
        assert len(result.data) == 0, "Nonexistent guest found"

@pytest.mark.asyncio
async def test_get_ambiguous_guest():
    async with Client(mcp) as client:
        result = await client.call_tool("get_guest", {"name": "JoaquinTomás Roselli"})
        assert any(d["full_name"] == "Joaquín Roselli" for d in result.data), "Similar guest not found"
        assert any(d["full_name"] == "Tomás Roselli" for d in result.data), "Similar guest not found"
        assert not any(d["full_name"] == "Noelia Lloret" for d in result.data), "Not similar guest not found"

@pytest.mark.asyncio
async def test_update_status():
    async with Client(mcp) as client:
        result = await client.call_tool("update_status", {"name": "Tomás Roselli", "status": "pending"})
        assert result.data.updated == True, "Guest status couldn't be updated"
        assert result.data.reason == "success", "Guest status update didn't finished successfully"
        assert result.data.candidates[0]["full_name"] == "Tomás Roselli", "Guest with status updated is incorrect"

@pytest.mark.asyncio
async def test_update_with_nonexistent_status():
    async with Client(mcp) as client:
        with pytest.raises(ToolError) as e:
            result = await client.call_tool("update_status", {"name": "Tomás Roselli", "status": "maybe"})
        assert "Input should be 'not_invited', 'pending', 'confirmed' or 'declined'" in str(e.value), "Exception message is incorrect"

@pytest.mark.asyncio
async def test_list_by_status_pending():
    async with Client(mcp) as client:
        result = await client.call_tool("list_by_status", {"status": "pending"})
        assert any(d["full_name"] == "Tomás Roselli" for d in result.data), "Guest with status pending not found"
        assert all(d["full_name"] != "Joaquín Roselli" for d in result.data), "Guest with status not pending found"
        assert all(d["status"] == "pending" for d in result.data), "Guest with status not pending found"

@pytest.mark.asyncio
async def test_list_by_status_empty():
    async with Client(mcp) as client:
        result = await client.call_tool("list_by_status", {"status": "declined"})
        assert len(result.data) == 0, "Guests with unexpected status"

@pytest.mark.asyncio
async def test_list_by_nonexistent_status():
    async with Client(mcp) as client:
        with pytest.raises(ToolError) as e:
            result = await client.call_tool("list_by_status", {"status": "maybe"})
        assert "Input should be 'not_invited', 'pending', 'confirmed' or 'declined'" in str(e.value), "Exception message is incorrect"
