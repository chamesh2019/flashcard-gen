<template>
    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Flashcard Practice</h1>
            <p v-if="subjectName" class="page-description">Studying: {{ subjectName }}</p>
        </div>

        <div v-if="isLoading" class="message-box info-message">
            <div class="loading-indicator">
                <span class="loading-spinner"></span>
                <p>Loading flashcards for {{ subjectName || 'subject' }}...</p>
            </div>
        </div>

        <div v-else-if="errorMessage" class="message-box error-message">
            <p>{{ errorMessage }}</p>
            <router-link to="/" class="btn btn-primary">Back to Home</router-link>
        </div>

        <div v-else-if="!currentFlashcard && !isPracticeFinished" class="message-box warning-message">
            <p>No flashcards found for {{ subjectName }}.</p>
            <router-link to="/" class="btn btn-primary">Back to Home</router-link>
        </div>

        <div v-if="currentFlashcard && !isPracticeFinished" class="flashcard-container card">
            <!-- Progress bar -->
            <div class="progress-container">
                <div class="progress-bar" :style="{ width: `${(currentIndex + 1) / flashcards.length * 100}%` }"></div>
            </div>
            <div class="flashcard" :class="{ 'flipped': showAnswer }" @click="!showAnswer && revealAnswer()">
                <div class="flashcard-inner">
                    <div class="flashcard-front">
                        <div class="card-content">
                            <p>{{ currentFlashcard.question }}</p>
                            <div v-if="!showAnswer" class="tap-hint">Tap to reveal answer</div>
                        </div>
                    </div>
                    <div class="flashcard-back">
                        <div class="card-content">
                            <div class="answer-label">ANSWER</div>
                            <p>{{ currentFlashcard.answer }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="showAnswer" class="rating-container">
                <p class="rating-prompt">How well did you know this?</p>
                <div class="rating-buttons">
                    <button @click="rateFlashcard('good')" class="rating-btn got-it-btn">
                        <span class="thumb-icon">👍</span> Got it
                    </button>
                    <button @click="rateFlashcard('bad')" class="rating-btn need-review-btn">
                        <span class="thumb-icon">👎</span> Need Review
                    </button>
                </div>
            </div>


        </div>

        <div v-if="isPracticeFinished" class="card summary-container">
            <div class="summary-header">
                <div class="completion-badge">
                    <div class="completion-icon">✓</div>
                </div>
                <h2>Practice Complete!</h2>
                <p class="completion-text">You've completed all flashcards for <strong>{{ subjectName }}</strong></p>
            </div>

            <div class="summary-stats">
                <div class="stat-item good-stats">
                    <span class="stat-value">{{ goodRatings }}</span>
                    <span class="stat-label">Got it</span>
                    <span class="stat-icon">👍</span>
                </div>
                <div class="stat-item bad-stats">
                    <span class="stat-value">{{ badRatings }}</span>
                    <span class="stat-label">Need Review</span>
                    <span class="stat-icon">👎</span>
                </div>
                <div v-if="unratedCount > 0" class="stat-item unrated-stats">
                    <span class="stat-value">{{ unratedCount }}</span>
                    <span class="stat-label">Unrated</span>
                    <span class="stat-icon">❓</span>
                </div>
            </div>

            <div class="summary-actions">
                <button @click="restartPractice" class="primary-action-btn">
                    Practice Again
                </button>
                <router-link to="/" class="secondary-action-btn">
                    Back to Home
                </router-link>
            </div>
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
        const summaryResponse = await fetch(`https://csmanager2020.pythonanywhere.com/api/subjects-summary`);
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

        const response = await fetch(`https://csmanager2020.pythonanywhere.com/api/subjects/${subjectId.value}/flashcards`);
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
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}

.flashcard-container {
    position: relative;
    padding: 0;
    padding-top: 6px;
    overflow: hidden;
}

/* Progress bar styling */
.progress-container {
    height: 6px;
    width: 100%;
    background-color: #e2e8f0;
    position: absolute;
    top: 0;
    left: 0;
    border-radius: var(--border-radius) var(--border-radius) 0 0;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background-color: var(--primary-color);
    transition: width 0.3s ease;
}

.flashcard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    margin-top: 0.5rem;
}

.card-count {
    color: var(--text-light);
    font-size: 0.9rem;
    font-weight: 500;
}

/* Flashcard styling using 3D transforms */
.flashcard {
    perspective: 1000px;
    height: 400px;
    cursor: pointer;
}

.flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    padding: 2em;
    transition: transform 0.6s;
}

.flashcard.flipped .flashcard-inner {
    transform: rotateY(180deg);
}

.flashcard-front,
.flashcard-back {
    position: absolute;
    width: calc(100% - 4em);
    height: calc(100% - 4em);
    backface-visibility: hidden;
    box-shadow: var(--box-shadow);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0;
}

.flashcard-front {
    background-color: white;
    color: var(--text-color);
}

.flashcard-back {
    background-color: #4285F4;
    /* Google blue color - matches screenshot */
    color: white;
    transform: rotateY(180deg);
    padding: 0;
}

