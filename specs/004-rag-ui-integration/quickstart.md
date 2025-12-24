# Quickstart: RAG UI Integration

**Date**: 2025-12-24

This guide explains how to run the RAG agent with its frontend UI for local development.

## Prerequisites

- Python 3.11
- Node.js and npm
- An OpenAI API key set in a `.env` file in the `backend` directory.
- A running Qdrant instance.

## Backend Setup

1.  Install the required Python packages:
    ```bash
    pip install -r backend/requirements.txt
    ```

2.  Run the FastAPI server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will be available at `http://127.0.0.1:8000`.

## Frontend Setup

1.  Install the required npm packages:
    ```bash
    npm install
    ```

2.  Run the Docusaurus development server:
    ```bash
    npm start
    ```
    The frontend will be available at `http://localhost:3000`.

## Usage

1.  Open your browser and navigate to `http://localhost:3000`.
2.  You should see the chat widget in the bottom-right corner of the screen.
3.  Type a question and press Enter to get an answer from the RAG agent.
