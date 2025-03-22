<script setup lang="ts">
import { ref } from 'vue'
import HeadBar from '@/components/HeadBar.vue'
import SearchRecipes from '../components/SearchRecipes.vue';

</script>

<template>
  <div class="h-screen flex flex-col items-center">
    <!-- HeadBar -->
    <div class="w-full">
      <HeadBar />
    </div>

    <!-- Search Bar -->
    <SearchRecipes/>
  </div>
</template>
