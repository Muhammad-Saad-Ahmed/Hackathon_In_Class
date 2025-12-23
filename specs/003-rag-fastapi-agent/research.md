# Research: RAG Agent Implementation

**Date**: 2025-12-24

This document outlines the research and decisions made for the implementation of the RAG agent, based on the user's latest instructions which deviate from the original `spec.md`.

## Decision: Agent Implementation without FastAPI

- **Decision**: The agent will be implemented as a Python script (`agent.py`) using the OpenAI Agents SDK, without a FastAPI web server.
- **Rationale**: The user requested a direct implementation of the agent's core logic first, deferring the web interface. This simplifies the initial development and allows for quicker iteration on the agent's functionality.
- **Alternatives considered**: Sticking to the original spec of building a FastAPI service. This was rejected because it was not the user's current priority.

## Decision: Data Retrieval from `retrieving.py`

- **Decision**: The core logic of the `retrieve` function from `retrieving.py` will be integrated into `agent.py`. This includes embedding the query and searching Qdrant.
- **Rationale**: The `retrieve` function in `retrieving.py` is implemented as a Typer command-line application. While it could be called as a subprocess, it's cleaner and more efficient to integrate the retrieval logic directly into the agent's Python code. This avoids the overhead of subprocess calls and allows for better error handling and data flow.
- **Alternatives considered**: Calling the `retrieve` command as a subprocess. This was rejected due to the added complexity and potential for errors.

## Decision: Use of OpenAI Agents SDK

- **Decision**: The agent will be built using the `openai` library, as requested by the user and specified in the project's constitution.
- **Rationale**: The OpenAI Agents SDK provides the necessary tools to build and run agents that can interact with tools, which in this case will be the data retrieval function.
- **Alternatives considered**: None, as this was a direct requirement from the user and the constitution.
