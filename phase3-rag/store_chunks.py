import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

def store_chunks(chunks: list[str], embeddings: list[list[float]]):
    client = chromadb.CloudClient(tenant=os.environ["CHROMA_TENANT"], database=os.environ["CHROMA_DATABASE"], api_key=os.environ["CHROMA_API_KEY"])
    collection = client.get_or_create_collection(name="juan_birthday_kb")
    ids = [str(i) for i, c in enumerate(chunks)] 
    collection.add(ids=ids, embeddings=embeddings, documents=chunks)