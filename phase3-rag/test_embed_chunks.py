import os
import pytest

from chunk_document import chunk_document
from embed_chunks import embed_chunks

KB_PATH = os.path.join(os.path.dirname(__file__), "juan_birthday_notes.md")


@pytest.mark.skip(reason="Requires a real Voyage AI API call; the free tier's 3 RPM limit makes this unreliable in CI even with the voyage_pacing fixture's spacing (see conftest.py). Skipped rather than paced -- unskip locally to verify against the real API.")
def test_embed_chunks_on_real_kb(voyage_pacing):
    with open(KB_PATH) as f:
        content = f.read()
    chunks = chunk_document(content)
    embeddings = embed_chunks(chunks, "document")

    assert len(embeddings) == len(chunks)
    dimensions = len(embeddings[0])
    for e in embeddings:
        assert len(e) == dimensions
        assert all(isinstance(x, float) for x in e)
