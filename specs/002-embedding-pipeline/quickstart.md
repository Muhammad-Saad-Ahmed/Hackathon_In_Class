# Quickstart: Embedding Pipeline

## Prerequisites
- Python 3.11+
- UV package manager
- Cohere API key
- Qdrant API key and endpoint

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install UV package manager** (if not already installed)
   ```bash
   pip install uv
   ```

3. **Create and navigate to backend directory**
   ```bash
   mkdir backend
   cd backend
   ```

4. **Create virtual environment and install dependencies**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install cohere qdrant-client beautifulsoup4 requests python-dotenv
   ```

5. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Usage

1. **Run the embedding pipeline**
   ```bash
   cd backend
   python main.py
   ```

## Configuration

The pipeline will:
1. Fetch all URLs from the target Docusaurus site using the sitemap.xml file
2. Extract clean text content from each URL
3. Chunk the text into manageable pieces
4. Generate embeddings using Cohere
5. Create a Qdrant collection named "New_Rag_Data"
6. Store all embeddings with metadata in Qdrant

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL to your Qdrant instance
- `QDRANT_API_KEY`: Your Qdrant API key (if using cloud service)

## Expected Output

The pipeline will create a Qdrant collection named "New_Rag_Data" containing vector embeddings of your Docusaurus content, ready for RAG-based retrieval.