# Research: Docusaurus UI Integration

**Date**: 2025-12-24

This document outlines the research and decisions made for integrating a custom React component into the Docusaurus site.

## Decision: Docusaurus Component Swizzling

- **Decision**: To add a persistent chat component to every page of the Docusaurus site, the `Root` component will be "swizzled".
- **Rationale**: Docusaurus's swizzling feature is the official and recommended way to customize theme components. Swizzling the `Root` component allows wrapping the entire Docusaurus application with custom components, making it the ideal place to add a site-wide chat widget that should be visible on all pages. The command to do this is `npm run swizzle @docusaurus/theme-classic Root -- --danger`. This will create a copy of the `Root` component at `src/theme/Root.tsx` which can then be safely modified.
- **Alternatives considered**:
    - **Manually editing `node_modules`**: This is not a viable long-term solution as changes would be lost on every `npm install`.
    - **Adding the component to every page manually**: This would be highly inefficient and difficult to maintain.

## Decision: FastAPI for the Backend

- **Decision**: The backend RAG agent will be served via a FastAPI application.
- **Rationale**: FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It's a good choice for this project as it's easy to use, has great documentation, and is well-suited for building the `/ask` endpoint required by the frontend. The existing agent logic in `agent.py` can be easily adapted to be called from a FastAPI endpoint.
- **Alternatives considered**:
    - **Flask**: Another popular Python web framework. FastAPI was chosen for its modern features, automatic OpenAPI documentation, and performance.
    - **Keeping the script-based agent**: This is not suitable for a web-based UI that needs to make HTTP requests.
