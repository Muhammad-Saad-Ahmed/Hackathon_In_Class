import json
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from ..retrieving import app, RetrievalResult


runner = CliRunner()

def test_retrieve_cli_command_json_output():
    with patch('backend.retrieving.get_qdrant_client') as mock_get_client, \
         patch('backend.retrieving.SentenceTransformer') as mock_sentence_transformer:

        # Mock Qdrant client
        mock_qdrant_client = MagicMock()
        mock_get_client.return_value = mock_qdrant_client
        
        # Mock SentenceTransformer
        mock_encoder = MagicMock()
        mock_sentence_transformer.return_value = mock_encoder
        mock_encoder.encode.return_value.tolist.return_value = [0.1, 0.2, 0.3]

        # Mock the search result from Qdrant
        mock_hits = [
            MagicMock(
                score=0.9,
                payload={'text': 'test text 1', 'metadata': {'url': '/test1', 'chunk_id': 1}}
            ),
            MagicMock(
                score=0.8,
                payload={'text': 'test text 2', 'metadata': {'url': '/test2', 'chunk_id': 2}}
            )
        ]
        mock_qdrant_client.search.return_value = mock_hits

        result = runner.invoke(app, ["--query", "test query"])
        assert result.exit_code == 0, f"CLI command failed with exception: {result.exception}"
        
        # Validate the JSON output
        output_json = json.loads(result.stdout)
        assert isinstance(output_json, list)
        assert len(output_json) == 2
        assert output_json[0]['text'] == 'test text 1'
        assert output_json[0]['url'] == '/test1'
        assert output_json[0]['chunkId'] == 1
        assert output_json[0]['score'] == 0.9

def test_process_hits():
    from ..retrieving import process_hits
    
    hits = [
        MagicMock(
            score=0.9,
            payload={'text': 'test text', 'metadata': {'url': '/test', 'chunk_id': 1}}
        )
    ]
    
    results = process_hits(hits)
    assert len(results) == 1
    assert isinstance(results[0], RetrievalResult)
    assert results[0].text == "test text"
    assert results[0].score == 0.9
