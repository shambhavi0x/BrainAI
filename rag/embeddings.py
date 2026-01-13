from sentence_transformers import SentenceTransformer

def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")
