import voyageai
from dotenv import load_dotenv

load_dotenv()

def embed_chunks(chunks: list[str], input_type: str) -> list[list[float]]:
    vo = voyageai.Client()
    documents_embeddings = vo.embed(chunks, model="voyage-4-large", input_type=input_type).embeddings
    return documents_embeddings

