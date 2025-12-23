# Data Model: RAG Agent

**Date**: 2025-12-24

This document describes the data models used in the RAG agent.

## Core Entities

### Query
- **Description**: Represents the user's input question.
- **Fields**:
    - `query_text` (string): The text of the user's query.

### DocumentChunk
- **Description**: Represents a chunk of text retrieved from the vector database.
- **Fields**:
    - `text` (string): The content of the document chunk.
    - `url` (string): The source URL of the document.
    - `chunk_id` (string or int): The unique identifier for the chunk.
    - `score` (float): The relevance score of the chunk to the query.

### AgentResponse
- **Description**: Represents the final output from the agent.
- **Fields**:
    - `answer` (string): The generated answer to the user's query.
    - `sources` (list of DocumentChunk): A list of the document chunks used to generate the answer.
