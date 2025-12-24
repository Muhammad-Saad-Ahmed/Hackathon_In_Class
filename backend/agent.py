"""
This module contains the RAG agent implementation.
"""
import os
from typing import List, Union, Optional
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
import google.generativeai as genai
import typer
from sentence_transformers import SentenceTransformer
import cohere # Import cohere
from dotenv import load_dotenv
from phr_generator import PHRGenerator
import json

load_dotenv()
# Configure Gemini
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=gemini_api_key)

# Configure Cohere
cohere_api_key = os.environ.get("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable not set.")
co = cohere.Client(cohere_api_key) # Initialize Cohere Client

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
    host = os.environ.get("QDRANT_HOST")
    api_key = os.environ.get("QDRANT_API_KEY")
    
    if not host:
        raise ValueError("QDRANT_HOST environment variable not set. Please set it to your Qdrant cloud URL.")

    # Remove protocol prefix if present, as QdrantClient expects the URL without it in the 'host' param
    # or expects full URL in 'url' param. Here we use 'url' param.
    if host.startswith("http://"):
        host = host[len("http://"):]
    elif host.startswith("https://"):
        host = host[len("https://"):]

    client = QdrantClient(url=host, api_key=api_key)
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

def retrieve_documents(query: str, collection_name_arg: Optional[str] = None) -> List[DocumentChunk]:
    """
    Retrieves document chunks from a Qdrant collection based on a query.
    """
    client = get_qdrant_client()
    # Use Cohere for embedding
    response = co.embed(
        texts=[query],
        model="embed-english-v3.0", # Using Cohere Embed v3 - English which outputs 1024 dim
        input_type="search_query"
    )
    query_vector = response.embeddings[0]

    collection_name = os.environ.get("QDRANT_COLLECTION", "New_Rag_Data")
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5,
        with_payload=True,
    )
    
    results = process_hits(hits)
    return results

def run_agent(query: str, command: str, qdrant_host: Optional[str] = None, qdrant_api_key: Optional[str] = None, qdrant_collection: Optional[str] = None):
    """
    Runs the RAG agent.
    """
    if not query:
        print("Error: Query cannot be empty.")
        return

    documents = retrieve_documents(query, collection_name_arg=qdrant_collection)
    
    if not documents:
        print("Could not find an answer to your question.")
        return

    context = "\n".join([doc.text for doc in documents])
    
    prompt = f"Based on the following context, please answer the question.\n\nContext:\n{context}\n\nQuestion:\n{query}"
    
    model = genai.GenerativeModel('gemini-2.5-flash')
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
def main(
    query: str = typer.Option(..., "--query", help="The query string."),
    qdrant_host: Optional[str] = typer.Option(None, "--qdrant-host", help="Qdrant host URL."),
    qdrant_api_key: Optional[str] = typer.Option(None, "--qdrant-api-key", help="Qdrant API key."),
    qdrant_collection: Optional[str] = typer.Option(None, "--qdrant-collection", help="Qdrant collection name."),
):
    """
    Main function to run the RAG agent.
    """
    command_str = f"python backend/agent.py --query '{query}'"
    if qdrant_host:
        command_str += f" --qdrant-host '{qdrant_host}'"
    if qdrant_api_key:
        command_str += f" --qdrant-api-key '********'" # Mask API key in command string
    if qdrant_collection:
        command_str += f" --qdrant-collection '{qdrant_collection}'"

    run_agent(
        query,
        command_str,
        qdrant_host=qdrant_host,
        qdrant_api_key=qdrant_api_key,
        qdrant_collection=qdrant_collection
    )

if __name__ == "__main__":
    app()
