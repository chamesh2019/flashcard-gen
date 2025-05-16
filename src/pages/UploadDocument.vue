<template>
  <div class="upload-document-container">
    <h2>Upload Document</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="document">Upload Document:</label>
        <input type="file" id="document" @change="handleFileUpload" accept=".pdf,.doc,.docx,.txt" />
      </div>
      <div class="form-group">
        <label for="subject">Select Subject:</label>
        <select id="subject" v-model="selectedSubject">
          <option disabled value="">Please select one</option>
          <!-- Add subject options here -->
          <option>Mathematics</option>
          <option>Science</option>
          <option>History</option>
        </select>
      </div>
      <button type="submit">Upload</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'UploadDocument',
  data() {
    return {
      selectedFile: null,
      selectedSubject: '',
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    handleSubmit() {
      if (!this.selectedFile) {
        alert('Please select a file to upload.');
        return;
      }
      if (!this.selectedSubject) {
        alert('Please select a subject.');
        return;
      }
      // Placeholder for upload logic
      console.log('Uploading file:', this.selectedFile.name, 'for subject:', this.selectedSubject);
      alert(`File "${this.selectedFile.name}" ready for upload for subject "${this.selectedSubject}". Backend logic not implemented yet.`);
      // Reset form
      this.selectedFile = null;
      this.selectedSubject = '';
      document.getElementById('document').value = '';
    },
  },
};
</script>

<style scoped>
.upload-document-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input[type="file"],
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #45a049;
}
</style>
