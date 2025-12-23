# Actionable Tasks for: RAG Agent

**Implementation Plan**: [plan.md](./plan.md)

This file breaks down the implementation of the RAG Agent feature into actionable, dependency-ordered tasks.

## Phase 1: Setup

- [ ] T001 Create the agent file at `backend/agent.py`.
- [ ] T002 Create the test file at `backend/tests/test_agent.py`.
- [ ] T003 Update `backend/requirements.txt` to include `openai`, `qdrant-client`, and `sentence-transformers`.

## Phase 2: Foundational

- [ ] T004 In `backend/agent.py`, implement a `retrieve_documents` function that takes a query, embeds it, and searches Qdrant, returning a list of `DocumentChunk` objects. This will be based on the logic in `backend/retrieving.py`.
- [ ] T005 In `backend/agent.py`, set up the OpenAI client, loading the API key from a `.env` file.

## Phase 3: User Story 1 - Core RAG functionality

**Goal**: A user can submit a query and receive a relevant answer based on stored documents.
**Independent Test**: Run the agent script with a query and verify a valid answer and sources are printed.

- [ ] T006 [US1] In `backend/agent.py`, implement the main `run_agent` function that takes a user query.
- [ ] T007 [US1] In `run_agent`, call `retrieve_documents` to get the context.
- [ ] T008 [US1] In `run_agent`, construct a prompt for the OpenAI completions API, including the user query and the retrieved context.
- [ ] T009 [US1] In `run_agent`, call the OpenAI API to get the generated answer.
- [ ] T010 [US1] In `run_agent`, print the answer and the sources to the console.
- [ ] T011 [US1] [P] In `backend/tests/test_agent.py`, add a test that calls `run_agent` with a sample query and asserts that a non-empty answer is returned.

## Phase 4: User Story 2 - Error Handling

**Goal**: The system gracefully handles invalid queries or cases with no results.
**Independent Test**: Run the agent with an empty query and with a query that yields no results, and verify the correct error messages are shown.

- [ ] T012 [US2] In `backend/agent.py`, add a check at the beginning of `run_agent` to handle empty or None queries.
- [ ] T013 [US2] In `backend/agent.py`, handle the case where `retrieve_documents` returns no documents, providing a "could not find an answer" message.
- [ ] T014 [US2] [P] In `backend/tests/test_agent.py`, add a test for the empty query case.
- [ ] T015 [US2] [P] In `backend/tests/test_agent.py`, add a test for the no-documents-found case (this may require mocking the retrieval function).

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T016 Add docstrings and type hinting to all new functions in `backend/agent.py`.
- [ ] T017 Add a main execution block in `backend/agent.py` to allow running it as a script with command-line arguments (using `argparse` or `typer`).

## Dependencies

- **User Story 2 (Error Handling)** depends on **User Story 1 (Core RAG functionality)**.

## Parallel Execution

- Within each user story phase, the implementation tasks are largely sequential.
- However, tests ([P] tasks) for a user story can be written in parallel with its implementation.

## Implementation Strategy

1.  **MVP First**: Implement all tasks for User Story 1 to get a working end-to-end flow.
2.  **Incremental Delivery**: Subsequently, implement tasks for User Story 2 to add robustness.
3.  **Polish**: Finalize the implementation with documentation and polish tasks.
