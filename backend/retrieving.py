import typer
import os
import json
from typing import List, Union
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class RetrievalResult(BaseModel):
    text: str
    url: str
    chunk_id: Union[int, str] = Field(..., alias="chunkId")
    score: float

app = typer.Typer()

def get_qdrant_client():
    host = os.environ.get("QDRANT_HOST", "localhost")
    port = int(os.environ.get("QDRANT_PORT", 6333))
    client = QdrantClient(host=host, port=port)
    return client

def process_hits(hits) -> List[RetrievalResult]:
    results = []
    for hit in hits:
        payload = hit.payload or {}
        metadata = payload.get("metadata", {})
        results.append(
            RetrievalResult(
                text=payload.get("text", ""),
                url=metadata.get("url", ""),
                chunkId=metadata.get("chunk_id", ""),
                score=hit.score,
            )
        )
    return results

@app.command()
def retrieve(query: str = typer.Option(..., "--query", help="The query string.")):
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
    
    # Use Pydantic's serialization capabilities
    json_output = json.dumps([r.model_dump(by_alias=True) for r in results], indent=2)
    print(json_output)


if __name__ == "__main__":
    app()
