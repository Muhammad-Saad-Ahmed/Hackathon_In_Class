# Data Model: RAG Retrieval Testing

This document defines the key data entities for the RAG retrieval testing feature, based on the feature specification.

## Entities

### 1. Query

Represents the input from the user to the retrieval system.

-   **Type**: `string`
-   **Description**: A text string representing the user's question or topic of interest.
-   **Example**: `"What are the core principles of Spec-Driven Development?"`

### 2. DocumentChunk

Represents a piece of text content retrieved from the Qdrant vector store.

-   **Type**: `object`
-   **Fields**:
    -   `id`: `string` (UUID) - The unique identifier of the vector in Qdrant.
    -   `payload`: `object` - The data associated with the vector, which contains the text and metadata.
        -   `text`: `string` - The original text content of the chunk.
        -   `metadata`: `object` - See `Metadata` entity below.
    -   `score`: `float` - The similarity score of the chunk relative to the query.

### 3. Metadata

Represents the metadata associated with a `DocumentChunk`.

-   **Type**: `object`
-   **Fields**:
    -   `url`: `string` - The source URL of the document from which the chunk was extracted.
    -   `chunk_id`: `integer` or `string` - A unique identifier for the chunk within its source document.

### 4. RetrievalResult

Represents the final, structured output of the retrieval script.

-   **Type**: `array` of `object`
-   **Description**: A list of the top-k retrieved document chunks, formatted for clean JSON output.
-   **Object Structure**:
    -   `text`: `string` - The text of the retrieved chunk.
    -   `url`: `string` - The source URL from the metadata.
    -   `chunk_id`: `integer` or `string` - The chunk identifier from the metadata.
    -   `score`: `float` - The similarity score.
