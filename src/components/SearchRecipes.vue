<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';

// Define the type for a recipe
interface Recipe {
  id: number;
  name: string;
  description: string;
  keywords: string | null;
  image: string | string[];
}

// Reactive references
const query = ref('');
const recipes = ref<Recipe[]>([]);
const suggestions = ref<string[]>([]);  // To hold real-time suggestions
const errorMessage = ref('');

// Function to handle recipe search
const searchRecipes = async () => {
  if (query.value.trim() === '') {
    suggestions.value = []; // Clear suggestions if the query is empty
    return;
  }

  try {
    const response = await axios.get('http://localhost:8000/recipes/search/', {
      params: { query: query.value },
    });

    console.log(response.data);
    recipes.value = response.data.results || [];
  } catch (error: any) {
    console.error('Error fetching recipes:', error);
    errorMessage.value = 'Failed to search recipes. Please try again.';
  }
};

const getSuggestions = async () => {
  if (query.value.trim() === '') {
    suggestions.value = [];
    return;
  }

  try {
    const response = await axios.get('http://localhost:8000/recipes/search/', {
      params: { query: query.value, page: 1, size: 5 }, // Limit to 5 suggestions
    });

    console.log('API Response:', response.data);

    // Assuming the results contain recipe names
    suggestions.value = response.data.results.map((result: any) => result.Name);
  } catch (error) {
    console.error('Error fetching suggestions:', error);
  }
};

const selectSuggestion = (suggestion: string) => {
  query.value = suggestion;  // Set input to selected suggestion
  suggestions.value = [];  // Clear suggestions after selection
};


watch(query, (newQuery) => {
  console.log('Query changed:', newQuery);  // Log query changes
  if (newQuery.length > 2) {  // Start suggesting after 3 characters are typed
    getSuggestions();
  } else {
    suggestions.value = [];  // Clear suggestions if input is too short
  }
});

// Utility to clean image URLs
const cleanImageUrls = (rawUrls: string) => {
  const cleaned = rawUrls.replace('c(', '').replace(')', '').split(',').map((url: string) => url.replace(/"/g, '').trim());
  let tempUrl = '';
  cleaned.forEach((part: string, index: number) => {
    if (part.startsWith('http')) {
      tempUrl = part;
    } else {
      tempUrl += (index === 0 ? '' : ',') + part;
    }
  });
  return tempUrl;
};
</script>

<template>
  <div class="relative search-recipes-container">
    <div class="flex items-center justify-center border border-gray-300 rounded-lg p-2 w-80 mt-8 mx-auto">
      <input 
        type="text" 
        v-model="query"
        placeholder="Search for recipes..." 
        class="flex-1 p-2 border-none rounded-l-lg focus:outline-none focus:ring-2 focus:ring-amber-400"
      />
      <!-- Suggestions Dropdown -->
      <div 
        v-if="suggestions.length > 0 && query" 
        class="absolute top-full left-0 w-full mt-1 bg-white shadow-lg rounded-md z-20"
      >
        <ul class="max-h-60 overflow-y-auto">
          <li
            v-for="(suggestion, index) in suggestions"
            :key="index"
            @click="selectSuggestion(suggestion)"
            class="px-4 py-2 cursor-pointer hover:bg-gray-200"
          >
            {{ suggestion }}
          </li>
        </ul>
      </div>
      <button 
        @click="searchRecipes"
        class="bg-amber-400 text-white p-2 rounded-r-lg hover:bg-amber-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Search
      </button>
    </div>

    <div v-if="errorMessage" class="text-red-500 mt-4">{{ errorMessage }}</div>

    <!-- Display Search Results -->
    <div v-if="recipes && recipes.length > 0" class="mt-8 w-1/2 mx-auto">
      <div v-for="recipe in recipes" :key="recipe.id" class="border-b py-4">
        <router-link :to="'/recipe/' + recipe.RecipeId">
          <img :src="cleanImageUrls(recipe.image_link)" alt="Recipe Image" class="w-fit h-auto"/>
          <h3 class="text-lg font-semibold">{{ recipe.Name }}</h3>
          <p class="text-gray-600">{{ recipe.Description }}</p>
        </router-link>
      </div>
    </div>
  </div>
</template>
