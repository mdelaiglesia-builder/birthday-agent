import os

from chunk_document import chunk_document

KB_PATH = os.path.join(os.path.dirname(__file__), "juan_birthday_notes.md")


def test_chunk_document_on_real_kb():
    with open(KB_PATH) as f:
        content = f.read()
    chunks = chunk_document(content)
    assert len(chunks) == 6
    for chunk in chunks:
        assert chunk.startswith("## ")


def test_chunk_document_no_headers():
    content_without_headers = "no headers at all here, just plain text"
    chunks = chunk_document(content_without_headers)
    assert len(chunks) == 1
    assert not chunks[0].startswith("## ")
