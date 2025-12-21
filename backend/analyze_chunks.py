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

def get_all_urls(sitemap_url: str = Config.SITEMAP_URL) -> List[str]:
    """
    Fetch all URLs from the target Docusaurus site using sitemap.xml

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of URLs extracted from the sitemap
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

def extract_text_from_url(url: str) -> Dict[str, any]:
    """
    Extract clean text content from a given URL using BeautifulSoup
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
    Split text into manageable chunks with overlap to maintain context

    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        # If this is the last chunk, include all remaining text
        if end >= text_length:
            chunk = text[start:]
        else:
            # Try to break at sentence boundary if possible
            chunk = text[start:end]

            # Find the last sentence ending in the chunk
            last_sentence_end = max(
                chunk.rfind('. '),
                chunk.rfind('? '),
                chunk.rfind('! '),
                chunk.rfind('\n')
            )

            # If we found a sentence boundary and it's not at the end, adjust the chunk
            if last_sentence_end > 0 and last_sentence_end < len(chunk) - overlap:
                actual_end = start + last_sentence_end + 1
                chunk = text[start:actual_end]
                end = actual_end

        chunks.append(chunk)
        start = end - overlap if end < text_length else text_length

    return chunks

def main_analysis():
    """
    Analyze the URLs and chunks without processing them completely
    """
    logger.info("Starting URL and chunk analysis...")

    # Get all URLs from sitemap
    logger.info("Getting all URLs from sitemap...")
    urls = get_all_urls()
    logger.info(f"Retrieved {len(urls)} URLs from sitemap")

    total_chunks = 0

    # Process each URL to count chunks
    for idx, url in enumerate(urls):
        logger.info(f"Analyzing URL {idx+1}/{len(urls)}: {url}")

        try:
            # Extract text from the URL
            extracted_data = extract_text_from_url(url)
            content = extracted_data['content']
            title = extracted_data['title']
            metadata = extracted_data['metadata']

            # Chunk the content
            chunks = chunk_text(content)
            logger.info(f"Content from '{title[:50]}...' chunked into {len(chunks)} pieces")

            total_chunks += len(chunks)

        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            continue  # Continue with the next URL

    logger.info(f"Total chunks across all URLs: {total_chunks}")
    return total_chunks

if __name__ == "__main__":
    main_analysis()