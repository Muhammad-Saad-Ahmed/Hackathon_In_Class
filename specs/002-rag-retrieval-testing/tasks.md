# Tasks: RAG Retrieval Pipeline Testing

**Feature**: `002-rag-retrieval-testing`
**Spec**: [specs/002-rag-retrieval-testing/spec.md](specs/002-rag-retrieval-testing/spec.md)
**Plan**: [specs/002-rag-retrieval-testing/plan.md](specs/002-rag-retrieval-testing/plan.md)

This document breaks down the implementation of the RAG retrieval pipeline testing feature into actionable, dependency-ordered tasks.

## Phase 1: Setup

- [x] T001 Create the file `backend/retrieving.py` with a basic main function guard.
- [x] T002 [P] Create a `backend/requirements.txt` file and add `qdrant-client`, `typer[all]`, `sentence-transformers`, and `pytest`.

## Phase 2: Foundational (CLI & Client Initialization)

- [x] T003 In `backend/retrieving.py`, set up a `typer` application and a command that accepts a `--query` string argument.
- [x] T004 In `backend/retrieving.py`, implement the initialization of the `QdrantClient` and `SentenceTransformer` model, reading connection details from environment variables as specified in `quickstart.md`.

## Phase 3: User Story 1 - Verify Top-K Retrieval

- **Goal**: Implement the core logic to query Qdrant and retrieve results.
- **Independent Test**: Can be tested by calling the search function with a mock client and verifying that it processes the query correctly.

- [x] T005 [US1] In `backend/retrieving.py`, encode the input query string into a vector using the `SentenceTransformer` model.
- [x] T006 [US1] In `backend/retrieving.py`, call the Qdrant client's `search` method with the query vector and retrieve the raw search hits.

## Phase 4: User Story 2 - Validate Metadata Integrity

- **Goal**: Process the raw search results to extract and validate metadata.
- **Independent Test**: Can be tested by providing a sample of raw Qdrant hits to a processing function and asserting that the structured data is correct.

- [x] T007 [US2] In `backend/retrieving.py`, define a Pydantic or dataclass model for the `RetrievalResult` item as defined in `data-model.md`.
- [x] T008 [US2] In `backend/retrieving.py`, implement a function to process the raw search hits from Qdrant into a list of `RetrievalResult` objects, ensuring payload data like `text`, `url`, and `chunk_id` is correctly extracted.

## Phase 5: User Story 3 - Confirm End-to-End Pipeline Output

- **Goal**: Format the processed results into the final JSON output.
- **Independent Test**: The whole script can be run with a mock client, and its standard output can be captured and validated against an expected JSON structure.

- [x] T009 [US3] In `backend/retrieving.py`, integrate the processing function into the main `typer` command.
- [x] T010 [US3] In `backend/retrieving.py`, convert the final list of `RetrievalResult` objects to a JSON string and print it to standard output.

## Phase 6: Testing

- [x] T011 Create the test file `backend/tests/test_retrieving.py` with initial setup.
- [x] T012 [P] In `backend/tests/test_retrieving.py`, write a test for the Typer CLI command structure using `CliRunner` to ensure the `--query` argument is handled correctly.
- [x] T013 [P] In `backend/tests/test_retrieving.py`, write a unit test for the search functionality, mocking the `QdrantClient` to return sample data and asserting the processing logic is correct.
- [x] T014 In `backend/tests/test_retrieving.py`, write an integration test that runs the full script with a mocked client and validates the structure and content of the final JSON output.

## Dependencies & Execution Order

The feature will be delivered incrementally, following the user story priorities.

1.  **MVP (User Story 1)**: Complete phases 1, 2, and 3. This delivers the core retrieval logic.
2.  **Increment 2 (User Story 2)**: Complete Phase 4. This adds metadata processing.
3.  **Increment 3 (User Story 3)**: Complete Phase 5. This provides the final, clean JSON output.
4.  **Testing**: Phase 6 can be worked on in parallel with the feature development.

### Parallel Execution

-   **Initial Setup**: T001 and T002 can be done in parallel.
-   **Testing**: T012 and T013 can be worked on in parallel by different developers once the initial file structure is in place.
