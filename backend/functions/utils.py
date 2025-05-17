\
import json
import os
import uuid
from datetime import datetime

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')
SUBJECTS_FILE = os.path.join(DATA_FOLDER, 'subjects.json')
FLASHCARDS_FILE = os.path.join(DATA_FOLDER, 'flashcards.json')
DOCUMENT_INDEX_FILE = os.path.join(DATA_FOLDER, 'document_index.json')
DOCUMENTS_FOLDER = os.path.join(DATA_FOLDER, 'documents')

def ensure_data_files_exist():
    """Ensures that the data directory and JSON files exist, creating them if necessary."""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)
    if not os.path.exists(SUBJECTS_FILE):
        save_data(SUBJECTS_FILE, [])
    if not os.path.exists(FLASHCARDS_FILE):
        save_data(FLASHCARDS_FILE, {})
    if not os.path.exists(DOCUMENT_INDEX_FILE):
        save_data(DOCUMENT_INDEX_FILE, [])

def load_data(file_path):
    """Loads data from a JSON file."""
    if not os.path.exists(file_path):
        # Differentiate initial structure based on file type
        if 'subjects' in os.path.basename(file_path):
            return []
        else:
            return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError: # Handle empty or corrupted file
        return [] if 'subjects' in os.path.basename(file_path) else {}


