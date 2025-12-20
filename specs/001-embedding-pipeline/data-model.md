# Data Model: Embedding Pipeline

## Entities

### Document Content
- **Fields**:
  - `url`: string (source URL of the document)
  - `title`: string (page title extracted from HTML)
  - `content`: string (cleaned text content)
  - `created_at`: datetime (timestamp when content was extracted)
  - `chunk_index`: integer (position of chunk in original document)

- **Validation**:
  - URL must be valid and accessible
  - Content must not be empty after cleaning
  - Title should not exceed 500 characters

### Embedding Vector
- **Fields**:
  - `vector`: list[float] (numerical representation from Cohere)
  - `dimension`: integer (size of the embedding vector)
  - `model`: string (name of the model used to generate embedding)

- **Validation**:
  - Vector must have consistent dimensions across all embeddings
  - Model name must match expected Cohere model

### Qdrant Record
- **Fields**:
  - `id`: string (unique identifier for the record)
  - `payload`: dict (metadata including URL, title, content snippet)
  - `vector`: list[float] (embedding vector)
  - `collection`: string (name of Qdrant collection - "rag_embedding")

- **Validation**:
  - ID must be unique within collection
  - Payload must contain required metadata fields
  - Vector must match collection's expected dimensions

## Relationships

- One Document Content → Many Embedding Vectors (when document is chunked)
- One Embedding Vector → One Qdrant Record (one-to-one mapping for storage)

## State Transitions

### Document Processing States
1. `pending` → `extracting` → `cleaning` → `chunking` → `embedding` → `storing` → `completed`
2. Any step can transition to `failed` state with error details

## Data Flow

1. Raw HTML from URL → Extracted Content → Cleaned Content → Chunked Content → Embedding Vector → Qdrant Record
2. Each transformation step validates data before passing to the next