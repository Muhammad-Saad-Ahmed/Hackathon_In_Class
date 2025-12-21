"""
Embedding Pipeline - Main Implementation

This module implements the complete pipeline for:
1. Extracting text from Docusaurus URLs using sitemap.xml
2. Generating embeddings using Cohere
3. Storing embeddings in Qdrant vector database
"""
import os
import logging
from typing import List, Dict, Tuple, Optional
import time
import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import uuid
import argparse


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Config:
    """Configuration class to load and validate environment variables"""

    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    # Validate required environment variables
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable is required")
    if not QDRANT_URL:
        raise ValueError("QDRANT_URL environment variable is required")

    # Optional environment variables with defaults
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    RATE_LIMIT = float(os.getenv("RATE_LIMIT", "1.0"))  # requests per second
    SITEMAP_URL = os.getenv("SITEMAP_URL", "https://hackathon-in-classnew.vercel.app/sitemap.xml")


# Initialize Cohere client
co = cohere.Client(Config.COHERE_API_KEY)

# Initialize Qdrant client
if Config.QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        url=Config.QDRANT_URL,
        api_key=Config.QDRANT_API_KEY,
        timeout=60  # 60 second timeout for all operations
    )
else:
    # For local instances without authentication
    qdrant_client = QdrantClient(
        url=Config.QDRANT_URL,
        timeout=60  # 60 second timeout for all operations
    )


def validate_and_sanitize_url(url: str) -> Optional[str]:
    """
    Validate and sanitize URL to prevent security issues per FR-010

    Args:
        url: The URL to validate and sanitize

    Returns:
        Sanitized URL if valid, None if invalid
    """
    try:
        # Basic URL format validation
        if not url or not isinstance(url, str):
            return None

        # Strip whitespace
        url = url.strip()

        # Check if it starts with http:// or https://
        if not url.startswith(('http://', 'https://')):
            return None

        # Basic sanitization - remove potential malicious patterns
        # This is a basic implementation - in production, use a more robust library
        if any(pattern in url.lower() for pattern in ['javascript:', 'vbscript:', 'data:', 'file:']):
            return None

        # Basic length check to prevent extremely long URLs
        if len(url) > 2048:
            return None

        return url
    except Exception:
        logger.error(f"Error validating URL: {url}")
        return None


