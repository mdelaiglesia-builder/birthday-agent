from chunk_document import chunk_document
from embed_chunks import embed_chunks
from store_chunks import store_chunks
import argparse
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

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
        embeddings = embed_chunks(chunks, "documentp")
        store_chunks(chunks, embeddings)
        client = chromadb.CloudClient(os.environ["CHROMA_TENANT"], os.environ["CHROMA_DATABASE"], os.environ["CHROMA_API_KEY"])
        collection = client.get_or_create_collection(name="juan_birthday_kb")
        check("Size of collection is the same as chunks", collection.count() == len(chunks))

except FileNotFoundError:
    print(f"Error: file '{args.filepath}' not found.")