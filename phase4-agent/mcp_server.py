from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, Literal, TypedDict

load_dotenv()

mcp = FastMCP("My MCP Server")

class UpdateResult(TypedDict):
    updated: bool
    reason: Literal["success", "no_match", "ambiguous"]
    candidates: list[dict[str, Any]]

@mcp.tool
def get_guest(name: str) -> list[dict[str, Any]]:
    """Get guests by full name."""
    with psycopg2.connect(os.environ["POSTGRESQL_DATABASE"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT *, similarity(full_name, %s) AS score FROM "Invitations" WHERE similarity(full_name, %s) > 0.3 ORDER BY score DESC', (name,name,))
            records = cur.fetchall()
    conn.close()    
    return records
    
@mcp.tool
def update_status(name: str, status: Literal["not_invited", "pending", "confirmed", "declined"]) -> UpdateResult:
    """Update status of a guest."""
    with psycopg2.connect(os.environ["POSTGRESQL_DATABASE"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT *, similarity(full_name, %s) AS score FROM "Invitations" WHERE similarity(full_name, %s) > 0.3 ORDER BY score DESC', (name,name,))
            records = cur.fetchall()
            candidates = [r for r in records if r["score"] >= 0.8]
            update_result = UpdateResult()
            if (len(candidates) == 0):
                update_result["updated"] = False
                update_result["reason"] = "no_match"
                update_result["candidates"] = []

            elif (len(candidates) == 1):
                cur.execute('UPDATE "Invitations" SET status = %s WHERE full_name = %s', (status,candidates[0]["full_name"],))
                update_result["updated"] = True
                update_result["reason"] = "success"
                update_result["candidates"] = candidates

            elif (len(candidates) > 1):
                update_result["updated"] = False
                update_result["reason"] = "ambiguous"
                update_result["candidates"] = candidates
    conn.close()
    return update_result

@mcp.tool
def list_by_status(status: Literal["not_invited", "pending", "confirmed", "declined"]) -> list[dict[str, Any]]:
    """List guests by status."""
    with psycopg2.connect(os.environ["POSTGRESQL_DATABASE"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM "Invitations" WHERE status = %s', (status,))
            records = cur.fetchall()
    conn.close()
    return records
    
if __name__ == "__main__":
    mcp.run()