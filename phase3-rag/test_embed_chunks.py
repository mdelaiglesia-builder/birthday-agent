from chunk_document import chunk_document
from embed_chunks import embed_chunks
import argparse

parser = argparse.ArgumentParser(description="KB of Juan's birthday")
parser.add_argument("filepath", help="Path to the file of the KB")
args = parser.parse_args()

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")

try:
    with open(args.filepath) as f:
        content = f.read()
        chunks = chunk_document(content)
        embeddings = embed_chunks(chunks,"document")
        check("The amount of embeddings is the same as the amount of chunks", len(chunks) == len(embeddings))
        dimensions = len(embeddings[0]) 
        for e in embeddings:
            check("Dimensionality consistency check", len(e) == dimensions)
            check("Every value of the vector is a floating number", all(isinstance(x, float) for x in e))

except FileNotFoundError:
    print(f"Error: file '{args.filepath}' not found.")