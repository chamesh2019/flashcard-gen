<template>
    <div class="container ignored-flashcards-page">
        <h1 class="page-title">Manage Ignored Flashcards</h1>

        <div v-if="isLoadingSubjects" class="loading-indicator">
            <div class="loading-spinner"></div>
            <p>Loading subjects...</p>
        </div>
        <div v-else-if="subjectsError" class="error-message">
            <p>Could not load subjects: {{ subjectsError }}</p>
        </div>

        <div v-else class="content-wrapper">
            <div class="subject-selector">
                <label for="subject-select">Select Subject:</label>
                <select id="subject-select" v-model="selectedSubjectId" @change="handleSubjectChange"
                    class="form-select">
                    <option disabled value="">Please select a subject</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                        {{ subject.name }}
                    </option>
                </select>
            </div>

            <div v-if="selectedSubjectId">
                <div v-if="isLoadingFlashcards" class="loading-indicator">
                    <div class="loading-spinner"></div>
                    <p>Loading ignored flashcards...</p>
                </div>
                <div v-else-if="flashcardsError" class="error-message">
                    <p>Could not load flashcards: {{ flashcardsError }}</p>
                </div>
                <div v-else-if="ignoredFlashcards.length === 0" class="info-message">
                    <p>No ignored flashcards for this subject.</p>
                </div>
                <div v-else class="ignored-flashcards-list">
                    <h2>Ignored Flashcards for {{ selectedSubjectName }}</h2>
                    <ul>
                        <li v-for="flashcard in ignoredFlashcards" :key="flashcard.id" class="flashcard-item">
                            <div class="flashcard-content">
                                <p><strong>Question:</strong> {{ flashcard.question }}</p>
                                <p><strong>Answer:</strong> {{ flashcard.answer }}</p>
                            </div>
                            <button @click="reuseFlashcard(flashcard.id)" class="btn btn-primary btn-sm">Reuse</button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import config from '../config';

const apiBaseUrl = config.apiBaseUrl;

const subjects = ref([]);
const selectedSubjectId = ref('');
const isLoadingSubjects = ref(true);
const subjectsError = ref('');

const allFlashcardsForSubject = ref([]);
const ignoredFlashcardIds = ref(new Set());
const isLoadingFlashcards = ref(false);
const flashcardsError = ref('');

const fetchSubjects = async () => {
    isLoadingSubjects.value = true;
    subjectsError.value = '';
    try {
        const response = await fetch(`${apiBaseUrl}/api/subjects-summary`);
        if (!response.ok) {
            throw new Error(`Failed to fetch subjects: ${response.statusText}`);
        }
        subjects.value = await response.json();
    } catch (error) {
        console.error('Error fetching subjects:', error);
        subjectsError.value = error.message;
    } finally {
        isLoadingSubjects.value = false;
    }
};

const loadIgnoredFlashcardIdsForSubject = () => {
    if (!selectedSubjectId.value) {
        ignoredFlashcardIds.value = new Set();
        return;
    }
    const storageKey = `ignoredFlashcards_${selectedSubjectId.value}`;
    const storedIds = localStorage.getItem(storageKey);
    if (storedIds) {
        ignoredFlashcardIds.value = new Set(JSON.parse(storedIds));
    } else {
        ignoredFlashcardIds.value = new Set();
    }
};

const fetchFlashcardsForSubject = async () => {
    if (!selectedSubjectId.value) return;
    isLoadingFlashcards.value = true;
    flashcardsError.value = '';
    allFlashcardsForSubject.value = [];
    try {
        const response = await fetch(`${apiBaseUrl}/api/subjects/${selectedSubjectId.value}/flashcards`);
        if (!response.ok) {
            throw new Error(`Failed to fetch flashcards: ${response.statusText}`);
        }
        allFlashcardsForSubject.value = await response.json();
    } catch (error) {
        console.error('Error fetching flashcards for subject:', error);
        flashcardsError.value = error.message;
    } finally {
        isLoadingFlashcards.value = false;
    }
};

const ignoredFlashcards = computed(() => {
    if (!selectedSubjectId.value || allFlashcardsForSubject.value.length === 0) {
        return [];
    }
    return allFlashcardsForSubject.value.filter(fc => ignoredFlashcardIds.value.has(fc.id));
});

const selectedSubjectName = computed(() => {
    const subject = subjects.value.find(s => s.id === selectedSubjectId.value);
    return subject ? subject.name : '';
});

const handleSubjectChange = async () => {
    if (selectedSubjectId.value) {
        loadIgnoredFlashcardIdsForSubject();
        await fetchFlashcardsForSubject();
    } else {
        allFlashcardsForSubject.value = [];
        ignoredFlashcardIds.value = new Set();
    }
};

const reuseFlashcard = (flashcardId) => {
    if (!selectedSubjectId.value) return;

    ignoredFlashcardIds.value.delete(flashcardId);
    const storageKey = `ignoredFlashcards_${selectedSubjectId.value}`;
    localStorage.setItem(storageKey, JSON.stringify(Array.from(ignoredFlashcardIds.value)));

    // Force re-computation of ignoredFlashcards by triggering a change
    // This is a bit of a hack; ideally, Vue's reactivity handles this,
    // but direct modification of the set might need a nudge if `allFlashcardsForSubject` doesn't change.
    // A more robust way would be to refilter or manage the displayed list directly.
    // For now, let's ensure the computed property re-evaluates.
    allFlashcardsForSubject.value = [...allFlashcardsForSubject.value];
    alert('Flashcard has been moved back to practice!');
};

onMounted(() => {
    fetchSubjects();
});
</script>

<style scoped>
.ignored-flashcards-page {
    padding: 2rem;
    max-width: 900px;
    margin: 0 auto;
}

.page-title {
    font-size: 2rem;
    color: var(--text-color);
    margin-bottom: 1.5rem;
    font-weight: 700;
    text-align: center;
}

.content-wrapper {
    background-color: #fff;
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
}

.subject-selector {
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.subject-selector label {
    font-weight: 600;
    color: var(--text-color-dark);
}

.form-select {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: var(--border-radius-sm);
    font-size: 1rem;
    width: 100%;
    box-sizing: border-box;
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
    width: 40px;
    height: 40px;
    border: 4px solid rgba(59, 130, 246, 0.3);
    border-radius: 50%;
    border-top-color: var(--primary-color);
    animation: spin 1s ease-in-out infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.error-message,
.info-message {
    padding: 1rem;
    border-radius: var(--border-radius-sm);
    margin: 1rem 0;
    text-align: center;
}

.error-message {
    background-color: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: #dc2626;
}

.info-message {
    background-color: rgba(59, 130, 246, 0.05);
    border: 1px solid rgba(59, 130, 246, 0.2);
    color: var(--primary-color);
}

.ignored-flashcards-list h2 {
    font-size: 1.5rem;
    color: var(--text-color-dark);
    margin-bottom: 1rem;
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5rem;
}

.ignored-flashcards-list ul {
    list-style: none;
    padding: 0;
}

.flashcard-item {
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: var(--border-radius-sm);
    padding: 1rem;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.flashcard-content p {
    margin: 0.3rem 0;
    color: var(--text-light);
}

.flashcard-content p strong {
    color: var(--text-color);
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius-sm);
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.btn-primary:hover {
    background-color: var(--primary-hover);
}

.btn-sm {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
}
</style>
