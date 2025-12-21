# Data Model: Embedding Pipeline

## Entities

### Document
- **id**: string (unique identifier for the document)
- **url**: string (source URL of the document)
- **title**: string (title extracted from the document)
- **content**: string (clean text content extracted from the URL)
- **created_at**: timestamp (when the document was processed)
- **metadata**: dict (additional metadata from the source)

### Chunk
- **id**: string (unique identifier for the chunk, typically derived from document id)
- **document_id**: string (reference to parent document)
- **content**: string (chunked text content)
- **chunk_index**: integer (position of the chunk in the original document)
- **metadata**: dict (metadata including source URL, title, and chunk-specific info)

### Embedding
- **id**: string (unique identifier for the embedding)
- **chunk_id**: string (reference to the source chunk)
- **vector**: list[float] (the embedding vector from Cohere)
- **created_at**: timestamp (when the embedding was generated)
- **metadata**: dict (metadata including source URL, document title, and other context)

### CrawlConfig
- **urls**: list[string] (list of URLs to crawl)
- **sitemap_url**: string (URL to the sitemap.xml file, e.g., https://hackathon-in-classnew.vercel.app/sitemap.xml)
- **max_depth**: integer (maximum depth for crawling, default 1 for single URLs)
- **rate_limit**: float (requests per second limit)
- **allowed_domains**: list[string] (domains allowed for crawling)
- **content_filters**: dict (filters for content selection)

## Qdrant Collection Schema: New_Rag_Data

### Payload Structure
- **document_id**: string (ID of the source document)
- **chunk_id**: string (ID of the source chunk)
- **url**: string (source URL)
- **title**: string (document title)
- **chunk_index**: integer (position in document)
- **content**: string (the actual text content of the chunk)
- **created_at**: string (timestamp)

### Vector Configuration
- **Vector Size**: 1024 (Cohere's embed-multilingual-v2.0 model dimension)
- **Distance Metric**: Cosine similarity

## Relationships
- Document 1 -- * Chunk (one document can have multiple chunks)
- Chunk 1 -- 1 Embedding (one chunk generates one embedding)
- CrawlConfig 1 -- * Document (one configuration can produce multiple documents)