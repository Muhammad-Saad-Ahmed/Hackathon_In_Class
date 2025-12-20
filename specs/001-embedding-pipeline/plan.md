# Implementation Plan: Embedding Pipeline Setup

**Branch**: `001-embedding-pipeline` | **Date**: 2025-12-20 | **Spec**: [specs/001-embedding-pipeline/spec.md](../001-embedding-pipeline/spec.md)
**Input**: Feature specification from `/specs/001-embedding-pipeline/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an embedding pipeline that extracts text from deployed Docusaurus URLs (specifically the deployed site at https://hackathone-late-1.vercel.app/), generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval. The implementation will be contained in a single main.py file with specific functions for URL crawling, text extraction, content chunking, embedding generation, and vector storage.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Cohere client library, Qdrant client library, requests, beautifulsoup4, python-dotenv, uv (for package management)
**Storage**: Qdrant vector database (remote)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (backend service)
**Project Type**: Single backend service
**Performance Goals**: Process typical documentation page within 10 seconds (per spec requirement SC-002)
**Constraints**: Must handle API rate limiting for web crawling and Cohere requests, support up to 1000 pages (per spec requirement SC-005)
**Scale/Scope**: Single deployed service to process documentation sites

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution (which is currently using a template), the implementation follows standard practices:
- Will implement test-first approach with pytest
- Will focus on observability with structured logging
- Will maintain simplicity with a single-file implementation as requested
- Will handle errors gracefully as specified in functional requirements

## System Architecture

### Overview
The embedding pipeline follows a single-file service architecture that processes Docusaurus documentation sites by crawling URLs, extracting content, generating embeddings, and storing them in a vector database for RAG applications.

### Components
- **URL Crawler**: Discovers and collects all valid URLs from the target Docusaurus site
- **Content Extractor**: Extracts clean text content from HTML pages, removing navigation elements
- **Text Chunker**: Splits large documents into smaller chunks suitable for embedding
- **Embedding Generator**: Uses Cohere API to convert text chunks into vector embeddings
- **Vector Storage**: Stores embeddings in Qdrant with metadata for retrieval
- **Pipeline Orchestrator**: Coordinates the entire process from start to finish

### Data Flow
1. URL Crawler → discovers URLs from base site
2. Content Extractor → processes each URL to extract clean text
3. Text Chunker → splits content into manageable chunks
4. Embedding Generator → creates vector embeddings from text chunks
5. Vector Storage → stores embeddings with metadata in Qdrant
6. Pipeline Orchestrator → manages the entire workflow

### External Dependencies
- **Cohere API**: For embedding generation
- **Qdrant Vector Database**: For vector storage and retrieval
- **Target Docusaurus Site**: https://hackathone-late-1.vercel.app/ (or configurable URL)
- **Sitemap URL**: https://hackathone-late-1.vercel.app/sitemap.xml

## Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Docusaurus    │───▶│  Embedding      │───▶│   Qdrant       │
│   Documentation │    │  Pipeline       │    │   Vector DB    │
│   Site          │    │  (main.py)      │    │                │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │    Cohere        │
                       │    API           │
                       └──────────────────┘
```

### Component Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    main.py (Single File)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   URL Crawler   │  │ Content Extract │  │ Text Chunker    │  │
│  │ get_all_urls()  │  │extract_text_from│  │  chunk_text()   │  │
│  └─────────────────┘  │   _url()        │  └─────────────────┘  │
│                       └─────────────────┘                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │Embedding Gen.   │  │Vector Storage   │  │Pipeline Orchest.│  │
│  │   embed()       │  │save_chunk_to_   │  │   main()        │  │
│  └─────────────────┘  │   qdrant()      │  └─────────────────┘  │
│                       └─────────────────┘                       │
│  ┌─────────────────┐  ┌─────────────────┐                       │
│  │ Collection      │  │ Configuration   │                       │
│  │create_collection│  │  (env vars,     │                       │
│  │    ()           │  │   logging)      │                       │
│  └─────────────────┘  └─────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack
- **Language**: Python 3.11
- **Web Scraping**: requests + BeautifulSoup4
- **Embeddings**: Cohere API
- **Vector Database**: Qdrant Client
- **Environment Management**: python-dotenv
- **Package Management**: UV

### API Integration Points
- **Cohere API**: Used for generating text embeddings via REST endpoints
- **Qdrant API**: Used for vector storage and retrieval via gRPC/HTTP
- **HTTP Client**: Used for crawling and extracting content from web pages

### Performance Considerations
- Rate limiting for API calls to prevent throttling
- Chunked processing to handle large documents efficiently
- Batch operations where possible for better throughput
- Memory management to handle up to 1000 pages

## Project Structure

### Documentation (this feature)

```text
specs/001-embedding-pipeline/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # Single file implementation with all required functions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .env.example         # Example environment variables
└── pyproject.toml       # Project configuration with uv
```

**Structure Decision**: Single-file implementation in main.py as requested by user, with backend folder structure to contain the embedding pipeline service. This follows the user's specific requirement for a single file containing all functions: get_all_urls, extract_text_from_url, chunk_text, embed, create_collection named rag_embedding, save_chunk_to_qdrant and execute in main function.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Single file architecture | User requirement for single main.py | Multiple files would add complexity without benefit for this focused task |
