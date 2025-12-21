# API Contracts: Embedding Pipeline

## Overview
This document outlines the API contracts for the embedding pipeline functions that will be implemented in main.py.

## Function Contracts

### get_all_urls()
- **Purpose**: Fetch all URLs from the target Docusaurus site using sitemap.xml
- **Input**: sitemap_url (string)
- **Output**: List of URLs (array of strings)
- **Error cases**: Network errors, invalid sitemap URL, sitemap parsing errors

### extract_text_from_url()
- **Purpose**: Extract clean text content from a given URL
- **Input**: url (string)
- **Output**: Dictionary with {title: string, content: string}
- **Error cases**: URL not accessible, content extraction fails

### chunk_text()
- **Purpose**: Split text content into manageable chunks
- **Input**: text (string), chunk_size (integer), overlap (integer)
- **Output**: Array of text chunks (array of strings)
- **Error cases**: Invalid input parameters

### embed()
- **Purpose**: Generate embeddings for text chunks using Cohere
- **Input**: text (string)
- **Output**: embedding vector (array of floats)
- **Error cases**: Cohere API errors, rate limits, invalid text

### create_collection()
- **Purpose**: Create a Qdrant collection named "New_Rag_Data"
- **Input**: collection_name (string)
- **Output**: Success status (boolean)
- **Error cases**: Qdrant connection errors, collection creation failure

### save_chunk_to_qdrant()
- **Purpose**: Store a text chunk with its embedding in Qdrant
- **Input**: chunk (string), embedding (array of floats), metadata (dict)
- **Output**: Success status (boolean)
- **Error cases**: Qdrant storage errors, invalid data format