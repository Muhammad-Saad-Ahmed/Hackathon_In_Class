# Research: Embedding Pipeline Implementation

## Decision: Backend folder structure and UV package management
**Rationale**: Following user requirement to create backend folder and initialize project with UV package. UV is a modern Python package manager that provides fast, reproducible environments.
**Alternatives considered**: pip + virtualenv, Poetry, Conda
**Chosen approach**: UV for its speed and compatibility with modern Python packaging

## Decision: Cohere and Qdrant client setup
**Rationale**: User specifically requested setup of Cohere and Qdrant clients for the embedding pipeline
**Alternatives considered**: OpenAI embeddings, Pinecone, Weaviate
**Chosen approach**: Cohere for embeddings and Qdrant for vector storage as specified in requirements

## Decision: Sitemap for URL discovery
**Rationale**: Need to discover all URLs from the deployed Docusaurus site at https://hackathon-in-classnew.vercel.app/ efficiently
**Alternatives considered**: Manual URL listing, web crawling, sitemap parsing
**Chosen approach**: Sitemap parsing as Docusaurus sites typically provide sitemap.xml for SEO

## Decision: Text extraction from Docusaurus URLs
**Rationale**: Need to extract clean text from deployed URLs at https://hackathon-in-classnew.vercel.app/
**Alternatives considered**: Selenium for dynamic content, requests + BeautifulSoup for static content
**Chosen approach**: requests + BeautifulSoup for efficiency and simplicity

## Decision: Content chunking strategy
**Rationale**: Large documents need to be chunked to fit within Cohere's token limits and for better retrieval
**Alternatives considered**: Fixed character length, semantic chunking, sentence-based chunking
**Chosen approach**: Fixed character length with overlap to maintain context

## Decision: Qdrant collection naming
**Rationale**: User specifically requested collection named "New_Rag_Data"
**Alternatives considered**: Default naming, date-stamped collections
**Chosen approach**: "New_Rag_Data" as specified

## Decision: Single file implementation (main.py)
**Rationale**: User requested all functionality in one file named main.py
**Alternatives considered**: Modular approach with separate files for each function
**Chosen approach**: Single file with all functions as specified

## Required Functions Implementation:
1. `get_all_urls` - Fetch all URLs from the deployed Docusaurus site
2. `extract_text_from_url` - Extract clean text content from a URL
3. `chunk_text` - Split text into manageable chunks
4. `embed` - Generate embeddings using Cohere
5. `create_collection` - Create Qdrant collection named "New_Rag_Data"
6. `save_chunk_to_qdrant` - Store embeddings with metadata in Qdrant
7. `main` - Execute the complete pipeline

## Architecture Overview:
```
[URLs] -> [Text Extraction] -> [Chunking] -> [Embedding] -> [Qdrant Storage]
   |           |                |            |                |
   v           v                v            v                v
Input    Cleaning &         Size           Vector        Vector Database
Source   Parsing          Management      Generation     Storage & Retrieval
```

## Dependencies to install with UV:
- cohere
- qdrant-client
- beautifulsoup4
- requests
- python-dotenv (for API key management)