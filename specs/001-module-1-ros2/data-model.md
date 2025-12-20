# Data Model: Textbook Content

**Date**: 2025-12-07

This document defines the structure of the educational content entities for the "Physical AI & Humanoid Robotics" textbook.

## 1. Module

A top-level container for a major subject area.

-   **Fields**:
    -   `id` (string, e.g., `01-ros2`): A unique identifier used for the directory name.
    -   `title` (string, e.g., "Module 1 — The Robotic Nervous System (ROS 2)"): The full title of the module.
    -   `description` (string): A brief overview of the module's content.
-   **Relationships**:
    -   Has many Chapters.

## 2. Chapter

A logical grouping of lessons within a module.

-   **Fields**:
    -   `id` (string, e.g., `01-intro-to-ros2`): A unique identifier used for the directory name.
    -   `title` (string, e.g., "Chapter 1: Introduction to ROS 2"): The full title of the chapter.
    -   `description` (string): A brief overview of the chapter's content.
-   **Relationships**:
    -   Belongs to one Module.
    -   Has many Lessons.

## 3. Lesson

A single, focused learning unit.

-   **Fields**:
    -   `id` (string, e.g., `01-what-is-ros2.mdx`): A unique identifier used for the file name.
    -   `title` (string, e.g., "Lesson 1.1: What is ROS 2?"): The full title of the lesson.
    -   `learning_goals` (list of strings): A list of what the student will be able to do after completing the lesson.
    -   `content` (MDX): The main body of the lesson, including explanations and code examples.
    -   `lab` (MDX): A hands-on exercise for the student to complete.
-   **Relationships**:
    -   Belongs to one Chapter.
