---
id: 001
title: Establish Project Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: gemini-pro
feature: none
branch: main
user: unspecified
command: /sp.constitution
labels: [constitution, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: Physical AI & Humanoid Robotics — Textbook + RAG Chatbot

Vision:
Create an AI-generated Docusaurus textbook on Physical AI & Humanoid Robotics, with an integrated RAG chatbot that answers questions strictly from the book’s content.

Audience:
Beginner–intermediate AI/robotics students learning ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA systems.

Core Principles:
- Technical accuracy (ROS 2, Gazebo, Unity, Isaac, VLA)
- Hands-on learning (labs + code demos)
- Clear, structured teaching (Modules → Chapters → Lessons)
- Consistent Python/ROS 2 examples
- Book content and chatbot logic remain separate

Standards:
- Fully MDX-ready Docusaurus content
- Spec-Kit Plus workflow: Constitution → Spec → Plan → Tasks → Implement
- RAG system uses FastAPI, Neon Postgres, Qdrant Cloud, and OpenAI Agents/ChatKit
- Each lesson includes learning goals, explanation, code, and a lab

Constraints:
- Exactly 4 modules:
  1. ROS 2 — Robotic Nervous System
  2. Gazebo & Unity — Digital Twin
  3. NVIDIA Isaac — AI-Robot Brain
  4. VLA — Vision-Language-Action Robotics
- No chatbot code inside textbook chapters
- All output must be valid MDX for Docusaurus

Success Criteria:
- Complete textbook with all modules, chapters, and lessons
- Docusaurus builds and deploys to GitHub Pages
- RAG chatbot answers using ONLY book text
- Students can complete the final humanoid robot capstone project

## Response snapshot

I have updated the project constitution and ensured all dependent templates are in sync.

- **New Version**: 1.0.0
- **Rationale for bump**: Initial version of the constitution.
- **Files updated**:
  - `.specify/memory/constitution.md`
  - `.specify/templates/plan-template.md`
- **Suggested commit message**: `docs: establish constitution v1.0.0`

## Outcome

- ✅ Impact: The project constitution has been established, providing a clear set of principles and guidelines for the project.
- 🧪 Tests: Not applicable for this task.
- 📁 Files: The constitution file and the plan template have been updated.
- 🔁 Next prompts: The next step would be to start a new feature by running `/sp.specify`.
- 🧠 Reflection: The process of updating the constitution and its dependent templates went smoothly. The instructions were clear and easy to follow.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
