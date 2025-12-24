
import os
import cohere
import qdrant_client
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import uuid

# Load environment variables from .env file
load_dotenv()

# Get API keys and URLs from environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
TARGET_URL = os.getenv("TARGET_URL", "https://hackathon-in-classnew.vercel.app/")
COLLECTION_NAME = "rag_embedding"

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Initialize Qdrant client
qdrant_client = qdrant_client.QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY,
)

def get_all_urls(base_url):
    """
    Crawls a sitemap to get all the URLs.
    """
    sitemap_url = f"{base_url.rstrip('/')}/sitemap.xml"
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    return urls

def extract_text_from_url(url):
    """
    Extracts the main text content from a URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the main content of the page (this might need to be adjusted based on the site's structure)
        # For Docusaurus, the main content is often in an article tag or a div with a specific class.
        # We will try to find a few common patterns.
        main_content = soup.find("article") or soup.find("main")

        if main_content:
            # Remove nav, header, footer, and script/style tags
            for element in main_content.find_all(["nav", "header", "footer", "script", "style"]):
                element.decompose()

            text = main_content.get_text(separator=' ', strip=True)
            title = soup.title.string if soup.title else "No Title"
            return text, title
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None


def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Splits text into overlapping chunks.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def embed(texts):
    """
    Generates embeddings using the Cohere API.
    """
    if not texts:
        return []
    response = co.embed(texts=texts, model="embed-english-light-v2.0")
    return response.embeddings

def create_collection():
    """
    Creates the Qdrant collection if it doesn't exist.
    """
    try:
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception as e:
        print(f"Collection '{COLLECTION_NAME}' does not exist. Creating it now.")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created.")


def save_chunk_to_qdrant(chunk, url, title, vector):
    """
    Saves a single chunk and its vector to Qdrant.
    """
    if vector:
        point_id = str(uuid.uuid4())
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"text": chunk, "url": url, "title": title},
                )
            ],
            wait=True,
        )


def main():
    """
    Main function to run the embedding pipeline.
    """
    print("Starting the embedding pipeline...")

    # Create the collection if it doesn't exist
    create_collection()

    # Get all URLs from the sitemap
    urls = get_all_urls(TARGET_URL)
    print(f"Found {len(urls)} URLs to process.")

    for url in urls:
        print(f"Processing {url}...")
        text, title = extract_text_from_url(url)

        if text:
            chunks = chunk_text(text)
            print(f"  -  Split into {len(chunks)} chunks.")
            
            vectors = embed(chunks)
            print(f"  -  Generated {len(vectors)} embeddings.")

            for i, chunk in enumerate(chunks):
                if i < len(vectors):
                    save_chunk_to_qdrant(chunk, url, title, vectors[i])
            print(f"  -  Saved {len(chunks)} chunks to Qdrant.")

    print("Embedding pipeline finished.")

if __name__ == "__main__":
    main()
