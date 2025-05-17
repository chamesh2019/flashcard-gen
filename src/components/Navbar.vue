<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link :to="{ path: '/', query: route.query }" class="navbar-item brand-text">
          <span class="logo-icon">📚</span>
          FlashcardGen
        </router-link>
      </div>
      <button 
        class="navbar-toggle" 
        @click="toggleMobileMenu" 
        :class="{ 'is-active': isMobileMenuOpen }"
        aria-label="menu" 
        :aria-expanded="isMobileMenuOpen.toString()">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <div class="navbar-menu" :class="{ 'is-active': isMobileMenuOpen }">
        <router-link :to="{ path: '/', query: route.query }" class="navbar-item">
          <span class="icon">🏠</span> Home
        </router-link>
        <router-link v-if="isAdmin" :to="{ path: '/add-subject', query: route.query }" class="navbar-item">
          <span class="icon">➕</span> Add Subject
        </router-link>
        <router-link v-if="isAdmin" :to="{ path: '/upload-document', query: route.query }" class="navbar-item">
          <span class="icon">📄</span> Upload Document
        </router-link>
        <router-link v-if="isAdmin" :to="{ path: '/document-info', query: route.query }" class="navbar-item">
          <span class="icon">📋</span> Document Info
        </router-link>
        <!-- Add other navigation links here as your app grows -->
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isAdmin = computed(() => route.query.admin !== undefined);
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  padding: 1rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand .navbar-item {
  color: var(--primary-color);
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.logo-icon {
  margin-right: 0.5rem;
  font-size: 1.8rem;
}

.navbar-brand .navbar-item:hover {
  color: var(--primary-hover);
}

.navbar-menu {
  display: flex;
  align-items: center;
}

/* Add base style for navbar-toggle, hidden on desktop */
.navbar-toggle {
  display: none;
  cursor: pointer;
  background: transparent;
  border: none;
  padding: 0.5rem;
  margin-left: auto; /* Push to the right if needed */
}

.navbar-toggle span {
  display: block;
  width: 25px;
  height: 3px;
  background-color: var(--text-color, #333); /* Use a theme variable or a default */
  margin: 5px 0;
  transition: all 0.3s ease-in-out;
  border-radius: 1px;
}

.navbar-toggle.is-active span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.navbar-toggle.is-active span:nth-child(2) {
  opacity: 0;
}
.navbar-toggle.is-active span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

@media (max-width: 768px) {
  .navbar {
    /* Adjust overall navbar padding for mobile if needed, e.g., padding: 0.75rem 1rem; */
    /* The container will handle internal spacing */
  }
  .container {
    flex-direction: row; /* Keep brand and toggle on one line */
    justify-content: space-between; /* Space out brand and toggle */
    align-items: center; /* Vertically align brand and toggle */
    flex-wrap: wrap; /* Allow menu to wrap below */
    padding: 0 1rem; /* Mobile padding for the container */
    width: 100%; /* Ensure container uses full width of navbar */
  }

  .navbar-brand {
    margin-bottom: 0; /* Remove bottom margin from previous mobile style */
    flex-shrink: 0; /* Prevent brand from shrinking too much */
  }

  .navbar-toggle {
    display: block; /* Show hamburger on mobile */
  }

  .navbar-menu {
    display: none; /* Hide menu by default on mobile */
    width: 100%; /* Menu takes full width */
    flex-basis: 100%; /* Ensure it takes a new line in flex-wrap scenario */
    flex-direction: column; /* Stack items vertically */
    align-items: flex-start; /* Align items to the left */
    margin-top: 1rem; /* Space below the brand/toggle row */
    /* Remove previous mobile styles like justify-content: space-around and flex-wrap: wrap */
  }

  .navbar-menu.is-active {
    display: flex; /* Show menu when active */
  }

  .navbar-menu .navbar-item {
    width: 100%; /* Make items full width */
    margin: 0 0 0.5rem 0; /* Top/bottom margin, remove side margins */
    padding: 0.75rem 1rem; /* Adjust padding for better touch targets */
    text-align: left; /* Align text to left */
    border-radius: 4px; /* Keep consistent border-radius */
    /* Optional: add a bottom border for separation */
    /* border-bottom: 1px solid rgba(0,0,0,0.05); */
  }
  /* .navbar-menu .navbar-item:last-child {
    border-bottom: none;
  } */

  /* Ensure icon and text alignment is good for vertical items */
  .navbar-menu .navbar-item .icon {
    margin-right: 0.75rem; /* Adjust icon spacing if needed */
  }

  /* Remove or adjust old mobile styles that are now superseded */
  /* .navbar { flex-direction: column; align-items: flex-start; } -> No longer needed as container handles layout */
  /* .navbar-brand { margin-bottom: 1rem; } -> Set to 0 */
  /* .navbar-menu (old mobile) { width: 100%; justify-content: space-around; flex-wrap: wrap; } -> Replaced */
  /* .navbar-menu .navbar-item (old mobile) { margin: 0.5rem; } -> Replaced */
}
</style>
