<script setup>
import Navbar from './components/Navbar.vue'; // Import the Navbar component
</script>

<template>
  <div id="app">
    <Navbar /> <!-- Add the Navbar component here -->
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
body {
  font-family: 'Arial', sans-serif;
  background-color: #f5f7fa;
  margin: 0;
  padding: 0;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex; /* Use flexbox to position navbar and content */
  flex-direction: column; /* Stack navbar and content vertically */
}

.content {
  flex-grow: 1; /* Allow content to take up remaining space */
  padding: 1rem; /* Add some padding around the page content */
  /* You might want to add more specific padding/margins based on navbar height */
}
</style>
