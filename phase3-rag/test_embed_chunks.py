import os

from chunk_document import chunk_document
from embed_chunks import embed_chunks

KB_PATH = os.path.join(os.path.dirname(__file__), "juan_birthday_notes.md")


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