def save_data(file_path, data):
    """Saves data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_all_subjects():
    """Retrieves all subjects from the subjects JSON file."""
    return load_data(SUBJECTS_FILE)

def get_subjects_with_flashcard_counts():
    """Retrieves all subjects and includes the count of flashcards for each."""
    subjects = get_all_subjects()
    all_flashcards = load_data(FLASHCARDS_FILE)
    
    subjects_with_counts = []
    for subject in subjects:
        count = len(all_flashcards.get(str(subject['id']), []))
        subjects_with_counts.append({
            **subject,
            'cardCount': count
        })
    return subjects_with_counts

def add_new_subject(subject_data):
    """Adds a new subject to the subjects JSON file."""
    subjects = get_all_subjects()
    if subjects:
        # Ensure IDs are integers for max() and correctly increment
        next_id = str(max(int(s['id']) for s in subjects if s['id'].isdigit()) + 1)
    else:
        next_id = '1'
    
    new_subject = {
        'id': next_id,
        'name': subject_data['name'],
        'description': subject_data.get('description', '')
    }
    subjects.append(new_subject)
    save_data(SUBJECTS_FILE, subjects)
    return new_subject

def get_flashcards_for_subject(subject_id):
    """Retrieves flashcards for a specific subject from the flashcards JSON file."""
    all_flashcards = load_data(FLASHCARDS_FILE)
    return all_flashcards.get(str(subject_id), [])

def get_flashcards_for_document(subject_id, document_id):
    """Retrieves flashcards for a specific document within a subject.
    
    Args:
        subject_id: ID of the subject
        document_id: ID of the document
        
    Returns:
        List of flashcards associated with the document, or empty list if none found.
        Note: This function will return flashcards even if the document itself has been deleted.
    """
    all_flashcards = load_data(FLASHCARDS_FILE)
    subject_flashcards = all_flashcards.get(str(subject_id), [])
    
    # Filter flashcards by document_id if provided
    if document_id:
        return [fc for fc in subject_flashcards if fc.get('document_id') == document_id]
    else:
        # Return flashcards with no document_id (legacy flashcards) or all if document_id is None
        return subject_flashcards

def add_flashcard_to_subject(subject_id, flashcard_data, document_id=None):
    """Adds a new flashcard to a subject in the flashcards JSON file.
    
    Args:
        subject_id: ID of the subject
        flashcard_data: Data for the flashcard (question, answer)
        document_id: Optional ID of the document this flashcard is associated with
    """
    all_flashcards = load_data(FLASHCARDS_FILE)
    subject_id_str = str(subject_id) # Ensure subject_id is a string for dictionary key

    if subject_id_str not in all_flashcards:
        all_flashcards[subject_id_str] = []
    
    current_flashcards = all_flashcards[subject_id_str]
    if current_flashcards:
        # Ensure IDs are integers for max() and correctly increment
        numeric_ids = [int(fc['id']) for fc in current_flashcards if fc['id'].isdigit()]
        if numeric_ids:
            next_id_num = max(numeric_ids) + 1
        else: # No numeric IDs found, start from a base
             next_id_num = int(subject_id_str) * 100 + 1 if subject_id_str.isdigit() else 1
        next_id = str(next_id_num)
    else:
        # First flashcard for a subject
        next_id = str(int(subject_id_str) * 100 + 1) if subject_id_str.isdigit() else "1"

    # Create the new flashcard with document_id if provided
    new_flashcard = {
        'id': next_id,
        'question': flashcard_data['question'],
        'answer': flashcard_data['answer'],
    }
    
    # Add document information if provided
    if document_id:
        new_flashcard['document_id'] = document_id
    
    all_flashcards[subject_id_str].append(new_flashcard)
    save_data(FLASHCARDS_FILE, all_flashcards)
    return new_flashcard

def get_all_documents():
    """Retrieves all documents from the document index JSON file."""
    documents = load_data(DOCUMENT_INDEX_FILE)
    return [doc for doc in documents]

def get_documents_by_subject(subject_id):
    """Retrieves all documents for a specific subject.
    
    Args:
        subject_id: ID of the subject to get documents for
        
    Returns:
        List of document objects for the specified subject that are not marked as deleted
    """
    all_documents = load_data(DOCUMENT_INDEX_FILE)
    subject_id_str = str(subject_id)
    return [doc for doc in all_documents if doc['subject_id'] == subject_id_str]

def delete_document(document_id):
    """Marks a document as deleted in the document index and removes the file from the file system.
    This preserves the document entry in the index (marked as deleted) and all associated flashcards.
    """
    document_index = load_data(DOCUMENT_INDEX_FILE)
    
    # Find the document with the matching ID
    document = next((doc for doc in document_index if doc['id'] == document_id), None)
    if not document:
        return False, "Document not found"
    
    # Remove the file from the file system
    file_path = os.path.join(DOCUMENTS_FOLDER, document['stored_filename'])
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        return False, f"Error deleting file: {str(e)}"
    
    # Mark the document as deleted in the index instead of removing it
    for doc in document_index:
        if doc['id'] == document_id:
            doc['deleted'] = True
            doc['deleted_at'] = datetime.now().isoformat()
    
    save_data(DOCUMENT_INDEX_FILE, document_index)
        
    return True, "Document deleted successfully (flashcards preserved)"

def mark_document_as_processed(document_id):
    """Marks a document as processed in the document index."""
    document_index = load_data(DOCUMENT_INDEX_FILE)
    
    # Find the document with the matching ID and update its processed status
    for doc in document_index:
        if doc['id'] == document_id:
            doc['processed'] = True
            doc['processed_at'] = datetime.now().isoformat()
            save_data(DOCUMENT_INDEX_FILE, document_index)
            return True, "Document marked as processed"
    
    return False, "Document not found"

def save_document_file(uploaded_file, filename, subject_id):
    """Saves an uploaded document file to the documents folder."""
    # Generate a unique filename to avoid collisions
    file_extension = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(DOCUMENTS_FOLDER, unique_filename)
    
    # Save the file
    uploaded_file.save(file_path)
    
    # Record in the document index
    document_record = {
        'id': uuid.uuid4().hex,
        'original_filename': filename,
        'stored_filename': unique_filename,
        'subject_id': subject_id,
        'uploaded_at': datetime.now().isoformat(),
        'processed': False
    }
    
    document_index = load_data(DOCUMENT_INDEX_FILE)
    document_index.append(document_record)
    save_data(DOCUMENT_INDEX_FILE, document_index)
    
    return document_record
