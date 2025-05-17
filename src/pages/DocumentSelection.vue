<template>
    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Select Document</h1>
            <p v-if="subjectName" class="page-description">Subject: {{ subjectName }}</p>
        </div>

        <div v-if="isLoading" class="message-box info-message">
            <div class="loading-indicator">
                <span class="loading-spinner"></span>
                <p>Loading documents...</p>
            </div>
        </div>

        <div v-else-if="errorMessage" class="message-box error-message">
            <p>{{ errorMessage }}</p>
            <router-link to="/" class="btn btn-primary">Back to Home</router-link>
        </div>

        <div v-else-if="documents.length === 0" class="message-box warning-message">
            <p>No documents found for this subject.</p>
            <router-link :to="{ name: 'UploadDocument' }" class="btn btn-primary">Upload a Document</router-link>
            <router-link to="/" class="btn btn-secondary">Back to Home</router-link>
        </div>

        <div v-else class="document-grid">
            <div v-for="document in documents" :key="document.id" class="document-card card">
                <div class="document-card-content">
                    <h3 class="document-title">{{ document.original_filename }}</h3>
                    <p class="document-date">Uploaded: {{ formatDate(document.uploaded_at) }}</p>
                    <div class="document-status" :class="document.processed ? 'processed' : 'not-processed'">
                        <span class="status-indicator"></span>
                        {{ document.processed ? 'Processed' : 'Not Processed' }}
                    </div>
                </div>
                <div class="document-actions">
                    <button @click="startPractice(document)" class="btn btn-primary" :disabled="!document.processed"
                        :title="!document.processed ? 'Document must be processed before practicing' : 'Start practicing with this document'">
                        Practice
                    </button>
                </div>
            </div>
        </div>

        <div class="page-actions">
            <router-link to="/" class="btn btn-secondary">
                Back to Home
            </router-link>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import config from '../config';

const route = useRoute();
const router = useRouter();
const apiBaseUrl = config.apiBaseUrl;
const subjectId = ref('');
const subjectName = ref('');
const documents = ref([]);
const isLoading = ref(true);
const errorMessage = ref('');

// Fetch documents for the selected subject
const fetchDocuments = async () => {
    isLoading.value = true;
    errorMessage.value = ''; try {
        // First fetch the subject details to get the name
        const subjectsResponse = await fetch(`${apiBaseUrl}/api/subjects-summary`);
        if (!subjectsResponse.ok) throw new Error('Failed to fetch subject details');

        const subjectsData = await subjectsResponse.json();
        const subject = subjectsData.find(s => s.id === subjectId.value);
        if (subject) {
            subjectName.value = subject.name;
        }

        // Then fetch the documents for this subject
        const response = await fetch(`${apiBaseUrl}/api/subjects/${subjectId.value}/documents`);

        if (!response.ok) {
            throw new Error(`Failed to fetch documents: ${response.statusText} (${response.status})`);
        }

        documents.value = await response.json();
    } catch (error) {
        console.error('Error fetching documents:', error);
        errorMessage.value = error.message || 'Could not load documents for this subject.';
    }

    isLoading.value = false;
};

// Format date for display
const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

// Start practice with the selected document
const startPractice = (document) => {
    if (!document.processed) {
        return; // Don't allow practice if document isn't processed
    }

    router.push({
        name: 'FlashcardPractice',
        params: {
            subjectId: subjectId.value,
            documentId: document.id
        }
    });
};

onMounted(() => {
    subjectId.value = route.params.subjectId;
    if (!subjectId.value) {
        errorMessage.value = 'No subject ID provided.';
        isLoading.value = false;
        return;
    }

    fetchDocuments();
});
</script>

<style scoped>
.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
}

.page-header {
    margin-bottom: 2rem;
}

.page-title {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.page-description {
    color: var(--text-light);
    font-size: 1.1rem;
}

.document-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.document-card {
    display: flex;
    flex-direction: column;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.document-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.document-card-content {
    flex-grow: 1;
    margin-bottom: 1rem;
}

.document-title {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    word-wrap: break-word;
}

.document-date {
    color: var(--text-light);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.document-status {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
}

.processed .status-indicator {
    background-color: #34A853;
    /* Google green */
}

.not-processed .status-indicator {
    background-color: #FBBC04;
    /* Google yellow */
}

.processed {
    color: #34A853;
}

.not-processed {
    color: #FBBC04;
}

.document-actions {
    display: flex;
    justify-content: flex-end;
}

.btn {
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.btn-primary {
    background-color: #4285F4;
    /* Google blue */
    color: white;
    border: none;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3);
}

.btn-primary:hover:not(:disabled) {
    background-color: #3367D6;
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4);
}

.btn-primary:disabled {
    background-color: #a2b9e6;
    cursor: not-allowed;
    opacity: 0.7;
    box-shadow: none;
}

.btn-secondary {
    background-color: white;
    color: #4285F4;
    border: 1px solid #4285F4;
}

.btn-secondary:hover {
    background-color: rgba(66, 133, 244, 0.05);
}

.page-actions {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
}

.loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
}

.loading-spinner {
    display: inline-block;
    width: 30px;
    height: 30px;
    border: 3px solid rgba(66, 133, 244, 0.2);
    border-radius: 50%;
    border-top-color: #4285F4;
    animation: spin 1s ease-in-out infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.message-box {
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.info-message {
    background-color: #E8F0FE;
    border: 1px solid rgba(66, 133, 244, 0.2);
}

.error-message {
    background-color: #FDECEA;
    border: 1px solid rgba(234, 67, 53, 0.2);
    color: #EA4335;
}

.warning-message {
    background-color: #FEF7E0;
    border: 1px solid rgba(251, 188, 4, 0.2);
    color: #EA8600;
}

/* Responsive adjustments */
@media (max-width: 640px) {
    .document-grid {
        grid-template-columns: 1fr;
    }

    .btn {
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
    }
}
</style>
