<template>
  <div id="app" :class="{ dark: isDarkMode }">
    <RouterView />
    <ApiStatus />
  </div>
</template>

<script>
import ApiStatus from '@/components/ApiStatus.vue'

export default {
  name: 'App',
  components: {
    ApiStatus
  },
  data() {
    return {
      isDarkMode: localStorage.getItem('darkMode') !== 'false'
    }
  },
  watch: {
    isDarkMode(newVal) {
      localStorage.setItem('darkMode', newVal)
      if (newVal) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  },
  mounted() {
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark')
    }
    window.addEventListener('darkModeChange', (e) => {
      this.isDarkMode = e.detail.isDarkMode
    })
  }
}
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #374151;
  min-height: 100vh;
}

#app.dark {
  background-color: #1f2937;
  color: #f3f4f6;
}
</style>
