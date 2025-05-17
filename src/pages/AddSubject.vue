<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Add New Subject</h1>
      <p class="page-description">Create a new subject for organizing your flashcards</p>
    </div>

    <div class="card form-container">
      <form @submit.prevent="handleSubmit" class="subject-form">
        <div class="form-group">
          <label for="subjectName">Subject Name:</label>
          <input type="text" id="subjectName" v-model="subjectName" required placeholder="Enter subject name"
            class="form-input" />
        </div>
        <div class="form-group">
          <label for="subjectDescription">Description (Optional):</label>
          <textarea id="subjectDescription" v-model="subjectDescription" placeholder="Enter subject description"
            class="form-textarea"></textarea>
        </div>
        <button type="submit" class="btn btn-primary submit-button" :disabled="isLoading">
          <span class="icon">{{ isLoading ? '⏳' : '📝' }}</span>
          {{ isLoading ? 'Adding...' : 'Add Subject' }}
        </button>

        <div v-if="successMessage" class="message-box success-message">
          <p>{{ successMessage }}</p>
        </div>

        <div v-if="errorMessage" class="message-box error-message">
          <p>{{ errorMessage }}</p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import config from '../config';

const apiBaseUrl = config.apiBaseUrl;
const subjectName = ref('');
const subjectDescription = ref('');
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const router = useRouter();

const handleSubmit = async () => {
  isLoading.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  try {
    const response = await fetch(`${apiBaseUrl}/api/subjects`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: subjectName.value,
        description: subjectDescription.value,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      successMessage.value = `Subject "${data.name}" added successfully!`;
      // Reset the form
      subjectName.value = '';
      subjectDescription.value = '';
      // Clear the success message after 3 seconds
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } else {
      errorMessage.value = data.error || 'Failed to add subject. Please try again.';
    }
  } catch (error) {
    console.error('Error adding subject:', error);
    errorMessage.value = 'An unexpected error occurred. Please check the console and try again.';
  }
  isLoading.value = false;
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  box-sizing: border-box;
}

.subject-form {
  width: 100%;
  box-sizing: border-box;
}

.form-input,
.form-textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-radius: var(--border-radius);
  background-color: white;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: var(--text-color);
  transition: var(--transition);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.submit-button {
  width: 100%;
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  box-sizing: border-box;
}

.submit-button:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.submit-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.message-box {
  text-align: center;
  padding: 1rem;
  border-radius: var(--border-radius);
  margin: 1rem 0;
}

.success-message {
  background-color: #e8f5e9;
  border: 1px solid var(--success-color);
  color: #2e7d32;
}

.error-message {
  background-color: #ffebee;
  border: 1px solid var(--danger-color);
  color: #c62828;
}
</style>
