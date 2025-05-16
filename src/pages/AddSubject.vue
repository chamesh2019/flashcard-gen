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
      <button type="submit">Add Subject</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const subjectName = ref('');
const subjectDescription = ref('');

const handleSubmit = () => {
  // For now, we'll just log the data.
  // Backend logic will be added later.
  console.log('New Subject:', {
    name: subjectName.value,
    description: subjectDescription.value,
  });
  // Optionally, clear the form or navigate away
  subjectName.value = '';
  subjectDescription.value = '';
  // router.push('/'); // Example: navigate to home after adding
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
</style>
