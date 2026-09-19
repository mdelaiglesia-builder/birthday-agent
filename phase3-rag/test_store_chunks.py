import os
import pytest

import chromadb

from chunk_document import chunk_document
from embed_chunks import embed_chunks
from store_chunks import store_chunks

KB_PATH = os.path.join(os.path.dirname(__file__), "juan_birthday_notes.md")


@pytest.mark.skip(reason="Requires a real Voyage AI API call; the free tier's 3 RPM limit makes this unreliable in CI even with the voyage_pacing fixture's spacing (see conftest.py). Skipped rather than paced -- unskip locally to verify against the real API.")
def test_store_chunks_on_real_kb(voyage_pacing):
    with open(KB_PATH) as f:
        content = f.read()
    chunks = chunk_document(content)
    embeddings = embed_chunks(chunks, "document")
    store_chunks(chunks, embeddings)

    client = chromadb.CloudClient(
        tenant=os.environ["CHROMA_TENANT"],
        database=os.environ["CHROMA_DATABASE"],
        api_key=os.environ["CHROMA_API_KEY"],
    )
    collection = client.get_or_create_collection(name="juan_birthday_kb")
    assert collection.count() == len(chunks)
