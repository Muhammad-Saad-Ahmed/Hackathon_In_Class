# Quickstart: Embedding Pipeline

## Setup

1. **Initialize the project with UV**:
   ```bash
   # Create backend directory
   mkdir backend && cd backend

   # Initialize with UV (if not already done)
   uv init
   ```

2. **Install dependencies**:
   ```bash
   uv pip install cohere qdrant-client requests beautifulsoup4 python-dotenv
   ```

3. **Set up environment variables**:
   Create a `.env` file with:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Configuration

The main.py file contains all necessary functions for the embedding pipeline:

- `get_all_urls(base_url)`: Crawls and extracts all valid URLs from a base URL
- `extract_text_from_url(url)`: Extracts clean text content from a given URL
- `chunk_text(text, chunk_size=1000, overlap=100)`: Splits text into manageable chunks
- `embed(texts)`: Generates embeddings using Cohere API
- `create_collection()`: Creates the "New_Embed" collection in Qdrant
- `save_chunk_to_qdrant(chunk, url, title, vector)`: Stores embeddings in Qdrant with metadata

## Usage

1. **Run the pipeline**:
   ```bash
   cd backend
   python main.py
   ```

2. **The main function will execute the complete pipeline**:
   - Fetch all URLs from the specified site (https://hackathon-in-classnew.vercel.app/)
   - Extract text content from each URL
   - Chunk the content appropriately
   - Generate embeddings using Cohere
   - Create the Qdrant collection if it doesn't exist
   - Store all embeddings with metadata in Qdrant

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant access (if required)
- `TARGET_URL`: The base URL to crawl (defaults to https://hackathon-in-classnew.vercel.app/)

## Troubleshooting

- Ensure all environment variables are properly set
- Check that your Cohere and Qdrant APIs are accessible
- Verify that the target website allows crawling (check robots.txt)
- Monitor API rate limits to avoid being throttled