# Project
AI/Spec-Driven Book Creation with Embedded RAG Chatbot

Build a technical book using **Docusaurus**, authored via **Spec-Kit Plus** and **Claude Code**, deployed to **GitHub Pages**, and augmented with an embedded **RAG chatbot** that answers questions about the book content, including answers restricted to user-selected text.

---

## Core Principles
- **Spec-first**: No content or code without an approved spec
- **Reproducibility**: Deterministic builds and deployments
- **AI discipline**: Claude Code implements specs only, no guessing
- **Transparency**: All decisions and data flows documented

---

## Book Standards
- Format: Docusaurus (Markdown)
- Audience: Software developers
- Each chapter must include:
  - Objective
  - Core concepts
  - Examples (where applicable)
  - Summary
  - Acceptance criteria

---

## Tooling
- **Spec-Kit Plus**: Source of truth for all specs
- **Claude Code**: Writing and implementation agent
- **Docusaurus**: Book framework
- **GitHub Pages**: Hosting and deployment

---

## RAG Chatbot Requirements
- Stack:
  - OpenAI Agents / ChatKit SDKs
  - FastAPI backend
  - Neon Serverless Postgres
  - Qdrant Cloud (Free Tier)
- Capabilities:
  - Answer questions using indexed book content only
  - Support answering based solely on user-selected text
  - Indicate when an answer cannot be derived from context

---

## Constraints
- No undocumented customizations
- No private or proprietary datasets
- Free-tier–compatible infrastructure only

---

## Success Criteria
- Book builds and deploys successfully to GitHub Pages
- All chapters conform to specs
- Chatbot functions correctly with RAG and selection-based context
- No hallucinated answers outside retrieved content

---

## Governing Rule
**If it is not specified, it must not be implemented.**