"""
Flashcard Generator for Markdown Documents using Google's Gemini API
"""

import json
from google import genai

def generate_flashcards_from_markdown(file_path):
    """Generate flashcards from a markdown document using Gemini API.
    
    Args:
        file_path: Path to the markdown document
        
    Returns:
        List of flashcards with question and answer fields
    """
    # Read the markdown file
    with open(file_path, "r", encoding="utf-8") as file:
        document = file.read()

    # Initialize Gemini client - move API key to environment variable in production
    client = genai.Client(
        api_key="AIzaSyBo0ujw97TVcc46Vyt7FSJ0SWs1xfVk5bM"
    )

    # Use gemini-2.0-flash model
    model = "gemini-2.0-flash"

    # Configure response schema to structure flashcards
    generate_content_config = genai.types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "flashcards": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        properties={
                            "question": genai.types.Schema(
                                type=genai.types.Type.STRING,
                            ),
                            "answer": genai.types.Schema(
                                type=genai.types.Type.STRING,
                            ),
                        },
                    ),
                ),
            },
        ),
    )

    content = """
    Generate flashcards from the following markdown document.
    Document:
    {}
    """.format(document)

    # Generate flashcards using Gemini
    response = client.models.generate_content(
        model=model,
        contents=content,
        config=generate_content_config,
    )

    # Extract flashcards from response
    response = json.loads(response.text)
    print(f"Generated {len(response['flashcards'])} flashcards.")

    return response['flashcards']

def save_flashcards_to_subject(flashcards, subject_id):
    """Save generated flashcards to a subject.
    
    Args:
        flashcards: List of flashcards with question and answer fields
        subject_id: ID of the subject to save flashcards to
        
    Returns:
        Number of flashcards saved
    """
    from utils import add_flashcard_to_subject  # Local import to avoid circular imports
    
    count = 0
    for flashcard in flashcards:
        try:
            add_flashcard_to_subject(subject_id, {
                'question': flashcard['question'],
                'answer': flashcard['answer']
            })
            count += 1
        except Exception as e:
            print(f"Error adding flashcard: {str(e)}")
    
    return count

# Example usage
if __name__ == "__main__":
    # print current working directory
    import os
    

    file_path = "data/documents/225a328d0a854e929f92d3cfdd193ddc.md"  # Replace with your markdown file path
    flashcards = generate_flashcards_from_markdown(file_path)
    
    print("Generated Flashcards:")
    for i, flashcard in enumerate(flashcards, 1):
        print(f"Flashcard {i}:")
        print(f"Question: {flashcard['question']}")
        print(f"Answer: {flashcard['answer']}")
        print()