.flashcard-front .card-content p,
.flashcard-back .card-content p {
    word-wrap: break-word;
    /* Older browsers */
    overflow-wrap: break-word;
    /* Standard property */
    white-space: pre-wrap;
    /* Preserve whitespace and wrap */
    max-height: 200px;
    /* Adjust as needed */
    overflow-y: auto;
    /* Add scroll for very long content */
}

.card-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

.answer-label {
    font-size: 0.85rem;
    letter-spacing: 1px;
    margin-bottom: 2rem;
    opacity: 0.8;
    font-weight: 500;
}

.card-content p {
    font-size: 1.75rem;
    margin: 0;
    line-height: 1.5;
    max-width: 90%;
    font-weight: 500;
}

.tap-hint {
    position: absolute;
    bottom: 1.5rem;
    left: 50%;
    /* Added for horizontal centering */
    transform: translateX(-50%);
    /* Added for horizontal centering */
    font-size: 0.9rem;
    color: #757575;
    display: flex;
    align-items: center;
    animation: pulse 2s infinite;
    gap: 0.5rem;
}

.tap-hint::before {
    content: "👆";
    font-size: 1rem;
}

@keyframes pulse {
    0% {
        opacity: 0.4;
    }

    50% {
        opacity: 0.9;
    }

    100% {
        opacity: 0.4;
    }
}

/* Controls styling */
.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 1rem;
}

.reveal-btn {
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.8rem 2rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}

.reveal-btn:hover {
    background-color: #3367D6;
    /* Darker blue on hover */
}

.rating-container {
    margin-bottom: 1.5rem;
}

.rating-prompt {
    font-size: 1rem;
    margin-top: 0;
    margin-bottom: 1rem;
    color: var(--text-light);
    text-align: center;
}

.rating-buttons {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
}

.rating-btn {
    padding: 0.8rem 2rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.rating-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.got-it-btn {
    background-color: #34A853;
    /* Google green */
    color: white;
}

.got-it-btn:hover {
    background-color: #2E9648;
}

.need-review-btn {
    background-color: #EA4335;
    /* Google red */
    color: white;
}

.need-review-btn:hover {
    background-color: #D33C2F;
}

.thumb-icon {
    margin-right: 0.5rem;
    font-size: 1.1rem;
}

/* Summary container styling */
.summary-container {
    text-align: center;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.summary-container h2 {
    margin-bottom: 0.5rem;
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 600;
}

.completion-text {
    color: var(--text-light);
    font-size: 1.1rem;
    margin-bottom: 0;
}

.summary-header {
    margin-bottom: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.completion-badge {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80px;
    height: 80px;
    background-color: #4285F4;
    border-radius: 50%;
    margin-bottom: 1.5rem;
}

.completion-icon {
    color: white;
    font-size: 3rem;
}

.summary-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    width: 100%;
    max-width: 500px;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem;
    border-radius: 12px;
    min-width: 120px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.good-stats {
    background-color: #E8F5E9;
    /* Light green */
    color: #34A853;
    /* Google green */
    border: 1px solid rgba(52, 168, 83, 0.2);
}

.bad-stats {
    background-color: #FDECEA;
    /* Light red */
    color: #EA4335;
    /* Google red */
    border: 1px solid rgba(234, 67, 53, 0.2);
}

.unrated-stats {
    background-color: #FFF3E0;
    /* Light orange */
    color: #FBBC04;
    /* Google yellow */
    border: 1px solid rgba(251, 188, 4, 0.2);
}

.stat-icon {
    font-size: 1.8rem;
    margin-top: 0.5rem;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.25rem;
}

.stat-label {
    font-size: 0.95rem;
    opacity: 0.8;
    font-weight: 500;
}

.summary-actions {
    margin-top: 3rem;
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.primary-action-btn,
.secondary-action-btn {
    padding: 0.8rem 2rem;
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

.primary-action-btn {
    background-color: #4285F4;
    /* Google blue */
    color: white;
    border: none;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3);
}

.primary-action-btn:hover {
    background-color: #3367D6;
    /* Darker blue */
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4);
}

.secondary-action-btn {
    background-color: white;
    color: #4285F4;
    border: 1px solid #4285F4;
}

.secondary-action-btn:hover {
    background-color: rgba(66, 133, 244, 0.05);
}

/* Responsive design */
@media (max-width: 640px) {
    .flashcard {
        height: 280px;
    }

    .card-content p {
        font-size: 1.25rem;
    }

    .summary-stats {
        gap: 1rem;
        flex-direction: column;
    }

    .stat-item {
        width: 100%;
        max-width: 280px;
    }

    .rating-buttons {
        flex-direction: column;
        gap: 1rem;
        width: 100%;
        max-width: 280px;
        margin: 0 auto;
    }

    .rating-btn {
        width: 100%;
    }

    .controls {
        margin-top: 1.5rem;
    }
}

.stat-item {
    padding: 0.75rem 1rem;
    min-width: 80px;
}
</style>
```
