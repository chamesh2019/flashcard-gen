<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Upload Document</h1>
      <p class="page-description">Upload a Markdown document to generate flashcards</p>
    </div>

    <div class="card form-container">
      <div v-if="isLoading" class="message-box info-message">
        <div class="loading-indicator">
          <span class="loading-spinner"></span>
          <p>Loading subjects...</p>
        </div>
      </div>

      <div v-else-if="error" class="message-box error-message">
        <p>{{ error }}</p>
        <button @click="fetchSubjects" class="btn btn-primary">Try Again</button>
      </div>
      <form v-else @submit.prevent="handleSubmit" class="upload-form">
        <div class="form-group">
          <label for="document" class="form-label">Upload Markdown Document:</label>
          <div class="file-upload-container">
            <input type="file" id="document" class="file-input" @change="handleFileUpload" accept=".md,.markdown"
              :disabled="uploading" />
            <label for="document" class="file-upload-label">
              <span class="file-upload-icon">📄</span>
              <span class="file-upload-text">{{ selectedFile ? selectedFile.name : 'Choose a file...' }}</span>
              <span class="file-upload-button">Browse</span>
            </label>
          </div>
          <div v-if="selectedFile" class="selected-file">
            <div class="file-info">
              <span class="file-icon">📄</span>
              <span class="file-details">
                <span class="file-name">{{ selectedFile.name }}</span>
                <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
              </span>
            </div>
            <button type="button" class="file-remove-btn" @click="clearFile">✕</button>
          </div>
        </div>

        <div class="form-group">
          <label for="subject">Select Subject:</label>
          <select id="subject" v-model="selectedSubjectId" required :disabled="uploading || subjects.length === 0">
            <option disabled value="">Please select one</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
          <div v-if="subjects.length === 0" class="message-box warning-message">
            No subjects available. Please <router-link to="/add-subject">add a subject</router-link> first.
          </div>
        </div>

        <button type="submit" class="btn btn-primary submit-button"
          :disabled="uploading || !selectedFile || !selectedSubjectId || subjects.length === 0">
          <span class="icon">{{ uploading ? '⏳' : '📤' }}</span>
          {{ uploading ? 'Uploading...' : 'Upload Document' }}
        </button>

        <div v-if="uploadSuccess" class="message-box success-message">
          <p>{{ uploadSuccess }}</p>
        </div>

        <div v-if="uploadError" class="message-box error-message">
          <p>{{ uploadError }}</p>
        </div>
      </form>
    </div>
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

const clearFile = () => {
  selectedFile.value = null;
  // Reset the input element
  const fileInput = document.getElementById('document');
  if (fileInput) fileInput.value = '';
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
    const response = await fetch('https://csmanager2020.pythonanywhere.com/api/subjects');
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
    const response = await fetch('https://csmanager2020.pythonanywhere.com/api/document', {
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
.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2.5rem;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 0.5rem;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  display: inline-block;
  width: 1.5rem;
  height: 1.5rem;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-right: 0.75rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Form styling */
.form-label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 500;
  color: var(--text-color);
}

/* Custom file upload styling */
.file-upload-container {
  position: relative;
  margin-bottom: 0.75rem;
}

.file-input {
  position: absolute;
  left: -9999px;
  opacity: 0;
  width: 1px;
  height: 1px;
}

.file-upload-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background-color: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: var(--transition);
  width: 100%;
}

.file-upload-label:hover {
  background-color: #f1f5f9;
  border-color: var(--primary-color);
}

.file-upload-icon {
  font-size: 1.5rem;
  margin-right: 0.75rem;
  color: var(--text-light);
}

.file-upload-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-light);
}

.file-upload-button {
  background-color: var(--primary-color);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

.selected-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: rgba(59, 130, 246, 0.05);
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  margin-top: 0.5rem;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.file-info {
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 0;
  /* For text truncation to work */
}

.file-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
  /* For text truncation to work */
}

.file-name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 0.8rem;
  color: var(--text-light);
}

.file-remove-btn {
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 24px;
  height: 24px;
}

.file-remove-btn:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.file-icon {
  margin-right: 0.5rem;
}

.file-name {
  font-weight: 500;
  margin-right: 0.5rem;
}

.file-size {
  color: var(--text-light);
  font-size: 0.875rem;
}

/* Select input styling */
select {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: var(--border-radius);
  background-color: white;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.2em;
  cursor: pointer;
  transition: all 0.2s ease;
}

select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

select:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: #f8fafc;
}

.submit-button {
  width: 100%;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.submit-button {
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
