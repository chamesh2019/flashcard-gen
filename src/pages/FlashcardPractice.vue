<template>
    <div class="flashcard-practice-page">
        <div v-if="isLoading" class="loading-message">
            <p>Loading flashcards for {{ subjectName || 'subject' }}...</p>
        </div>
        <div v-else-if="errorMessage" class="error-message">
            <p>{{ errorMessage }}</p>
            <router-link to="/"><button>Back to Home</button></router-link>
        </div>
        <div v-else-if="!currentFlashcard && !isPracticeFinished" class="no-flashcards-message">
            <p>No flashcards found for {{ subjectName }}.</p>
            <router-link to="/"><button>Back to Home</button></router-link>
        </div>

        <div v-if="currentFlashcard && !isPracticeFinished" class="flashcard-container">
            <h2>Practicing: {{ subjectName }} ({{ currentIndex + 1 }} / {{ flashcards.length }})</h2>
            <div class="flashcard">
                <div class="question">
                    <p>{{ currentFlashcard.question }}</p>
                </div>
                <div v-if="showAnswer" class="answer">
                    <p>{{ currentFlashcard.answer }}</p>
                </div>
            </div>

            <div class="controls">
                <button v-if="!showAnswer" @click="revealAnswer">Show Answer</button>
                <div v-if="showAnswer" class="rating-buttons">
                    <button @click="rateFlashcard('good')">👍 Good</button>
                    <button @click="rateFlashcard('bad')">👎 Bad</button>
                </div>
            </div>
        </div>

        <div v-if="isPracticeFinished" class="summary-container">
            <h2>Practice Summary for {{ subjectName }}</h2>
            <p>You have completed all flashcards for this subject.</p>
            <p><strong>{{ goodRatings }}</strong> rated 👍 (Good)</p>
            <p><strong>{{ badRatings }}</strong> rated 👎 (Bad)</p>
            <p><strong>{{ unratedCount }}</strong> unrated (if any, due to refresh or leaving early)</p>
            <button @click="restartPractice">Practice Again</button>
            <router-link to="/"><button>Back to Home</button></router-link>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const subjectId = ref(null);
const subjectName = ref('');
const flashcards = ref([]);
const currentIndex = ref(0);
const showAnswer = ref(false);
const ratings = ref({}); // { flashcardId: 'good' | 'bad' }

const isLoading = ref(true);
const errorMessage = ref('');
const isPracticeFinished = ref(false);

const currentFlashcard = computed(() => {
    if (flashcards.value.length > 0 && currentIndex.value < flashcards.value.length) {
        return flashcards.value[currentIndex.value];
    }
    return null;
});

const loadRatings = () => {
    const storedRatings = localStorage.getItem(`flashcardRatings_${subjectId.value}`);
    if (storedRatings) {
        ratings.value = JSON.parse(storedRatings);
    }
};

const saveRatings = () => {
    localStorage.setItem(`flashcardRatings_${subjectId.value}`, JSON.stringify(ratings.value));
};

const fetchSubjectDetails = async () => {
    // Attempt to get subject name from subjects-summary first for efficiency
    try {
        const summaryResponse = await fetch(`http://127.0.0.1:5000/api/subjects-summary`);
        if (!summaryResponse.ok) throw new Error('Failed to fetch subjects summary');
        const summaryData = await summaryResponse.json();
        const foundSubject = summaryData.find(s => s.id === subjectId.value);
        if (foundSubject) {
            subjectName.value = foundSubject.name;
            return;
        }
    } catch (e) {
        console.warn("Couldn't fetch subject name from summary, trying individual subject endpoint:", e);
    }
    // Fallback or if not found in summary (should ideally not happen if summary is up-to-date)
    try {
        // This endpoint doesn't exist yet, we might need to create it or adjust
        // For now, we'll assume subject name might be part of flashcard data or we skip detailed name fetching
        // Or, we can create a GET /api/subjects/<id> endpoint
        // For simplicity, if not found in summary, we might just use "Subject ID: X"
        // Let's assume for now we will get it from the flashcards endpoint or another source if needed.
        // For now, if not in summary, we won't have a specific name beyond ID.
        // A dedicated /api/subjects/:id endpoint would be better.
        subjectName.value = `Subject ${subjectId.value}`; // Placeholder if not found in summary
    } catch (error) {
        console.error('Error fetching subject details:', error);
        // errorMessage.value = 'Could not load subject details.'; // Avoid overwriting flashcard load errors
    }
};

