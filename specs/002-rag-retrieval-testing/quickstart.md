# Quickstart: RAG Retrieval Testing Script

This guide explains how to set up and run the RAG retrieval testing script.

## Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Install dependencies**:
    Make sure you have Python 3.11+ and pip installed. It is recommended to use a virtual environment.
    ```bash
    pip install "typer[all]" qdrant-client sentence-transformers
    ```

## Running the Script

The script is named `retrieving.py` and is located in the `backend` directory. It uses `typer` for command-line arguments.

### Basic Usage

To run a query, use the `--query` option:
```bash
python retrieving.py --query "your query text here"
```

### Example

```bash
python retrieving.py --query "What is Spec-Driven Development?"
```

## Output Format

The script will print a JSON object to standard output containing a list of the retrieved documents.

### Example JSON Output

```json
[
  {
    "text": "Spec-Driven Development is a methodology where a detailed specification is the source of truth for all implementation...",
    "url": "/docs/intro/what-is-sdd",
    "chunk_id": 1,
    "score": 0.98123
  },
  {
    "text": "The core principle of SDD is 'if it is not specified, it must not be implemented'...",
    "url": "/docs/intro/what-is-sdd",
    "chunk_id": 2,
    "score": 0.95432
  }
]
```

## Overriding Defaults

You can override the default Qdrant connection settings using environment variables:

-   `QDRANT_HOST`: The Qdrant server host (default: `localhost`).
-   `QDRANT_PORT`: The Qdrant server port (default: `6333`).
-   `QDRANT_COLLECTION`: The name of the collection to query (default: `test_collection`).

### Example with Environment Variables

**PowerShell:**
```powershell
$env:QDRANT_HOST="192.168.1.100"
$env:QDRANT_COLLECTION="prod_collection"
python retrieving.py --query "What is Spec-Driven Development?"
```

**Bash:**
```bash
export QDRANT_HOST="192.168.1.100"
export QDRANT_COLLECTION="prod_collection"
python retrieving.py --query "What is Spec-Driven Development?"
```
