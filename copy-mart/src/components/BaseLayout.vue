<template>
  <div class="flex h-screen bg-gray-100">
    <AppNavigation />
    
    <div class="flex-1 overflow-auto bg-gray-50">
      <slot />
    </div>
  </div>
</template>

<script>
import AppNavigation from './AppNavigation.vue'

export default {
  name: 'BaseLayout',
  components: {
    AppNavigation
  }
}
</script>
