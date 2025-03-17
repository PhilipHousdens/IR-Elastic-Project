<script setup lang="ts">
import { ref } from 'vue'
import HeadBar from '@/components/HeadBar.vue'

</script>

<template>
  <div class="h-screen flex flex-col items-center">
    <!-- HeadBar -->
    <div class="w-full">
      <HeadBar />
    </div>

    <!-- Search Bar -->
    <div class="flex items-center justify-center border border-gray-300 rounded-lg p-2 w-80 mt-8">
      <!-- Search Input -->
      <input 
        type="text" 
        placeholder="Search..." 
        class="flex-1 p-2 border-none rounded-l-lg focus:outline-none focus:ring-2 focus:ring-amber-400"
      />
      <!-- Search Button -->
      <button class="bg-amber-400 text-white p-2 rounded-r-lg hover:bg-amber-400 focus:outline-none focus:ring-2 focus:ring-blue-500">
        Search
      </button>
    </div>
  </div>
</template>
