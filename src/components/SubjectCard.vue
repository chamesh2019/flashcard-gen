<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  id: { // Added id prop
    type: [String, Number],
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  cardCount: {
    type: Number,
    required: true
  }
});

const router = useRouter();

const navigateToPractice = () => {
  if (props.id) {
    router.push(`/flashcards/${props.id}`);
  }
};
</script>

<template>
  <div class="subject-card card" @click="navigateToPractice">
    <h2 class="title">{{ title }}</h2>
    <p class="description">{{ description }}</p>
    <div class="card-footer">
      <div class="card-count">
        <span class="card-badge">{{ cardCount }} flashcards</span>
      </div>
      <div class="card-action">
        <span class="study-btn">Study Now →</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.subject-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.title {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
}

.description {
  flex-grow: 1;
  color: #666;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.card-count {
  font-size: 0.9rem;
  color: #42b883;
  font-weight: 600;
  border-top: 1px solid #eee;
  padding-top: 0.8rem;
}
</style>
