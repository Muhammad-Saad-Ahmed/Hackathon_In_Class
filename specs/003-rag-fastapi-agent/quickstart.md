# Quickstart: RAG Agent

**Date**: 2025-12-24

This guide explains how to run the RAG agent.

## Prerequisites

- Python 3.11
- An OpenAI API key set in a `.env` file in the `backend` directory, like this:
  ```
  OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- A running Qdrant instance.

## Installation

1.  Install the required Python packages:
    ```bash
    pip install -r backend/requirements.txt
    ```

## Running the Agent

The agent is implemented in `backend/agent.py`. You can run it from the command line with a query:

```bash
python backend/agent.py --query "Your question here"
```

The agent will then print the generated answer and the sources it used.
