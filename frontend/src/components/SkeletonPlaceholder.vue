<template>
  <div class="skeleton-wrapper">
    <Skeleton height="2rem" width="30%" class="mb-2" />
    <div class="grid">
      <Skeleton height="10rem" class="col-4" v-for="i in 3" :key="i" />
    </div>
  </div>
</template>

<script setup>
import Skeleton from 'primevue/skeleton';
</script>

<style scoped>
.skeleton-wrapper {
  padding: 2rem;
}
</style>
