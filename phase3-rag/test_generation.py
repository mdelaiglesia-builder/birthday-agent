from typing import Any
import pytest

from generation import generation
from judge import judge
from retrieval import retrieval


@pytest.mark.skip(reason="Requires a real Voyage AI API call; the free tier's 3 RPM limit makes this unreliable in CI even with the voyage_pacing fixture's spacing (see conftest.py). Skipped rather than paced -- unskip locally to verify against the real API.")
def test_generation_and_judge_grounded_for_parking_question(voyage_pacing):
    query = "where's parking?"
    chunks_retrieved = retrieval(query)
    generation_response: dict[str, Any] = generation(query, chunks_retrieved)

    assert generation_response["answer"]
    assert generation_response["chunks_used"]

    chunks_used_ids = [d["chunk_id"] for d in generation_response["chunks_used"]]
    chunks_retrieved_ids = [chunk_id for chunk_id, document in chunks_retrieved]
    assert all(used_id in chunks_retrieved_ids for used_id in chunks_used_ids)

    judge_response: dict[str, Any] = judge(
        query,
        chunks_retrieved,
        generation_response["answer"],
        generation_response["chunks_used"],
    )
    assert judge_response["grounded"]
