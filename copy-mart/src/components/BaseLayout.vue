<template>
  <div class="flex h-screen bg-gray-100 dark:bg-gray-900 pt-16">
    <AppNavigation />
    
    <div class="flex-1 overflow-auto bg-gray-50 dark:bg-gray-800 pb-16">
      <slot />
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AppNavigation from './AppNavigation.vue'
import AppFooter from './AppFooter.vue'

export default {
  name: 'BaseLayout',
  components: {
    AppNavigation,
    AppFooter
  }
}
</script>
