# Quickstart: Contributing to the Textbook

**Date**: 2025-12-07

This guide provides instructions for contributing content to the "Physical AI & Humanoid Robotics" textbook.

## 1. Prerequisites

-   You have a local clone of the project repository.
-   You have Node.js and Yarn installed for running Docusaurus.
-   You have a working ROS 2 Humble environment on Ubuntu 22.04 for validating code examples.

## 2. Content Creation Workflow

1.  **Create a new lesson file**: Following the structure in `plan.md`, create a new `.mdx` file in the appropriate `content/` subdirectory.
2.  **Write the lesson content**:
    -   Follow the structure defined in `data-model.md`: title, learning goals, content, and lab.
    -   Write clear and concise explanations.
    -   Provide complete, working code examples in Python using `rclpy`.
    -   Create a hands-on lab that allows students to apply the concepts.
3.  **Validate the content**:
    -   Build the Docusaurus site locally to ensure the MDX renders correctly.
    -   Run all code examples in your ROS 2 environment to verify they work as expected.

## 3. Building the Docusaurus Site

1.  **Install dependencies**:
    ```bash
    yarn install
    ```
2.  **Start the development server**:
    ```bash
    yarn start
    ```
    This will open the site in your browser at `http://localhost:3000`. The site will automatically reload as you make changes to the content files.

## 4. Submitting Changes

1.  Commit your changes to your feature branch.
2.  Create a pull request against the `main` branch.
3.  Ensure your changes have been reviewed and approved before merging.
