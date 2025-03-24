<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';

interface Recipe {
  RecipeId: number;
  Name: string;
  Description: string;
  Keywords: string | null;
  image_link: string;
}

const query = ref('');
const recipes = ref<Recipe[]>([]);
const suggestions = ref<string[]>([]);
const errorMessage = ref('');
const showSuggestions = ref(true);

const currentPage = ref(1);
const totalPages = ref(0);
const totalResults = ref(0);

const searchRecipes = async () => {
  if (query.value.trim() === '') {
    suggestions.value = [];
    return;
  }

  // Ensure page and size are valid
  const currentPageNumber = isNaN(currentPage.value) || currentPage.value <= 0 ? 1 : currentPage.value;  // Default to 1 if invalid
  const pageSize = 10;  // Or dynamically set this if needed

  try {
    const response = await axios.get('http://localhost:8000/recipes/search/', {
      params: { 
        query: query.value, 
        page: currentPageNumber, 
        size: pageSize
      }
    });

    console.log(response.data);
    
    // Set the recipes
    recipes.value = response.data.results || [];
    
    // Set the total number of results and calculate totalPages
    totalResults.value = response.data.total || 0;
    totalPages.value = Math.min(Math.ceil(totalResults.value / pageSize), 10);  // Calculate total pages
    
    showSuggestions.value = false;
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
      params: { query: query.value, page: 1, size: 5 },
    });

    suggestions.value = response.data.results.map((result: any) => result.Name);
  } catch (error) {
    console.error('Error fetching suggestions:', error);
  }
};

const selectSuggestion = (suggestion: string) => {
  query.value = suggestion;
  suggestions.value = [];
};

watch(query, (newQuery) => {
  if (newQuery.length > 2) {
    getSuggestions();
    showSuggestions.value = true;
  } else {
    suggestions.value = [];
    showSuggestions.value = false;
  }
});

const changePage = (newPage: number) => {
  // Validate that newPage is a valid number (greater than 0)
  if (isNaN(newPage) || newPage <= 0) {
    newPage = 1;  // Default to the first page if invalid
  }

  // Limit page number to not exceed totalPages (maximum of 10 pages)
  if (newPage > 10) {
    newPage = 10;
  }

  currentPage.value = newPage;  // Update currentPage state

  // Make sure to call the search function with the new page
  searchRecipes();  
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
  <div class="relative search-recipes-container">
    <div class="flex items-center justify-center border border-gray-300 rounded-lg p-2 w-80 mt-8 mx-auto relative">
      <input
        type="text"
        v-model="query"
        placeholder="Search for recipes..."
        class="flex-1 p-2 border-none rounded-l-lg focus:outline-none focus:ring-2 focus:ring-amber-400"
      />
      
      <!-- Suggestions Dropdown -->
      <div
        v-if="suggestions.length > 0 && showSuggestions"
        class="absolute top-full left-0 w-full mt-1 bg-white shadow-lg rounded-md z-30"
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

      <!-- Search Button -->
      <button
        @click="searchRecipes"
        class="bg-amber-400 text-white p-2 rounded-r-lg hover:bg-amber-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Search
      </button>
    </div>

    <div v-if="recipes && recipes.length > 0" class="my-4 flex justify-center items-center space-x-4">
      <button
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50"
      >
        Previous
      </button>

      <span class="text-gray-700">
        {{ currentPage }} / {{ totalPages }}
      </span>

      <button
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50"
      >
        Next
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="text-red-500 mt-4">{{ errorMessage }}</div>

    <!-- Search Results -->
    <div v-if="recipes && recipes.length > 0" class="mt-8 w-[80%] mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <router-link v-for="recipe in recipes" :key="recipe.RecipeId" :to="'/recipe/' + recipe.RecipeId" class="block">
          <div class="bg-white rounded-lg shadow overflow-hidden">
            <img :src="cleanImageUrls(recipe.image_link)" alt="Recipe Image" class="w-full h-48 object-cover" />
            <div class="p-4">
              <h3 class="text-lg font-semibold mb-2">{{ recipe.Name }}</h3>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Pagination Controls -->
    <div v-if="recipes && recipes.length > 0" class="my-4 flex justify-center items-center space-x-4">
      <button
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50"
      >
        Previous
      </button>

      <span class="text-gray-700">
        {{ currentPage }} / {{ totalPages }}
      </span>

      <button
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50"
      >
        Next
      </button>
    </div>
  </div>
</template>
