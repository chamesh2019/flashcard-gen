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
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f0f0f0;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

.title {
  color: var(--text-color);
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  font-weight: 600;
}

.description {
  flex-grow: 1;
  color: var(--text-light);
  font-size: 1rem;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 1rem;
  margin-top: auto;
}

.card-count {
  font-size: 0.9rem;
  font-weight: 500;
}

.card-badge {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
}

.card-action {
  text-align: right;
}

.study-btn {
  color: var(--primary-color);
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.subject-card:hover .study-btn {
  color: var(--primary-hover);
}
</style>
