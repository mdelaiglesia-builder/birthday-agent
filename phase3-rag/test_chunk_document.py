from chunk_document import chunk_document
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
        check("Amount of chunks is 7", len(chunks) == 7)
        for c in chunks:
            check("Chunk starts with ##", c.startswith("## "))
except FileNotFoundError:
    print(f"Error: file '{args.filepath}' not found.")

content_without_headers = "no headers at all here, just plain text"
no_chunks = chunk_document(content_without_headers)
check("Amount of chunks when no header present is 1", len(no_chunks) == 1)
check("Chunk when no header present doesn't start with ##", not no_chunks[0].startswith("## "))
