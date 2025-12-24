# Data Model: RAG UI Integration

**Date**: 2025-12-24

This document describes the data models for the API endpoint that connects the frontend and the backend.

## API Data Structures

### Request Body (`/ask`)

- **Description**: The JSON payload sent from the frontend to the backend.
- **Fields**:
    - `query` (string, required): The user's question.

### Response Body (`/ask`)

- **Description**: The JSON payload returned from the backend to the frontend.
- **Fields**:
    - `answer` (string): The generated answer to the user's query.
    - `sources` (list of Source objects): A list of the document sources used to generate the answer.
    - `matched_chunks` (list of strings): The raw text chunks that were matched from the sources.

### Source Object

- **Description**: Represents a source document.
- **Fields**:
    - `url` (string): The URL of the source document.
    - `score` (float): The relevance score of the document.
