<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

// Define the type for a recipe
interface Recipe {
  id: number;
  name: string;
  description: string;
  keywords: string | null;
  image: string | string[];
}

const query = ref('');
const recipes = ref<Recipe[]>([]);  // Explicitly type as an array of Recipe objects
const errorMessage = ref('');

// Function to handle recipe search
const searchRecipes = async () => {
  if (query.value.trim() === '') {
    return;
  }

  try {
    const response = await axios.get('http://localhost:8000/recipes/search/', {
      params: { query: query.value },
    });

    console.log(response.data);

    // Access the 'results' key from the response
    recipes.value = response.data.results || []; // Update this to access 'results'
  } catch (error: any) {
    console.error('Error fetching recipes:', error);
    errorMessage.value = 'Failed to search recipes. Please try again.';
  }
};

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
    <div class="search-recipes-container">
      <div class="flex items-center justify-center border border-gray-300 rounded-lg p-2 w-80 mt-8 mx-auto">
        <input 
          type="text" 
          v-model="query"
          placeholder="Search for recipes..." 
          class="flex-1 p-2 border-none rounded-l-lg focus:outline-none focus:ring-2 focus:ring-amber-400"
        />
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
