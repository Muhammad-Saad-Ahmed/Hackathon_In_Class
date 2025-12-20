---
id: 002
title: Overhaul Docusaurus UI to Deep Space Theme
stage: implement
date: 2025-12-07
surface: agent
model: gemini-cli
feature: ui-overhaul
branch: main
user: "placeholder"
command: "placeholder"
labels: ["ui", "docusaurus", "css", "react"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/css/custom.css
 - src/pages/index.tsx
 - src/pages/index.module.css
tests:
 - "none"
---

## Prompt

# Role
You are a Senior Frontend Designer specializing in Docusaurus, React, and Modern UI/UX.

# Goal
Overhaul the UI of my Docusaurus project ("Physical AI & Humanoid Robotics") to look **extraordinary**, futuristic, and premium. The vibe should be "OpenAI Research" meets "Cyberpunk functionality."

# Constraints & Tech Stack
- Use **pure CSS/SCSS** in `src/css/custom.css` (avoid installing Tailwind unless necessary to keep build simple).
- Use **React** for the Homepage (`src/pages/index.tsx`).
- Ensure it remains fully responsive.

# Execution Tasks

## 1. The Visual Identity (CSS Variables)
Update `src/css/custom.css` to implement a "Deep Space" Dark Mode by default.
- **Backgrounds:** Deep blue-black (`#0a0b10`) instead of grey.
- **Accents:** Neon Cyan (`#00f0ff`) and Electric Purple (`#7000ff`) for links and primary buttons.
- **Typography:** Use system fonts but styled like `Inter` (sans-serif) and `JetBrains Mono` (code).
- **Glassmorphism:** Apply a blur effect (`backdrop-filter: blur(12px)`) to the Navbar and Sidebar.

## 2. Global UI Tweaks
- **Navbar:** Make it floating (detached from top) with a subtle glow border.
- **Sidebar:** Remove the right border; use a soft gradient background instead.
- **Admonitions:** Redesign `:::note`, `:::tip`, `:::danger` to look like "Heads-Up Display" (HUD) elements with glowing left borders and dark transparent backgrounds.
- **Code Blocks:** Give them a "terminal" look—rounded corners, distinct window buttons (red/yellow/green dots) in the header.

## 3. The Hero Page (`src/pages/index.tsx`)
Completely rewrite the homepage.
- **Hero Section:** Large, centered typography. "Building the Body for the Artificial Mind."
- **Visual:** A subtle CSS animation in the background (e.g., a scanning grid or floating particles).
- **CTA Buttons:** "Start Learning" (Primary, Glowing) and "View GitHub" (Secondary, Outline).
- **Feature Grid:** A 3-column grid below the hero highlighting "ROS 2 Native," "Sim-First," and "VLA Ready" with modern SVG icons.

## 4. Typography & Readability
- Increase the max-width of the content container for better reading.
- Increase line-height for body text.
- Make H1, H2, H3 headers bold and tracking-tight (letter-spacing: -0.02em).

# Action
Generate the code for `src/css/custom.css` and `src/pages/index.tsx` that implements this vision immediately.

## Response snapshot

I have completed the UI overhaul for your Docusaurus project.

- **`src/css/custom.css`** has been updated with a "Deep Space" dark theme, including new color variables, a floating glassmorphism navbar, redesigned admonitions, and terminal-style code blocks.
- **`src/pages/index.tsx`** has been completely rewritten to feature a new hero section with a background animation, modern call-to-action buttons, and a feature grid.
- **`src/pages/index.module.css`** has been updated to style the new homepage components.

Your project now has a futuristic and premium look and feel.

## Outcome

- ✅ Impact: Major UI overhaul completed as per spec.
- 🧪 Tests: No tests were run as this was a visual-only change.
- 📁 Files: 3 files were created/modified.
- 🔁 Next prompts: The user might want to tweak the design or move to another task.
- 🧠 Reflection: The task was straightforward and the instructions were clear. The use of CSS variables and React components made the implementation clean.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Tweak the background animation.
