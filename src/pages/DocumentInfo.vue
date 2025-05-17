<template>
    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Document Management</h1>
            <p class="page-description">Manage your uploaded documents and generate flashcards</p>
        </div>

        <div v-if="actionMessage" class="message-box success-message">
            <p>{{ actionMessage }}</p>
        </div>

        <div v-if="isLoading" class="message-box info-message">
            <div class="loading-indicator">
                <span class="loading-spinner"></span>
                <p>Loading documents...</p>
            </div>
        </div>

        <div v-else-if="error" class="message-box error-message">
            <p>{{ error }}</p>
            <button @click="fetchDocuments" class="btn btn-primary">Try Again</button>
        </div>

        <div v-else-if="documents.length === 0" class="message-box info-message empty-state">
            <p>No documents have been uploaded yet.</p>
            <router-link to="/upload-document" class="btn btn-primary">
                <span class="icon">📄</span> Upload a document
            </router-link>
        </div>
        <div v-else class="documents-list">
            <table>
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>Subject</th>
                        <th>Upload Date</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="doc in documents" :key="doc.id">
                        <td class="filename-cell">
                            <div class="file-icon">📄</div>
                            <div class="file-info">
                                <span class="file-name">{{ doc.original_filename }}</span>
                            </div>
                        </td>
                        <td>{{ getSubjectName(doc.subject_id) }}</td>
                        <td>{{ formatDate(doc.uploaded_at) }}</td>
                        <td>
                            <span class="status-indicator"
                                :class="doc.processed ? 'status-processed' : 'status-pending'">
                                <span class="status-dot"></span>
                                {{ doc.processed ? 'Processed' : 'Pending' }}
                            </span>
                        </td>
                        <td class="action-buttons"> <a :href="`${apiBaseUrl}/api/documents/${doc.id}/download`"
                                class="btn btn-primary">
                                <span class="icon">⬇️</span> Download
                            </a>
                            <button v-if="!doc.processed" @click="processDocument(doc)" class="btn btn-success"
                                :disabled="processingDocId === doc.id">
                                <span class="icon">⚙️</span>
                                {{ processingDocId === doc.id ? 'Processing...' : 'Process' }}
                            </button>
                            <button @click="deleteDocument(doc)" class="btn btn-danger"
                                :disabled="deletingDocId === doc.id">
                                <span class="icon">🗑️</span>
                                {{ deletingDocId === doc.id ? 'Deleting...' : 'Delete' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import config from '../config';

const apiBaseUrl = config.apiBaseUrl;
const documents = ref([]);
const subjects = ref([]);
const isLoading = ref(true);
const error = ref('');
const processingDocId = ref(null);
const deletingDocId = ref(null);
const actionMessage = ref('');

const fetchDocuments = async () => {
    isLoading.value = true;
    error.value = '';

    try {        // Fetch documents
        const documentsResponse = await fetch(`${apiBaseUrl}/api/documents`);
        if (!documentsResponse.ok) {
            throw new Error(`Failed to fetch documents: ${documentsResponse.statusText}`);
        }
        documents.value = await documentsResponse.json();        // Also fetch subjects to display subject names
        const subjectsResponse = await fetch(`${apiBaseUrl}/api/subjects`);
        if (!subjectsResponse.ok) {
            throw new Error(`Failed to fetch subjects: ${subjectsResponse.statusText}`);
        }
        subjects.value = await subjectsResponse.json();
    } catch (err) {
        console.error('Error fetching data:', err);
        error.value = err.message || 'Failed to load documents. Please try again.';
    } finally {
        isLoading.value = false;
    }
};

const getSubjectName = (subjectId) => {
    const subject = subjects.value.find(s => s.id === subjectId);
    return subject ? subject.name : 'Unknown Subject';
};

const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
};

const processDocument = async (doc) => {
    processingDocId.value = doc.id; try {
        const response = await fetch(`${apiBaseUrl}/api/documents/${doc.id}/process`, {
            method: 'POST'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to process document');
        }

        const responseData = await response.json();        // On success, update the document in our local state
        const updatedDoc = { ...doc, processed: true };
        documents.value = documents.value.map(d => d.id === doc.id ? updatedDoc : d);

        // Show success message with flashcard count
        actionMessage.value = responseData.message || `Document processed successfully! Generated ${responseData.flashcardCount || 0} flashcards.`;
        setTimeout(() => { actionMessage.value = ''; }, 5000);
    } catch (err) {
        console.error('Error processing document:', err);
        error.value = err.message || 'Failed to process document';
        setTimeout(() => { error.value = ''; }, 3000);
    } finally {
        processingDocId.value = null;
    }
};

const deleteDocument = async (doc) => {
    if (!confirm(`Are you sure you want to delete "${doc.original_filename}"?\n\nNote: Any flashcards generated from this document will be preserved and will still be available for practice.`)) {
        return;
    }

    deletingDocId.value = doc.id; try {
        const response = await fetch(`${apiBaseUrl}/api/documents/${doc.id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to delete document');
        }

        // On success, remove the document from our local state
        documents.value = documents.value.filter(d => d.id !== doc.id);        // Show success message making it clear that flashcards are preserved
        actionMessage.value = 'Document deleted successfully! Any generated flashcards have been preserved and are still available for practice.';
        setTimeout(() => { actionMessage.value = ''; }, 5000);
    } catch (err) {
        console.error('Error deleting document:', err);
        error.value = err.message || 'Failed to delete document';
        setTimeout(() => { error.value = ''; }, 3000);
    } finally {
        deletingDocId.value = null;
    }
};

onMounted(() => {
    fetchDocuments();
});
</script>

<style scoped>
th {
    background-color: #f8fafc;
    padding: 1rem;
}

td {
    padding: 1rem;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f9fafb;
}

tr:last-child td {
    border-bottom: none;
}

/* Cell content styling */
.filename-cell {
    display: flex;
    align-items: center;
}

.file-icon {
    margin-right: 0.75rem;
    font-size: 1.25rem;
}

.file-info {
    display: flex;
    flex-direction: column;
}

.file-name {
    font-weight: 500;
}

.loading-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading-spinner {
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    border: 3px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: var(--primary-color);
    animation: spin 1s ease-in-out infinite;
    margin-right: 0.75rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-weight: 500;
    font-size: 0.875rem;
}

.status-processed {
    background-color: var(--success-color);
    color: white;
}

.status-pending {
    background-color: var(--warning-color);
    color: white;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    background-color: rgba(255, 255, 255, 0.8);
}

.empty-state {
    text-align: center;
    padding: 2rem;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    min-width: 240px;
    /* Ensures consistent width for action column */
}

/* Button styling for table actions */
.action-buttons .btn {
    margin-bottom: 0.25rem;
    white-space: nowrap;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
}

button:disabled,
button[disabled] {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>
