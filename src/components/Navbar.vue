<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link :to="{ path: '/', query: route.query }" class="navbar-item">
          <span class="logo-icon">🧠</span> FlashcardGen
        </router-link>
      </div>

      <button class="navbar-toggle" :class="{ 'is-active': isMobileMenuOpen }" @click="toggleMobileMenu"
        aria-label="menu" aria-expanded="isMobileMenuOpen">
        <span></span>
        <span></span>
        <span></span>
      </button>

      <div class="navbar-menu" :class="{ 'is-active': isMobileMenuOpen }">
        <router-link :to="{ path: '/', query: route.query }" class="navbar-item"
          @click="isMobileMenuOpen = false">Home</router-link>
        <router-link v-if="isAdmin" :to="{ path: '/add-subject', query: route.query }" class="navbar-item"
          @click="isMobileMenuOpen = false">Add
          Subject</router-link>
        <router-link v-if="isAdmin" :to="{ path: '/upload-document', query: route.query }" class="navbar-item"
          @click="isMobileMenuOpen = false">Upload
          Document</router-link>
        <router-link v-if="isAdmin" :to="{ path: '/document-info', query: route.query }" class="navbar-item"
          @click="isMobileMenuOpen = false">Document
          Info</router-link>
        <router-link :to="{ path: '/ignored-flashcards', query: route.query }" class="navbar-item"
          @click="isMobileMenuOpen = false">Ignored
          Flashcards</router-link>
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

.navbar-menu .navbar-item {
  color: var(--text-color);
  text-decoration: none;
  padding: 0.75rem 1rem;
  display: block;
  transition: background-color 0.2s ease, color 0.2s ease;
  border-radius: 4px;
  margin: 0 0.25rem;
}

.navbar-menu .navbar-item:hover,
.navbar-menu .navbar-item.router-link-active {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--primary-color);
}

.navbar-toggle {
  display: none;
  cursor: pointer;
  background: transparent;
  border: none;
  padding: 0.5rem;
  margin-left: auto;
}

.navbar-toggle span {
  display: block;
  width: 25px;
  height: 3px;
  background-color: var(--text-color, #333);
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
  .container {
    flex-direction: row;
    flex-wrap: wrap;
    position: relative;
  }

  .navbar-brand {
    margin-right: auto;
  }

  .navbar-toggle {
    display: block;
    order: 1;
  }

  .navbar-menu {
    display: none;
    flex-direction: column;
    width: 100%;
    background-color: #fff;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-top: 1px solid #eee;
    padding: 0.5rem 0;
  }

  .navbar-menu.is-active {
    display: flex;
  }

  .navbar-menu .navbar-item {
    width: 100%;
    text-align: left;
    padding: 0.75rem 1.5rem;
    margin: 0;
    border-bottom: 1px solid #f0f0f0;
  }

  .navbar-menu .navbar-item:last-child {
    border-bottom: none;
  }

  .navbar-menu .navbar-item .icon {
    margin-right: 0.5rem;
  }
}
</style>
