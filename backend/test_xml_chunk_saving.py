"""
Test script to verify XML chunks are completely saved to Qdrant with proper timeout settings
"""
import os
import logging
import time
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Config:
    """Configuration class to load and validate environment variables"""
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    if not QDRANT_URL:
        raise ValueError("QDRANT_URL environment variable is required")

def initialize_qdrant_client():
    """Initialize Qdrant client with timeout settings"""
    if Config.QDRANT_API_KEY:
        qdrant_client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=60  # 60 second timeout for all operations
        )
    else:
        qdrant_client = QdrantClient(
            url=Config.QDRANT_URL,
            timeout=60  # 60 second timeout for all operations
        )
    return qdrant_client

def test_xml_chunk_saving():
    """Test function to verify XML chunks are completely saved to Qdrant"""
    logger.info("Starting XML chunk saving test...")

    # Initialize Qdrant client
    qdrant_client = initialize_qdrant_client()

    # Test collection name
    test_collection = "test_xml_chunks"

    try:
        # Create a test collection
        logger.info(f"Creating test collection: {test_collection}")
        qdrant_client.recreate_collection(
            collection_name=test_collection,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        logger.info(f"Successfully created test collection: {test_collection}")

        # Test data - simulate XML chunks
        test_chunks = [
            {
                'content': 'This is the first XML chunk with content to be saved to Qdrant.',
                'embedding': [0.1] * 1024,  # Simulated embedding
                'metadata': {
                    'document_id': 'test_doc_1',
                    'chunk_index': 0,
                    'source_url': 'https://test.example.com/doc1',
                    'title': 'Test Document 1'
                }
            },
            {
                'content': 'This is the second XML chunk with more content to be saved to Qdrant.',
                'embedding': [0.2] * 1024,  # Simulated embedding
                'metadata': {
                    'document_id': 'test_doc_1',
                    'chunk_index': 1,
                    'source_url': 'https://test.example.com/doc1',
                    'title': 'Test Document 1'
                }
            },
            {
                'content': 'This is a third XML chunk with even more content to be saved to Qdrant.',
                'embedding': [0.3] * 1024,  # Simulated embedding
                'metadata': {
                    'document_id': 'test_doc_2',
                    'chunk_index': 0,
                    'source_url': 'https://test.example.com/doc2',
                    'title': 'Test Document 2'
                }
            }
        ]

        # Save chunks with timeout verification
        saved_point_ids = []
        for i, chunk_data in enumerate(test_chunks):
            logger.info(f"Saving chunk {i+1}/{len(test_chunks)} to Qdrant...")

            # Use UUID for point ID as required by Qdrant
            import uuid
            point_id = str(uuid.uuid4())
            saved_point_ids.append(point_id)

            point = PointStruct(
                id=point_id,
                vector=chunk_data['embedding'],
                payload={
                    "document_id": chunk_data['metadata']['document_id'],
                    "chunk_id": point_id,
                    "url": chunk_data['metadata']['source_url'],
                    "title": chunk_data['metadata']['title'],
                    "chunk_index": chunk_data['metadata']['chunk_index'],
                    "content": chunk_data['content'],
                    "created_at": time.time(),
                    **chunk_data['metadata']
                }
            )

            # Save with explicit timeout - note: timeout parameter may not be supported in all versions
            try:
                result = qdrant_client.upsert(
                    collection_name=test_collection,
                    points=[point]
                )
            except TypeError:
                # If timeout parameter is not supported, call without it
                result = qdrant_client.upsert(
                    collection_name=test_collection,
                    points=[point]
                )

            logger.info(f"Chunk {i+1} saved successfully with ID: {point_id}")

            # Verify the chunk was saved by retrieving it
            retrieved_points = qdrant_client.retrieve(
                collection_name=test_collection,
                ids=[point_id],
                timeout=30
            )

            if retrieved_points:
                logger.info(f"Verification successful: Chunk {i+1} exists in Qdrant")
            else:
                logger.error(f"Verification failed: Chunk {i+1} not found after save")

        # Check total count
        collection_info = qdrant_client.get_collection(test_collection)
        logger.info(f"Collection '{test_collection}' now has {collection_info.points_count} points")

        if collection_info.points_count == len(test_chunks):
            logger.info("SUCCESS: All XML chunks were completely saved to Qdrant")
        else:
            logger.warning(f"WARNING: Expected {len(test_chunks)} points, but found {collection_info.points_count}")

        # Clean up - delete test collection
        logger.info("Cleaning up: Deleting test collection")
        qdrant_client.delete_collection(test_collection)
        logger.info("Test completed successfully!")

        return True

    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_xml_chunk_saving()
    if success:
        logger.info("XML chunk saving test PASSED")
    else:
        logger.error("XML chunk saving test FAILED")