# Implementation Plan: RAG UI Integration

**Branch**: `004-rag-ui-integration` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/004-rag-ui-integration/spec.md`

## Summary

The plan is to productionize the RAG agent by wrapping it in a FastAPI server, and to create a new React-based chat component in the Docusaurus frontend. This chat component will be displayed on all pages and will communicate with the FastAPI backend to provide answers to user questions.

## Technical Context

**Backend**: Python 3.11, FastAPI, `openai`, `qdrant-client`, `sentence-transformers`, `uvicorn`
**Frontend**: Docusaurus (React, TypeScript), `axios` for API calls
**Storage**: Qdrant Cloud
**Testing**: `pytest` for backend, Jest/React Testing Library for frontend
**Project Type**: Web application (frontend/backend)
**Performance Goals**: API responses should be under 5 seconds.
**Constraints**: The chat UI should be a non-intrusive overlay on the existing Docusaurus site.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan aligns with the project constitution. All technologies are within the defined stack, and the feature follows the "spec-first" principle.

## Project Structure

### Documentation (this feature)

```text
specs/004-rag-ui-integration/
├── plan.md              # This file
├── research.md          # Research on Docusaurus swizzling
├── data-model.md        # Data model for the API
├── quickstart.md        # Instructions to run the feature
├── contracts/           # OpenAPI specification
└── tasks.md             # Implementation tasks (to be generated)
```

### Source Code (repository root)

```text
backend/
├── agent.py             # Existing agent logic, to be modified for FastAPI
├── embedding_pipeline.py # Renamed from main.py
├── main.py                # New FastAPI application
└── tests/
    └── test_agent.py      # To be updated for the API endpoint

src/
├── theme/
│   ├── Root.tsx           # Swizzled Root component to include the chat UI
│   └── ChatComponent/
│       ├── index.tsx      # The main chat component
│       └── styles.css   # Styles for the chat component
└── ... (existing docusaurus files)
```

**Structure Decision**: The backend will be served from a new `main.py` using FastAPI. The existing `agent.py` will be refactored to be callable by the API. The original `main.py` will be renamed to `embedding_pipeline.py` to avoid confusion. The frontend will have a new `ChatComponent` which will be added to all pages by swizzling the Docusaurus `Root` component.

## Complexity Tracking

No violations of the constitution that require justification.