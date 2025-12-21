"""
Tests for the embedding pipeline functions
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import chunk_text, validate_and_sanitize_url


class TestMainFunctions(unittest.TestCase):

    def test_chunk_text_basic(self):
        """Test basic text chunking functionality"""
        text = "This is a test sentence. " * 50  # Create a longer text
        chunks = chunk_text(text, chunk_size=50, overlap=10)

        # Should have multiple chunks
        self.assertGreater(len(chunks), 1)

        # Each chunk should be approximately the right size
        for i, chunk in enumerate(chunks):
            if i == len(chunks) - 1:  # Last chunk can be shorter
                continue
            # Allow some flexibility due to sentence boundary detection
            self.assertLessEqual(len(chunk), 50)

    def test_chunk_text_empty(self):
        """Test chunking of empty text"""
        chunks = chunk_text("")
        self.assertEqual(chunks, [])

    def test_chunk_text_shorter_than_chunk_size(self):
        """Test chunking of text shorter than chunk size"""
        text = "Short text"
        chunks = chunk_text(text, chunk_size=100, overlap=10)
        self.assertEqual(chunks, ["Short text"])

    def test_validate_and_sanitize_url_valid(self):
        """Test URL validation with valid URLs"""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com/path"
        ]

        for url in valid_urls:
            result = validate_and_sanitize_url(url)
            self.assertEqual(result, url)

    def test_validate_and_sanitize_url_invalid(self):
        """Test URL validation with invalid URLs"""
        invalid_urls = [
            "javascript:alert(1)",
            "vbscript:alert(1)",
            "data:text/html,<script>alert(1)</script>",
            "ftp://example.com",  # Not http/https
            "",  # Empty string
            "not-a-url"
        ]

        for url in invalid_urls:
            result = validate_and_sanitize_url(url)
            self.assertIsNone(result)

    def test_validate_and_sanitize_url_with_spaces(self):
        """Test URL validation with whitespace that should be stripped"""
        url_with_spaces = "  https://example.com  "
        result = validate_and_sanitize_url(url_with_spaces)
        self.assertEqual(result, "https://example.com")


if __name__ == '__main__':
    unittest.main()