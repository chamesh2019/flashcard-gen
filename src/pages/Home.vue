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
    const response = await fetch('http://127.0.0.1:5000/api/subjects-summary');
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
      <h1 class="page-title">Flashcard Generator</h1>
      <p class="page-description">Select a subject to view and practice with your flashcards, or add a new subject to
        get started.</p>
      <router-link to="/add-subject" class="btn btn-primary">
        <span class="icon">✚</span> Add New Subject
      </router-link>
    </div>

    <div v-if="isLoading" class="loading-message">
      <p>Loading subjects...</p>
    </div>
    <div v-else-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
      <button @click="fetchSubjectsSummary">Try Again</button>
    </div>
    <div v-else-if="subjectsWithFlashcards.length === 0" class="no-subjects-message">
      <p>No subjects found. Why not add one?</p>
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
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.header p {
  font-size: 1.2rem;
  color: #666;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  row-gap: 3rem;
  margin-bottom: 2rem;
}

.subject-item {
  min-height: 200px;
  margin-bottom: 1rem;
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
