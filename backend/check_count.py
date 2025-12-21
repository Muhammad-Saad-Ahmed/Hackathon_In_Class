import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if qdrant_api_key:
    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )
else:
    qdrant_client = QdrantClient(url=qdrant_url)

# Get collection info
collection_name = "New_Rag_Data"
try:
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"Collection '{collection_name}' has {collection_info.points_count} points")
except Exception as e:
    print(f"Error getting collection info: {e}")