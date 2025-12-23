import pytest
from unittest.mock import patch, MagicMock
from backend.agent import run_agent, DocumentChunk

@patch('backend.agent.retrieve_documents')
@patch('backend.agent.openai.completions.create')
def test_run_agent_returns_answer(mock_openai_create, mock_retrieve_documents):
    # Arrange
    mock_retrieve_documents.return_value = [
        DocumentChunk(text="doc1", url="http://doc1.com", chunkId=1, score=0.9),
        DocumentChunk(text="doc2", url="http://doc2.com", chunkId=2, score=0.8)
    ]
    
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].text = "This is the answer."
    mock_openai_create.return_value = mock_completion
    
    # Act
    # We need to capture the print output to check it
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_agent("test query")
    output = f.getvalue()

    # Assert
    assert "Answer:" in output
    assert "This is the answer." in output
    assert "Sources:" in output
    mock_retrieve_documents.assert_called_once_with("test query")
    mock_openai_create.assert_called_once()

def test_run_agent_empty_query():
    # Act
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_agent("")
    output = f.getvalue()

    # Assert
    assert "Error: Query cannot be empty." in output

@patch('backend.agent.retrieve_documents')
def test_run_agent_no_documents_found(mock_retrieve_documents):
    # Arrange
    mock_retrieve_documents.return_value = []
    
    # Act
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_agent("test query")
    output = f.getvalue()

    # Assert
    assert "Could not find an answer to your question." in output
    mock_retrieve_documents.assert_called_once_with("test query")
