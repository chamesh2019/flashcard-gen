<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link :to="{ path: '/', query: route.query }" class="navbar-item brand-text">
          <span class="logo-icon">📚</span>
          FlashcardGen
        </router-link>
      </div>
      <div class="navbar-menu">
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
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isAdmin = computed(() => route.query.admin !== undefined);
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
  display: flex;
  align-items: center;
  position: relative;
  padding: 0.5rem 1rem;
  margin-left: 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.icon {
  margin-right: 0.5rem;
}

.navbar-menu .navbar-item:hover {
  color: var(--primary-color);
  background-color: rgba(59, 130, 246, 0.05);
}

.navbar-menu .router-link-active {
  color: var(--primary-color);
  background-color: rgba(59, 130, 246, 0.1);
  font-weight: 500;
}

.navbar-menu .navbar-item::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.navbar-menu .navbar-item:hover::after,
.navbar-menu .router-link-active::after {
  transform: scaleX(1);
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    padding: 1rem;
  }

  .navbar-brand {
    margin-bottom: 1rem;
  }

  .navbar-menu {
    width: 100%;
    justify-content: space-around;
    flex-wrap: wrap;
  }

  .navbar-menu .navbar-item {
    margin: 0.5rem;
  }

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
