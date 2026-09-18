def chunk_document(text: str) -> list[str]:
    # split text into chunks, one per "## " section
    # each chunk should keep its own header
    chunks: list[str] = []
    pieces = text.split("## ")
    if (len(pieces) > 1):
        pieces.pop(0)
        for p in pieces:
            p = "## " + p
            chunks.append(p)
    else:
        chunks = pieces

    return chunks

