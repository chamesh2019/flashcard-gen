<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item brand-text">FlashcardGen</router-link>
    </div>
    <div class="navbar-menu">
      <router-link to="/" class="navbar-item">Home</router-link>
      <router-link to="/add-subject" class="navbar-item">Add Subject</router-link>
      <router-link to="/upload-document" class="navbar-item">Upload Document</router-link>
      <!-- Add other navigation links here as your app grows -->
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  background-color: #34495e; /* Dark blue-grey */
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand .navbar-item {
  color: #ecf0f1; /* Light grey */
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.navbar-brand .navbar-item:hover {
  color: #bdc3c7; /* Lighter grey on hover */
}

.navbar-menu {
  display: flex;
  align-items: center;
}

.navbar-menu .navbar-item {
  color: #ecf0f1; /* Light grey */
  text-decoration: none;
  padding: 0.5rem 1rem;
  margin-left: 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.navbar-menu .navbar-item:hover,
.navbar-menu .navbar-item.router-link-exact-active {
  background-color: #2c3e50; /* Slightly darker blue-grey */
  color: #ffffff; /* White */
}

/* Responsive adjustments if needed */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
  }
  .navbar-menu {
    margin-top: 1rem;
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }
  .navbar-menu .navbar-item {
    margin-left: 0;
    margin-bottom: 0.5rem;
    width: 100%;
    text-align: left;
  }
}
</style>