const fetchFlashcards = async () => {
    isLoading.value = true;
    errorMessage.value = '';
    isPracticeFinished.value = false;
    try {
        await fetchSubjectDetails(); // Get subject name

        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${subjectId.value}/flashcards`);
        if (!response.ok) {
            throw new Error(`Failed to fetch flashcards: ${response.statusText} (${response.status})`);
        }
        const data = await response.json();
        flashcards.value = data;
        currentIndex.value = 0;
        showAnswer.value = false;
        if (data.length === 0) {
            // No flashcards, practice can be considered finished or show a specific message
            // isPracticeFinished.value = true; // Or handle with a specific no-flashcards message
        }
    } catch (error) {
        console.error('Error fetching flashcards:', error);
        errorMessage.value = error.message || 'Could not load flashcards for this subject.';
    }
    isLoading.value = false;
};

const revealAnswer = () => {
    showAnswer.value = true;
};

const rateFlashcard = (rating) => {
    if (currentFlashcard.value) {
        ratings.value[currentFlashcard.value.id] = rating;
        saveRatings();
        nextFlashcard();
    }
};

const nextFlashcard = () => {
    if (currentIndex.value < flashcards.value.length - 1) {
        currentIndex.value++;
        showAnswer.value = false;
    } else {
        isPracticeFinished.value = true;
        // All flashcards reviewed
    }
};

const goodRatings = computed(() => Object.values(ratings.value).filter(r => r === 'good').length);
const badRatings = computed(() => Object.values(ratings.value).filter(r => r === 'bad').length);
const unratedCount = computed(() => {
    const ratedIds = Object.keys(ratings.value);
    return flashcards.value.filter(fc => !ratedIds.includes(fc.id.toString())).length;
});

const restartPractice = () => {
    ratings.value = {}; // Clear ratings for this subject for a fresh start
    saveRatings();      // Persist cleared ratings
    currentIndex.value = 0;
    showAnswer.value = false;
    isPracticeFinished.value = false;
    // Optionally re-fetch if data could have changed, but for now just reset state
    if (flashcards.value.length === 0 && !errorMessage.value) { // If there were no flashcards to begin with
        fetchFlashcards(); // Try fetching again
    }
};


onMounted(() => {
    subjectId.value = route.params.subjectId;
    if (subjectId.value) {
        loadRatings();
        fetchFlashcards();
    } else {
        errorMessage.value = "No subject ID provided.";
        isLoading.value = false;
    }
});

// Watch for route changes if the user navigates between different subject practices directly
watch(() => route.params.subjectId, (newId) => {
    if (newId && newId !== subjectId.value) {
        subjectId.value = newId;
        ratings.value = {}; // Reset ratings for the new subject
        loadRatings();
        fetchFlashcards();
    }
});

</script>

<style scoped>
.flashcard-practice-page {
    max-width: 700px;
    margin: 2rem auto;
    padding: 1rem;
    font-family: sans-serif;
}

.loading-message,
.error-message,
.no-flashcards-message,
.summary-container {
    text-align: center;
    padding: 2rem;
}

.error-message button,
.no-flashcards-message button,
.summary-container button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    margin-left: 0.5rem;
    /* For spacing if multiple buttons */
}

.summary-container button:first-of-type {
    margin-left: 0;
}

.flashcard-container h2 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
}

.flashcard {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 2rem;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
}

.flashcard .question p,
.flashcard .answer p {
    font-size: 1.5rem;
    margin: 0;
}

.flashcard .answer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px dashed #eee;
    width: 100%;
}

.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1rem;
}

.controls button {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    background-color: #28a745;
    color: white;
    transition: background-color 0.2s ease;
}

.controls button:hover {
    background-color: #218838;
}

.rating-buttons button {
    margin: 0 0.5rem;
}

.rating-buttons button:first-child {
    background-color: #007bff;
    /* Blue for Good */
}

.rating-buttons button:first-child:hover {
    background-color: #0056b3;
}

.rating-buttons button:last-child {
    background-color: #dc3545;
    /* Red for Bad */
}

.rating-buttons button:last-child:hover {
    background-color: #c82333;
}

.summary-container h2 {
    margin-bottom: 1rem;
}

.summary-container p {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}
</style>
