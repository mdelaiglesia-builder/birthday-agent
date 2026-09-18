import os

import chromadb

from chunk_document import chunk_document
from embed_chunks import embed_chunks
from store_chunks import store_chunks

KB_PATH = os.path.join(os.path.dirname(__file__), "juan_birthday_notes.md")


def test_store_chunks_on_real_kb():
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
