# Research: RAG Retrieval Pipeline Testing

This document outlines the research and decisions made to resolve technical uncertainties for the RAG retrieval pipeline testing feature.

## 1. Qdrant Connection Details

### Decision
The script will connect to a Qdrant instance using the following default parameters:
- **Host**: `localhost`
- **Port**: `6333`
- **API Key**: `None`

These defaults assume a local Qdrant instance running in a development environment without authentication. The script should allow these to be overridden via environment variables or command-line arguments for flexibility.

### Rationale
Using local defaults simplifies the setup for developers and aligns with the free-tier infrastructure constraint from the project constitution. Providing overrides ensures the script is usable in other environments (staging, production) without code changes.

### Alternatives Considered
- Hardcoding the values: Rejected as it reduces flexibility.
- Requiring command-line arguments for all connection details: Rejected as it makes the script more cumbersome for the common local development case.

### Implementation (`qdrant-client`)
```python
from qdrant_client import QdrantClient

# Connection would be established as follows:
client = QdrantClient(host="localhost", port=6333)
```

## 2. Qdrant Collection Name

### Decision
The script will query a collection named `test_collection` by default. This will be an overridable parameter.

### Rationale
A default collection name simplifies local testing. `test_collection` is a clear and descriptive name for a collection used in a testing context.

## 3. Similarity Search

### Decision
The script will use the `qdrant_client.QdrantClient.search()` method to perform similarity searches. A sentence-transformer model (e.g., `'all-MiniLM-L6-v2'`) will be needed to encode the query text into a vector before sending it to Qdrant.

### Rationale
The `search()` method is the standard way to perform vector similarity searches in Qdrant. It is efficient and provides the necessary parameters to retrieve top-k results with their payloads. Using a sentence-transformer is a standard practice for creating query embeddings.

### Implementation (`qdrant-client`)
```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# 1. Initialize client and model
client = QdrantClient(host="localhost", port=6333)
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Encode the query
query_vector = encoder.encode("your query text").tolist()

# 3. Perform the search
hits = client.search(
    collection_name="test_collection",
    query_vector=query_vector,
    limit=5,  # 'k'
    with_payload=True  # To retrieve metadata
)
```
All `NEEDS CLARIFICATION` items from the plan are now resolved with these documented assumptions.
