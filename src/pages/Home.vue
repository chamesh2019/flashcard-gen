<script setup>
import SubjectCard from '../components/SubjectCard.vue';
import { ref, onMounted } from 'vue';

const subjectsWithFlashcards = ref([]);
const isLoading = ref(true);
const errorMessage = ref('');

const fetchSubjectsSummary = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const response = await fetch('https://csmanager2020.pythonanywhere.com/api/subjects-summary');
    if (!response.ok) {
      throw new Error(`Failed to fetch subjects summary: ${response.statusText} (${response.status})`);
    }
    const data = await response.json();
    // The new endpoint already provides 'cardCount' and subject details including 'name' and 'description'
    // We just need to ensure the 'title' prop for SubjectCard is mapped if it expects 'title' specifically.
    subjectsWithFlashcards.value = data.map(subject => ({
      ...subject,
      title: subject.name // Assuming SubjectCard expects a 'title' prop
    }));
  } catch (error) {
    console.error('Error fetching subjects summary:', error);
    errorMessage.value = error.message || 'Could not load subjects. Please try again later.';
  }
  isLoading.value = false;
};

onMounted(() => {
  fetchSubjectsSummary();
});

</script>

<template>
  <div class="container">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Flashcard Generator</h1>
        <p class="page-description">Select a subject to view and practice with your flashcards, or add a new subject to
          get started.</p>
      </div>
      <div class="header-actions">
        <router-link to="/add-subject" class="btn btn-primary">
          <span class="icon">✚</span> Add New Subject
        </router-link>
      </div>
    </div>

    <div v-if="isLoading" class="message-box info-message">
      <div class="loading-indicator">
        <span class="loading-spinner"></span>
        <p>Loading subjects...</p>
      </div>
    </div>

    <div v-else-if="errorMessage" class="message-box error-message">
      <p>{{ errorMessage }}</p>
      <button @click="fetchSubjectsSummary" class="btn btn-primary">Try Again</button>
    </div>

    <div v-else-if="subjectsWithFlashcards.length === 0" class="message-box warning-message">
      <div class="empty-state">
        <div class="empty-icon">📚</div>
        <h3>No Subjects Found</h3>
        <p>You don't have any subjects yet. Create your first subject to get started!</p>
        <router-link to="/add-subject" class="btn btn-primary">
          <span class="icon">✚</span> Add New Subject
        </router-link>
      </div>
    </div>

    <div v-else class="subjects-grid">
      <div v-for="subject in subjectsWithFlashcards" :key="subject.id" class="subject-item">
        <SubjectCard :id="subject.id" :title="subject.title" :description="subject.description"
          :cardCount="subject.cardCount" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-content {
  max-width: 70%;
}

.header-actions {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 2.2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.page-description {
  font-size: 1.1rem;
  color: var(--text-light);
  line-height: 1.6;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  row-gap: 2.5rem;
  margin-bottom: 3rem;
}

.subject-item {
  min-height: 220px;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.empty-state h3 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.empty-state p {
  margin-bottom: 2rem;
  color: var(--text-light);
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

/* Loading spinner */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
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

/* Message boxes */
.message-box {
  padding: 2rem;
  border-radius: var(--border-radius);
  text-align: center;
  margin: 1.5rem 0;
}

.info-message {
  background-color: rgba(59, 130, 246, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.error-message {
  background-color: rgba(239, 68, 68, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #dc2626;
}

.warning-message {
  background-color: rgba(245, 158, 11, 0.05);
  border: 1px solid rgba(245, 158, 11, 0.2);
}

/* Responsive design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-content {
    max-width: 100%;
    margin-bottom: 1rem;
  }

  .subjects-grid {
    grid-template-columns: 1fr;
  }
}

.add-subject-button {
  background-color: #4CAF50;
  /* Green */
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin-top: 1rem;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.add-subject-button:hover {
  background-color: #45a049;
}

.loading-message,
.error-message,
.no-subjects-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #555;
}

.error-message button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .subjects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
