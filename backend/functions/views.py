from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import random
from functions.utils import (
    get_all_subjects,
    add_new_subject,
    get_flashcards_for_subject,
    add_flashcard_to_subject,
    ensure_data_files_exist,
    get_subjects_with_flashcard_counts,
    save_document_file,
    get_all_documents,
    delete_document,
    mark_document_as_processed,
    load_data,
    DOCUMENTS_FOLDER,
    DOCUMENT_INDEX_FILE,
    get_documents_by_subject,
    get_flashcards_for_document
)

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Set maximum file size to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Define allowed file extensions - only markdown is allowed
ALLOWED_EXTENSIONS = {'md', 'markdown'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/subjects', methods=['GET'])
def api_get_subjects():
    """API endpoint to get all subjects."""
    return jsonify(get_all_subjects())

@app.route('/api/subjects-summary', methods=['GET'])
def api_get_subjects_summary():
    """API endpoint to get all subjects with their flashcard counts."""
    return jsonify(get_subjects_with_flashcard_counts())

@app.route('/api/subjects', methods=['POST'])
def api_add_subject():
    """API endpoint to add a new subject."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Subject name is required'}), 400
    
    subjects = get_all_subjects()
    if any(s['name'].lower() == data['name'].lower() for s in subjects):
        return jsonify({'error': 'Subject name already exists'}), 409 # Conflict

    new_subject = add_new_subject(data)
    return jsonify(new_subject), 201

@app.route('/api/document', methods=['POST'])
def api_upload_document():
    """API endpoint for file upload."""
    # Check if subject_id is provided
    subject_id = request.form.get('subject_id')
    if not subject_id:
        return jsonify({'error': 'Subject ID is required'}), 400
    
    # Check if the subject exists
    subjects = get_all_subjects()
    if not any(s['id'] == subject_id for s in subjects):
        return jsonify({'error': 'Subject not found'}), 404

    # Check if file part exists in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if the file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    
    try:
        document_record = save_document_file(file, filename, subject_id)
        return jsonify({
            'message': 'File uploaded successfully',
            'document': document_record
        }), 201
    except Exception as e:
        return jsonify({'error': f'Error saving file: {str(e)}'}), 500

@app.route('/api/documents/<string:document_id>/download', methods=['GET'])
def api_download_document(document_id):
    """API endpoint to download a document by its ID."""
    from .utils import load_data, DOCUMENT_INDEX_FILE
    
    document_index = load_data(DOCUMENT_INDEX_FILE)
    document = next((doc for doc in document_index if doc['id'] == document_id), None)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    return send_from_directory(
        DOCUMENTS_FOLDER, 
        document['stored_filename'],
        as_attachment=True,
        download_name=document['original_filename']
    )

@app.route('/api/subjects/<subject_id>/flashcards', methods=['GET'])
def api_get_flashcards(subject_id):
    """API endpoint to get flashcards for a specific subject."""
    subjects = get_all_subjects()

    if not any(s['id'] == str(subject_id) for s in subjects):
        return jsonify({'error': 'Subject not found'}), 404
    flashcards = get_flashcards_for_subject(subject_id)

    # shuffle the flashcards
    random.shuffle(flashcards)

    return jsonify(flashcards)

@app.route('/api/documents', methods=['GET'])
def api_get_documents():
    """API endpoint to get all documents."""
    return jsonify(get_all_documents())

@app.route('/api/documents/<string:document_id>', methods=['DELETE'])
def api_delete_document(document_id):
    """API endpoint to delete a document."""
    success, message = delete_document(document_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 404

@app.route('/api/documents/<string:document_id>/process', methods=['POST'])
def api_process_document(document_id):
    """API endpoint to process a document and generate flashcards."""
    from .markdown_flashcard_generator import generate_flashcards_from_markdown
    import os
    import traceback
    
    # Get the document details
    document_index = load_data(DOCUMENT_INDEX_FILE)
    document = next((doc for doc in document_index if doc['id'] == document_id), None)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    try:
        # Build the full path to the document
        document_path = os.path.join(DOCUMENTS_FOLDER, document['stored_filename'])
        
        # Generate flashcards from the markdown document
        flashcards = generate_flashcards_from_markdown(document_path)
          # Save the flashcards directly to the subject, including document_id
        count = 0
        for flashcard in flashcards:
            add_flashcard_to_subject(document['subject_id'], {
                'question': flashcard['question'],
                'answer': flashcard['answer']
            }, document_id)  # Pass document_id to associate flashcards with this document
            count += 1
        
        # Mark the document as processed
        success, _ = mark_document_as_processed(document_id)
        if not success:
            return jsonify({'error': 'Failed to update document status'}), 500
        
        return jsonify({
            'message': f'Document processed successfully. Generated {count} flashcards.',
            'flashcardCount': count
        }), 200
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error processing document: {str(e)}\n{error_traceback}")
        return jsonify({'error': f'Error processing document: {str(e)}'}), 500

@app.route('/api/subjects/<subject_id>/documents', methods=['GET'])
def api_get_documents_by_subject(subject_id):
    """API endpoint to get all documents for a specific subject."""
    subjects = get_all_subjects()

    if not any(s['id'] == str(subject_id) for s in subjects):
        return jsonify({'error': 'Subject not found'}), 404
    
    documents = get_documents_by_subject(subject_id)
    return jsonify(documents)

@app.route('/api/subjects/<subject_id>/documents/<document_id>/flashcards', methods=['GET'])
def api_get_flashcards_by_document(subject_id, document_id):
    """API endpoint to get flashcards for a specific document within a subject.
    """
    subjects = get_all_subjects()

    if not any(s['id'] == str(subject_id) for s in subjects):
        return jsonify({'error': 'Subject not found'}), 404
    
    # Get flashcards for this specific document
    flashcards = get_flashcards_for_document(subject_id, document_id)
    
    # If we have flashcards, return them even if the document is deleted
    if flashcards:
        # Shuffle the flashcards for randomized practice
        random.shuffle(flashcards)
        return jsonify(flashcards)
    
    # If no flashcards found, check if the document exists (might not be processed)
    document_index = load_data(DOCUMENT_INDEX_FILE)
    document = next((doc for doc in document_index if doc['id'] == document_id and doc['subject_id'] == str(subject_id)), None)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    if document.get('deleted', False):
        return jsonify({'error': 'Document has been deleted and has no associated flashcards'}), 404
    
    # Document exists but has no flashcards, check if it's been processed
    if not document.get('processed', False):
        return jsonify({'error': 'Document has not been processed yet'}), 400
    
    # Document is processed but has no flashcards (unusual case)
    return jsonify([])  # Return empty array

@app.route('/api/subjects/<subject_id>/documents/<document_id>/info', methods=['GET'])
def api_get_document_info(subject_id, document_id):
    """API endpoint to get info for a specific document, including deleted ones."""
    subjects = get_all_subjects()

    if not any(s['id'] == str(subject_id) for s in subjects):
        return jsonify({'error': 'Subject not found'}), 404
    
    # Check for the document in the document index, including deleted ones
    document_index = load_data(DOCUMENT_INDEX_FILE)
    document = next((doc for doc in document_index if doc['id'] == document_id and doc['subject_id'] == str(subject_id)), None)
    
    if document:
        return jsonify(document)
    else:
        return jsonify({'error': 'Document not found'}), 404

def create_app():
    """Application factory function."""
    ensure_data_files_exist() # Ensure data files are ready when app starts
    return app
