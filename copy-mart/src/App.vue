<template>
  <div id="app">
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
</style>
