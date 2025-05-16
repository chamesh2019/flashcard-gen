<template>
  <div class="upload-document-container">
    <h2>Upload Document</h2>

    <div v-if="isLoading" class="loading-message">
      <p>Loading subjects...</p>
    </div>

    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="fetchSubjects">Try Again</button>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="upload-form">
      <div class="form-group">
        <label for="document">Upload Document:</label>
        <input type="file" id="document" @change="handleFileUpload" accept=".pdf,.doc,.docx,.txt"
          :disabled="uploading" />
        <p class="file-info" v-if="selectedFile">
          Selected: {{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})
        </p>
      </div>

      <div class="form-group">
        <label for="subject">Select Subject:</label>
        <select id="subject" v-model="selectedSubjectId" required :disabled="uploading || subjects.length === 0">
          <option disabled value="">Please select one</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </select>
        <div v-if="subjects.length === 0" class="warning-message">
          No subjects available. Please <router-link to="/add-subject">add a subject</router-link> first.
        </div>
      </div>

      <button type="submit" :disabled="uploading || !selectedFile || !selectedSubjectId || subjects.length === 0">
        {{ uploading ? 'Uploading...' : 'Upload' }}
      </button>

      <div v-if="uploadSuccess" class="success-message">
        <p>{{ uploadSuccess }}</p>
      </div>

      <div v-if="uploadError" class="error-message">
        <p>{{ uploadError }}</p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const selectedFile = ref(null);
const selectedSubjectId = ref('');
const subjects = ref([]);
const isLoading = ref(true);
const error = ref('');
const uploading = ref(false);
const uploadSuccess = ref('');
const uploadError = ref('');

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0];
  // Clear previous messages when a new file is selected
  uploadSuccess.value = '';
  uploadError.value = '';
};

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' bytes';
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  else return (bytes / 1048576).toFixed(1) + ' MB';
};

const fetchSubjects = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const response = await fetch('http://127.0.0.1:5000/api/subjects');
    if (!response.ok) {
      throw new Error(`Failed to fetch subjects: ${response.statusText}`);
    }
    subjects.value = await response.json();
  } catch (err) {
    console.error('Error fetching subjects:', err);
    error.value = err.message || 'Failed to load subjects. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

const handleSubmit = async () => {
  if (!selectedFile.value) {
    uploadError.value = 'Please select a file to upload.';
    return;
  }

  if (!selectedSubjectId.value) {
    uploadError.value = 'Please select a subject.';
    return;
  }

  uploading.value = true;
  uploadSuccess.value = '';
  uploadError.value = '';

  const formData = new FormData();
  formData.append('file', selectedFile.value);
  formData.append('subject_id', selectedSubjectId.value);

  try {
    const response = await fetch('http://127.0.0.1:5000/api/document', {
      method: 'POST',
      body: formData,
      // Don't set Content-Type header for FormData
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Upload failed');
    }

    // Upload successful
    uploadSuccess.value = `File "${selectedFile.value.name}" uploaded successfully!`;

    // Reset form
    selectedFile.value = null;
    selectedSubjectId.value = '';
    document.getElementById('document').value = '';
  } catch (err) {
    console.error('Upload error:', err);
    uploadError.value = err.message || 'An error occurred during upload. Please try again.';
  } finally {
    uploading.value = false;
  }
};

onMounted(() => {
  fetchSubjects();
});
</script>

<style scoped>
.upload-document-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.form-group input[type="file"],
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  box-sizing: border-box;
}

.form-group select {
  height: 2.5rem;
}

.form-group input[type="file"]:disabled,
.form-group select:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

.file-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.loading-message,
.error-message,
.success-message,
.warning-message {
  text-align: center;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.loading-message {
  background-color: #e3f2fd;
  color: #0d47a1;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
}

.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.warning-message {
  background-color: #fff8e1;
  color: #f57f17;
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.warning-message a {
  color: #0288d1;
  text-decoration: none;
  font-weight: bold;
}

.warning-message a:hover {
  text-decoration: underline;
}
</style>
