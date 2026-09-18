import chromadb
from dotenv import load_dotenv
import os
from embed_chunks import embed_chunks

load_dotenv()

def retrieval(query: str) -> list[tuple[str, str]]:
    client = chromadb.CloudClient(tenant=os.environ["CHROMA_TENANT"], database=os.environ["CHROMA_DATABASE"], api_key=os.environ["CHROMA_API_KEY"])
    collection = client.get_or_create_collection(name="juan_birthday_kb")

    query_embedding = embed_chunks([query], "query")
    query_result = collection.query(query_embeddings=query_embedding, n_results=3)
    
    return list(zip(query_result["ids"][0], query_result["documents"][0]))

