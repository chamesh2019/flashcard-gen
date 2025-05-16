<script setup>
import SubjectCard from '../components/SubjectCard.vue';
import { ref } from 'vue';

// Hardcoded subjects data
const subjects = ref([
  {
    id: 1,
    title: 'Mathematics',
    description: 'Algebra, calculus, geometry, and other mathematical concepts for students of all levels.',
    cardCount: 45
  },
  {
    id: 2,
    title: 'Computer Science',
    description: 'Programming concepts, algorithms, data structures, and computer architecture.',
    cardCount: 32
  },
  {
    id: 3,
    title: 'Biology',
    description: 'Cell biology, genetics, ecology, and human anatomy for biology students.',
    cardCount: 28
  },
  {
    id: 4,
    title: 'History',
    description: 'World history, important events, historical figures and civilizations.',
    cardCount: 37
  },
  {
    id: 5,
    title: 'Chemistry',
    description: 'Organic chemistry, periodic table, chemical reactions and laboratory techniques.',
    cardCount: 24
  },
  {
    id: 6,
    title: 'Languages',
    description: 'Vocabulary, grammar, and common phrases for various languages.',
    cardCount: 56
  }
]);
</script>

<template>
  <div class="home-container">
    <div class="header">
      <h1>Flashcard Generator</h1>
      <p>Select a subject to view or create flashcards</p>
    </div>
    
    <div class="subjects-grid">
      <div v-for="subject in subjects" :key="subject.id" class="subject-item">
        <SubjectCard 
          :title="subject.title" 
          :description="subject.description" 
          :cardCount="subject.cardCount" 
        />
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

@media (max-width: 768px) {
  .subjects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
