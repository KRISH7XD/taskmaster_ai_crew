import chromadb
from langchain_openai import OpenAIEmbeddings
from config import OPENROUTER_API_KEY


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("taskmaster_memory")


embedder = OpenAIEmbeddings(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="meta-llama/llama-4-maverick"
)

def add_to_memory(content, task_id):
    embedding = embedder.embed_query(content)
    collection.add(
        documents=[content],
        embeddings=[embedding],
        ids=[task_id]
    )
    return f"Added to memory: {task_id}"

def retrieve_from_memory(query):
    embedding = embedder.embed_query(query)
    results = collection.query(query_embeddings=[embedding], n_results=1)
    if results["documents"]:
        return results["documents"][0][0]
    return "No relevant memory found."