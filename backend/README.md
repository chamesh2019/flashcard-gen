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
