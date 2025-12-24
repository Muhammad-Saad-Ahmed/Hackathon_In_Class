"""
This module contains the RAG agent implementation.
"""
import os
from typing import List, Union
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
import google.generativeai as genai
import typer
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from phr_generator import PHRGenerator
import json

load_dotenv()
# Configure Gemini
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=gemini_api_key)

app = typer.Typer()

class DocumentChunk(BaseModel):
    """
    Represents a chunk of a document retrieved from the vector database.
    """
    text: str
    url: str
    chunk_id: Union[int, str] = Field(..., alias="chunkId")
    score: float

def get_qdrant_client() -> QdrantClient:
    """
    Returns a Qdrant client.
    """
    host = os.environ.get("QDRANT_HOST", "localhost")
    port = int(os.environ.get("QDRANT_PORT", 6333))
    client = QdrantClient(host=host, port=port)
    return client

def process_hits(hits: list) -> List[DocumentChunk]:
    """
    Processes the hits from a Qdrant search.
    """
    results = []
    for hit in hits:
        payload = hit.payload or {}
        metadata = payload.get("metadata", {})
        results.append(
            DocumentChunk(
                text=payload.get("text", ""),
                url=metadata.get("url", ""),
                chunkId=metadata.get("chunk_id", ""),
                score=hit.score,
            )
        )
    return results

def retrieve_documents(query: str) -> List[DocumentChunk]:
    """
    Retrieves document chunks from a Qdrant collection based on a query.
    """
    client = get_qdrant_client()
    encoder = SentenceTransformer('all-MiniLM-L6-v2')

    query_vector = encoder.encode(query).tolist()

    collection_name = os.environ.get("QDRANT_COLLECTION", "test_collection")
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5,
        with_payload=True,
    )
    
    results = process_hits(hits)
    return results

def run_agent(query: str, command: str):
    """
    Runs the RAG agent.
    """
    if not query:
        print("Error: Query cannot be empty.")
        return

    documents = retrieve_documents(query)
    
    if not documents:
        print("Could not find an answer to your question.")
        return

    context = "\n".join([doc.text for doc in documents])
    
    prompt = f"Based on the following context, please answer the question.\n\nContext:\n{context}\n\nQuestion:\n{query}"
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    answer = response.text
    
    print("Answer:")
    print(answer)
    print("\nSources:")
    for doc in documents:
        print(f"- {doc.url} (Score: {doc.score:.4f})")

    # Generate PHR
    phr_generator = PHRGenerator()
    phr_filepath = phr_generator.generate_phr(
        prompt_text=query,
        response_text=answer,
        title="RAG Agent Query",
        stage="general",
        model="gemini-pro",
        command=command,
        files_yaml=[doc.url for doc in documents],
        outcome_impact="RAG agent response to user query.",
        files_summary=json.dumps([{"url": doc.url, "score": doc.score} for doc in documents]),
    )
    print(f"\nPHR generated at: {phr_filepath}")

@app.command()
def main(query: str = typer.Option(..., "--query", help="The query string.")):
    """
    Main function to run the RAG agent.
    """
    command_str = f"python backend/agent.py --query '{query}'"
    run_agent(query, command_str)

if __name__ == "__main__":
    app()
