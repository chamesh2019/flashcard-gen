# Flashcard Generator Backend

This is the backend for the Flashcard Generator application. It provides API endpoints for creating and retrieving flashcards, subjects, and handling document uploads.

## Document Upload

The application now accepts **Markdown files only** (.md or .markdown) for document uploads. The system uses Google's Gemini API to automatically generate flashcards from these markdown documents.

## Setting Up

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```
   flask run
   ```

## Using the Markdown Flashcard Generator

The `markdown_flashcard_generator.py` module provides functionality to generate flashcards from markdown documents. It uses Google's Gemini API to analyze the content and create question-answer pairs.

Example usage:

```python
from markdown_flashcard_generator import generate_flashcards_from_markdown

# Generate flashcards from a markdown file
flashcards = generate_flashcards_from_markdown("path/to/document.md")

# Print the generated flashcards
for flashcard in flashcards:
    print(f"Q: {flashcard['question']}")
    print(f"A: {flashcard['answer']}")
    print()
```

## API Endpoints

- GET `/api/subjects` - Get all subjects
- POST `/api/subjects` - Create a new subject
- GET `/api/subjects-summary` - Get subjects with flashcard counts
- GET `/api/subjects/<subject_id>/flashcards` - Get flashcards for a subject
- POST `/api/document` - Upload a markdown document
- GET `/api/documents/<document_id>/download` - Download a document

## Running with Docker

You can run this project using Docker for a consistent and isolated environment.

- **Python version:** The Docker image uses `python:3.13-slim`.
- **Ports:** The backend service is exposed on port **5000**.
- **Environment variables:** No required environment variables are set by default. If you need to use a `.env` file, uncomment the `env_file` line in the `docker-compose.yml`.

### Build and Run

1. Build and start the service using Docker Compose:
   ```
   docker compose up --build
   ```
   This will build the image and start the backend at [http://localhost:5000](http://localhost:5000).

2. To stop the service:
   ```
   docker compose down
   ```

- No additional configuration or external services are required.
- All dependencies are installed inside a Python virtual environment within the container.
- The application runs as a non-root user for improved security.

If you need to customize environment variables, create a `.env` file in the project root and uncomment the `env_file` line in the `docker-compose.yml`.