def retry_api_call(func=None, *, max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry API calls with exponential backoff

    Args:
        func: The function to wrap (when used as @retry_api_call)
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds

    Returns:
        Wrapped function with retry logic
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        # Exponential backoff: wait longer after each attempt
                        wait_time = delay * (2 ** attempt)
                        logger.warning(f"API call failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"API call failed after {max_retries + 1} attempts: {str(e)}")

            # If all retries failed, raise the last exception
            raise last_exception

        return wrapper

    if func is None:
        # Called with parameters: @retry_api_call(max_retries=3, delay=1.0)
        return decorator
    else:
        # Called without parameters: @retry_api_call
        return decorator(func)


# Example of how to use the retry decorator with API calls
# @retry_api_call(max_retries=3, delay=1.0)
# def example_api_call():
#     # Your API call here
#     pass


@retry_api_call(max_retries=3, delay=1.0)
def get_all_urls(sitemap_url: str = Config.SITEMAP_URL) -> List[str]:
    """
    Fetch all URLs from the target Docusaurus site using sitemap.xml

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of URLs extracted from the sitemap

    Raises:
        requests.RequestException: If there's an error fetching the sitemap
        ValueError: If the sitemap format is invalid
    """
    try:
        logger.info(f"Fetching sitemap from: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()

        # Parse the sitemap XML - try different parsers
        try:
            soup = BeautifulSoup(response.content, 'xml')
        except Exception:
            # If xml parser is not available, try html parser which can handle XML
            soup = BeautifulSoup(response.content, 'html.parser')

        # Find all URL elements in the sitemap
        url_elements = soup.find_all('url')
        urls = []

        for url_elem in url_elements:
            loc_elem = url_elem.find('loc')
            if loc_elem:
                url = loc_elem.text.strip()
                url = url.replace("https://muhammad-saad-ahmed.github.io/", "https://hackathon-in-classnew.vercel.app/")
                sanitized_url = validate_and_sanitize_url(url)
                if sanitized_url:
                    urls.append(sanitized_url)

        logger.info(f"Successfully extracted {len(urls)} URLs from sitemap")
        return urls

    except requests.RequestException as e:
        logger.error(f"Error fetching sitemap from {sitemap_url}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error parsing sitemap from {sitemap_url}: {str(e)}")
        raise ValueError(f"Invalid sitemap format: {str(e)}")


@retry_api_call(max_retries=3, delay=1.0)
def extract_text_from_url(url: str) -> Dict[str, any]:
    """
    Extract clean text content from a given URL using BeautifulSoup

    Args:
        url: The URL to extract text from

    Returns:
        Dictionary with 'title', 'content', 'url', and 'metadata' keys

    Raises:
        requests.RequestException: If there's an error fetching the URL
        ValueError: If the content cannot be extracted
    """
    try:
        # Validate and sanitize the URL
        sanitized_url = validate_and_sanitize_url(url)
        if not sanitized_url:
            raise ValueError(f"Invalid URL: {url}")

        logger.info(f"Extracting text from: {sanitized_url}")
        response = requests.get(sanitized_url, timeout=30)
        response.raise_for_status()

        # Parse the HTML content - BeautifulSoup handles malformed HTML gracefully
        # Use 'html.parser' which is more lenient than 'xml.parser' for malformed HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "No Title"

        # Remove navigation, headers, footers, and sidebar elements that are common in Docusaurus sites
        # These are often found with specific CSS classes in Docusaurus
        selectors_to_remove = [
            'nav', 'header', 'footer', 'aside',  # Standard HTML elements
            '.nav', '.navbar', '.navigation',  # Navigation elements
            '.header', '.topbar', '.header-wrapper',  # Header elements
            '.footer', '.bottom', '.footer-wrapper',  # Footer elements
            '.sidebar', '.sidenav', '.side-nav',  # Sidebar elements
            '.toc', '.table-of-contents',  # Table of contents
            '.theme-edit-this-page',  # Edit link
            '.pagination', '.pager',  # Pagination elements
            '.social', '.share',  # Social sharing elements
            '.comments', '.disqus',  # Comments sections
            '.ads', '.advertisement',  # Ad elements
        ]

        for selector in selectors_to_remove:
            for element in soup.select(selector):
                element.decompose()

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Look for main content containers that are common in Docusaurus
        content_selectors = [
            'main',  # Main content area
            '.main-wrapper',  # Docusaurus main wrapper
            '.container',  # Container elements
            '.theme-doc-markdown',  # Docusaurus markdown content
            '.markdown',  # Markdown content
            '.doc-content',  # Documentation content
            '.content',  # General content area
            'article',  # Article elements
        ]

        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Get text from the first matching element
                content = elements[0].get_text(separator=' ', strip=True)
                break

        # If no specific content container found, get all text from body
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text(separator=' ', strip=True)

        # Clean up the content - remove extra whitespace
        import re
        content = re.sub(r'\s+', ' ', content).strip()

        # Preserve source URL and document structure information in metadata per FR-008
        result = {
            'title': title,
            'content': content,
            'url': sanitized_url,
            'metadata': {
                'source_url': sanitized_url,
                'title': title,
                'content_length': len(content),
                'extraction_timestamp': time.time(),
                'content_type': 'docusaurus_page'
            }
        }

        logger.info(f"Successfully extracted text from {sanitized_url} - Title: {title[:50]}...")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {str(e)}")
        raise ValueError(f"Could not extract content from URL: {str(e)}")


def chunk_text(text: str, chunk_size: int = Config.CHUNK_SIZE, overlap: int = Config.CHUNK_OVERLAP) -> List[str]:
    """
    Split text into manageable chunks with overlap to maintain context.

    Args:
        text: The text to chunk.
        chunk_size: Maximum size of each chunk.
        overlap: Number of characters to overlap between chunks.

    Returns:
        List of text chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Advance start position, ensuring it moves forward
        next_start = start + chunk_size - overlap
        
        # If next_start is not advancing, force it to advance to prevent infinite loops
        if next_start <= start:
            next_start = start + 1 
            
        start = next_start

    return chunks


@retry_api_call(max_retries=3, delay=1.0)
def embed(text: str) -> List[float]:
    """
    Generate embeddings for text using Cohere API

    Args:
        text: The text to embed

    Returns:
        Embedding vector as a list of floats

    Raises:
        Exception: If embedding generation fails
    """
    try:
        logger.info(f"Generating embedding for text of length {len(text)}")

        # Use Cohere's embed API to generate embeddings
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",  # Using model that supports 1024 dimensions as per data-model.md
            input_type="search_document"  # Specify this is for document search
        )

        # Extract the embedding from the response
        embedding = response.embeddings[0] if response.embeddings else None

        if embedding is None:
            raise Exception("No embedding returned from Cohere API")

        logger.info(f"Successfully generated embedding with {len(embedding)} dimensions")
        return embedding

    except Exception as e:
        logger.error(f"Error generating embedding for text: {str(e)}")
        raise


@retry_api_call(max_retries=3, delay=1.0)
def create_collection(collection_name: str = "New_Rag_Data"):
    """
    Create a Qdrant collection named "New_Rag_Data" with appropriate schema

    Args:
        collection_name: Name of the collection to create

    Raises:
        Exception: If collection creation fails
    """
    try:
        logger.info(f"Creating Qdrant collection: {collection_name}")

        # Define the collection schema per data-model.md (vector size 1024, cosine similarity)
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),  # Cohere's multilingual model dimension per spec
        )

        logger.info(f"Successfully created Qdrant collection: {collection_name}")

    except Exception as e:
        logger.error(f"Error creating Qdrant collection {collection_name}: {str(e)}")
        raise


def save_chunks_batch_to_qdrant(chunks_data: List[Dict], collection_name: str = "New_Rag_Data", batch_size: int = 10):
    """
    Store multiple text chunks with their embeddings in Qdrant using batch operations

    Args:
        chunks_data: List of dictionaries containing 'chunk', 'embedding', and 'metadata'
        collection_name: Name of the collection to store in
        batch_size: Number of chunks to process in each batch

    Raises:
        Exception: If batch storage fails
    """
    if not chunks_data:
        logger.info("No chunks to save to Qdrant")
        return

    logger.info(f"Saving {len(chunks_data)} chunks to Qdrant in batches of {batch_size}")

    # Process in batches to ensure complete saving
    for i in range(0, len(chunks_data), batch_size):
        batch = chunks_data[i:i + batch_size]
        batch_points = []

        for chunk_data in batch:
            chunk = chunk_data['chunk']
            embedding = chunk_data['embedding']
            metadata = chunk_data['metadata']

            # Generate a unique ID for this point
            point_id = str(uuid.uuid4())

            # Prepare the point to insert
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document_id": metadata.get('source_url', ''),
                    "chunk_id": point_id,
                    "url": metadata.get('source_url', ''),
                    "title": metadata.get('title', ''),
                    "chunk_index": metadata.get('chunk_index', 0),
                    "content": chunk,
                    "created_at": metadata.get('extraction_timestamp', time.time()),
                    **metadata  # Include any additional metadata
                }
            )
            batch_points.append(point)

        try:
            # Insert the batch of points into the collection - timeout is handled at client level
            result = qdrant_client.upsert(
                collection_name=collection_name,
                points=batch_points
            )

            logger.info(f"Successfully saved batch of {len(batch_points)} chunks to Qdrant")

            # Verify the batch was saved by checking the result
            if hasattr(result, 'status') and result.status:
                logger.debug(f"Batch operation completed successfully")
            else:
                logger.warning(f"Batch operation completed but status unclear")

        except Exception as e:
            logger.error(f"Error saving batch of chunks to Qdrant: {str(e)}")
            # Retry saving individual points if batch fails
            for point in batch_points:
                try:
                    qdrant_client.upsert(
                        collection_name=collection_name,
                        points=[point]
                    )
                    logger.info(f"Saved individual chunk after batch failure: {point.id}")
                except Exception as individual_error:
                    logger.error(f"Failed to save individual chunk after batch failure: {str(individual_error)}")
                    raise
            continue  # Continue with next batch after handling the error

    logger.info(f"Successfully saved all {len(chunks_data)} chunks to Qdrant in batches")


@retry_api_call(max_retries=3, delay=1.0)
def save_chunk_to_qdrant(chunk: str, embedding: List[float], metadata: Dict, collection_name: str = "New_Rag_Data"):
    """
    Store a text chunk with its embedding in Qdrant

    Args:
        chunk: The text chunk to store
        embedding: The embedding vector
        metadata: Additional metadata to store with the chunk
        collection_name: Name of the collection to store in

    Raises:
        Exception: If storage fails
    """
    try:
        # Generate a unique ID for this point
        point_id = str(uuid.uuid4())

        logger.info(f"Saving chunk to Qdrant collection {collection_name}, chunk length: {len(chunk)}")

        # Prepare the point to insert
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "document_id": metadata.get('source_url', ''),
                "chunk_id": point_id,
                "url": metadata.get('source_url', ''),
                "title": metadata.get('title', ''),
                "chunk_index": metadata.get('chunk_index', 0),
                "content": chunk,
                "created_at": metadata.get('extraction_timestamp', time.time()),
                **metadata  # Include any additional metadata
            }
        )

        # Insert the point into the collection - timeout is handled at client level
        result = qdrant_client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        # Verify that the point was actually saved by checking the operation info
        if hasattr(result, 'status') and result.status:
            logger.info(f"Successfully saved chunk to Qdrant with ID: {point_id}")
        else:
            logger.warning(f"Chunk save operation completed but status unclear for ID: {point_id}")

        # Optional: Verify the point was actually stored by retrieving it
        try:
            retrieved_points = qdrant_client.retrieve(
                collection_name=collection_name,
                ids=[point_id],
                timeout=30
            )
            if retrieved_points:
                logger.debug(f"Verified chunk saved successfully with ID: {point_id}")
            else:
                logger.warning(f"Could not verify chunk with ID: {point_id} after save")
        except Exception as verify_error:
            logger.warning(f"Could not verify chunk save for ID {point_id}: {str(verify_error)}")

    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {str(e)}")
        raise


class CrawlConfig:
    """
    Configuration class for URL crawling parameters per data-model.md
    """
    def __init__(self, urls: List[str] = None, sitemap_url: str = Config.SITEMAP_URL,
                 max_depth: int = 1, rate_limit: float = Config.RATE_LIMIT,
                 allowed_domains: List[str] = None, content_filters: Dict = None):
        self.urls = urls or []
        self.sitemap_url = sitemap_url
        self.max_depth = max_depth
        self.rate_limit = rate_limit  # requests per second
        self.allowed_domains = allowed_domains or []
        self.content_filters = content_filters or {}


def main():
    """
    Main function that orchestrates the complete pipeline:
    get_all_urls → extract_text_from_url → chunk_text → embed → create_collection → save_chunk_to_qdrant
    """
    parser = argparse.ArgumentParser(description="Embedding Pipeline for Docusaurus sites.")
    parser.add_argument("--start-index", type=int, default=None, help="The starting index of the URL list to process.")
    parser.add_argument("--end-index", type=int, default=None, help="The ending index of the URL list to process.")
    parser.add_argument("--get-total-urls", action="store_true", help="Print the total number of URLs and exit.")
    parser.add_argument("--url-index", type=int, default=None, help="The index of the URL to process from the sitemap.")
    parser.add_argument("--chunk-start-index", type=int, default=None, help="The starting index of the chunk list to process.")
    parser.add_argument("--chunk-end-index", type=int, default=None, help="The ending index of the chunk list to process.")
    parser.add_argument("--get-total-chunks-for-url", type=int, default=None, help="Print the total number of chunks for a given URL index and exit.")
    args = parser.parse_args()

    logger.info("Starting embedding pipeline...")

    try:
        # Step 1: Get all URLs from sitemap
        logger.info("Getting all URLs from sitemap...")
        urls = get_all_urls()
        logger.info(f"Retrieved {len(urls)} URLs from sitemap")

        if args.get_total_urls:
            print(f"Total URLs: {len(urls)}")
            return

        if args.get_total_chunks_for_url is not None:
            url_index = args.get_total_chunks_for_url
            if 0 <= url_index < len(urls):
                url = urls[url_index]
                extracted_data = extract_text_from_url(url)
                content = extracted_data['content']
                chunks = chunk_text(content)
                print(f"Total chunks for URL {url_index} ({url}): {len(chunks)}")
            else:
                print(f"Invalid URL index: {url_index}. Must be between 0 and {len(urls) - 1}.")
            return

        # Determine the slice of URLs to process
        if args.url_index is not None:
            urls_to_process = [urls[args.url_index]]
            logger.info(f"Processing single URL at index {args.url_index}: {urls_to_process[0]}")
        elif args.start_index is not None and args.end_index is not None:
            urls_to_process = urls[args.start_index:args.end_index]
            logger.info(f"Processing URLs from index {args.start_index} to {args.end_index}")
        else:
            urls_to_process = urls
            logger.info("Processing all URLs")

        # Step 2: Create the Qdrant collection (only if it doesn't exist)
        try:
            collection_info = qdrant_client.get_collection("New_Rag_Data")
            logger.info(f"Collection 'New_Rag_Data' already exists with {collection_info.points_count} points")
        except:
            logger.info("Creating Qdrant collection...")
            create_collection("New_Rag_Data")

        # Step 3: Process each URL
        all_chunks_data = []  # Collect all chunks for batch processing

        for idx, url in enumerate(urls_to_process):
            logger.info(f"Processing URL {idx+1}/{len(urls_to_process)}: {url}")

            try:
                # Extract text from the URL
                extracted_data = extract_text_from_url(url)
                content = extracted_data['content']
                metadata = extracted_data['metadata']

                # Chunk the content
                chunks = chunk_text(content)
                logger.info(f"Content chunked into {len(chunks)} pieces")

                # Determine the slice of chunks to process
                if args.chunk_start_index is not None and args.chunk_end_index is not None:
                    chunks_to_process = chunks[args.chunk_start_index:args.chunk_end_index]
                    logger.info(f"Processing chunks from index {args.chunk_start_index} to {args.chunk_end_index}")
                else:
                    chunks_to_process = chunks
                    logger.info("Processing all chunks for this URL")

                # Process each chunk and collect for batch processing
                for chunk_idx, chunk in enumerate(chunks_to_process):
                    if chunk.strip():  # Only process non-empty chunks
                        # Update metadata with chunk-specific info
                        chunk_metadata = metadata.copy()
                        chunk_metadata['chunk_index'] = chunk_idx + (args.chunk_start_index or 0)

                        # Generate embedding for the chunk
                        embedding = embed(chunk)

                        # Collect chunk data for batch processing
                        chunk_data = {
                            'chunk': chunk,
                            'embedding': embedding,
                            'metadata': chunk_metadata
                        }
                        all_chunks_data.append(chunk_data)

                        # Rate limiting to be respectful to APIs
                        time.sleep(1.0 / Config.RATE_LIMIT)

            except Exception as e:
                logger.error(f"Error processing URL {url}: {str(e)}")
                continue  # Continue with the next URL

        # Process all chunks in batches for efficient and complete saving to Qdrant
        if all_chunks_data:
            logger.info(f"Saving {len(all_chunks_data)} total chunks to Qdrant using batch processing")
            save_chunks_batch_to_qdrant(all_chunks_data)

        logger.info("Pipeline completed successfully!")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise


# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()