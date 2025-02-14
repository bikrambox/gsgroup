<template>
  <!-- <div class="min-h-screen  p-8"> -->
  <div class="w-full max-w-9/10 max-[500px]:max-w-10/10 mx-auto flex-row  items-center ">
    <div class="max-w-7xl mx-auto">
      <Profile />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

import {
  initAccordions,
  initCarousels,
  initCollapses,
  initDials,
  initDismisses,
  initDrawers,
  initDropdowns,
  initModals,
  initPopovers,
  initTabs,
  initTooltips
} from 'flowbite'
import Profile from './Profile.vue';

const metrics = ref([
  { title: 'Total Users', value: '2,543', trend: 12.4 },
  { title: 'Active Sessions', value: '1,234', trend: -3.8 },
  { title: 'Revenue', value: '$12,345', trend: 8.2 },
  { title: 'Conversion Rate', value: '3.8%', trend: 2.1 },
]);

const chartContainer = ref(null);

onMounted(() => {
  initAccordions();
  initCarousels();
  initCollapses();
  initDials();
  initDismisses();
  initDrawers();
  initDropdowns();
  initModals();
  initPopovers();
  initTabs();
  initTooltips();
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
