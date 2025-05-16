<template>
  <div class="add-subject-page">
    <h1>Add New Subject</h1>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="subjectName">Subject Name:</label>
        <input type="text" id="subjectName" v-model="subjectName" required />
      </div>
      <div>
        <label for="subjectDescription">Description (Optional):</label>
        <textarea id="subjectDescription" v-model="subjectDescription"></textarea>
      </div>
      <button type="submit" :disabled="isLoading">{{ isLoading ? 'Adding...' : 'Add Subject' }}</button>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

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
    const response = await fetch('http://127.0.0.1:5000/api/subjects', {
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
      subjectName.value = '';
      subjectDescription.value = '';
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
.add-subject-page {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

form div {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1rem;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

button[type="submit"] {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

button[type="submit"]:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.success-message {
  color: green;
  margin-top: 1rem;
  text-align: center;
}

.error-message {
  color: red;
  margin-top: 1rem;
  text-align: center;
}
</style>
