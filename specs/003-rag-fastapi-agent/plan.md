# Implementation Plan: RAG Agent using OpenAI SDK

**Branch**: `003-rag-fastapi-agent` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-rag-fastapi-agent/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The plan is to create a RAG agent using the OpenAI Agents SDK. The agent will be implemented in a new `agent.py` file inside the `backend` directory. It will take a user query, use functionality from `retrieving.py` to fetch relevant documents from a Qdrant database, and then use an OpenAI model to generate an answer. This is a change from the original specification, which proposed a FastAPI endpoint. The immediate goal is to have a working agent script.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: `openai`, `qdrant-client`, `sentence-transformers`, `typer`
**Storage**: Qdrant Cloud
**Testing**: `pytest`
**Target Platform**: Local execution via Python script
**Project Type**: Single project (`backend`)
**Performance Goals**: Not critical for the initial script-based implementation.
**Constraints**: Must use OpenAI API key from `.env` file. No FastAPI implementation for now.
**Scale/Scope**: A single agent capable of handling one query at a time.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-first**: VIOLATION. The user has requested a change in implementation (no FastAPI, use `agent.py`) that deviates from the approved `spec.md`. This is a user-driven change to simplify the immediate goal. All other principles are respected.

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-fastapi-agent/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── __init__.py
├── main.py
├── requirements.txt
├── retrieving.py
├── agent.py           # New file for the agent
└── tests/
    ├── __init__.py
    ├── test_retrieving.py
    └── test_agent.py    # New test file for the agent
```

**Structure Decision**: The existing `backend` directory will be used. A new `agent.py` file will be created for the agent logic, and `test_agent.py` for its tests. This keeps the new functionality within the existing backend structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Deviation from spec | User requested a more direct implementation focusing on the agent logic first, deferring the web interface. | Sticking to the original spec would involve building a FastAPI wrapper which is not the user's current priority. |