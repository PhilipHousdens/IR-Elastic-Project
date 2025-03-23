<script setup lang="ts">
import { ref, onMounted } from 'vue';
import HeadBar from '../components/HeadBar.vue';
import axios from 'axios';

interface Recipe {
  Name: string;
  image_link: string;
  Calories: number;
  ProteinContent: number;
  FatContent: number;
  SaturatedFatContent: number;
  CholesterolContent: number;
  SodiumContent: number;
  CarbohydrateContent: number;
  FiberContent: number;
  SugarContent: number;
  RecipeServings: number;
  RecipeInstructions: string[];
  Description: string;
  DatePublished: string;
  RecipeCategory: string;
  Keywords: string;
  CookTime: string;
  PrepTime: string;
  TotalTime: string;
  AggregatedRating: number;
  ReviewCount: number;
}

const recipe = ref<Recipe | null>(null);

const cleanInstructions = (rawInstructions: string): string[] => {
  // Clean up the instructions string
  const cleaned = rawInstructions
    .replace('c(', '') // Remove 'c(' at the beginning
    .replace(')', '') // Remove ')' at the end
    .split('", "') // Split by the '", "' pattern
    .map((instruction: string) => instruction.replace(/"/g, '').trim()); // Remove quotes and trim spaces

  return cleaned;
};

// Fetch recipe details by ID
const fetchRecipeDetails = async (id: string) => {
  try {
    const response = await fetch(`http://localhost:8000/recipes/${id}`);
    const data: Recipe = await response.json();
    // Clean the RecipeInstructions field
    data.RecipeInstructions = cleanInstructions(data.RecipeInstructions);
    recipe.value = data;
  } catch (error) {
    console.error("Error fetching recipe:", error);
  }
};

// Clean the image URLs
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
// Get recipe ID from route params and fetch recipe data when the component is mounted
onMounted(() => {
  const recipeId = (window.location.pathname.split('/').pop() as string); // Alternatively, use vue-router
  fetchRecipeDetails(recipeId);
});

const addToBookmark = async (recipeId: number, folderId: number, rating: number | 0) => {
  console.log("Client time:", new Date());
  const token = localStorage.getItem("access_token"); // Retrieve token from localStorage
  console.log("Token retrieved:", token); // Log the token

  if (!token) {
    console.error("Token is missing, please log in.");
    return;
  }

  try {
    const response = await axios.post(
      "http://localhost:8000/bookmarks/",
      {
        recipe_id: recipeId,
        folder_id: folderId,
        rating: rating || 1,
      },
      {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log("Bookmark added successfully:", response.data); // Log response data
    return response.data; // Return the response data if needed.
  } catch (error) {
    console.error("Error adding bookmark:", error);
    throw error; // Rethrow the error to be handled by the caller.
  }
};

const handleAddToBookmark = async () => {
  if (recipe.value) {
    try {
      const result = await addToBookmark(recipe.value.RecipeId, 1, recipe.value.AggregatedRating);
      console.log('Bookmark operation result:', result);
      // Handle successful bookmark addition (e.g., show a success message)
    } catch (error) {
      console.error('Failed to add bookmark:', error);
      // Handle errors (e.g., show an error message)
    }
  }
};
</script>

<template>
    <div>
        <div>
            <HeadBar /> <!-- Ensure this is imported correctly -->
        </div>
        <div class="max-w-4xl mx-auto p-4" v-if="recipe">
            <div>
                <div class="flex items-end justify-end">
                    <button
                        class="text-white bg-amber-400 p-2 rounded-3xl font-bold px-3"
                        @click="handleAddToBookmark"
                    >
                        Add To Bookmark
                    </button>
                </div>
                <h1 class="text-4xl font-bold text-center mb-4">{{ recipe.Name }}</h1>
                <img :src="cleanImageUrls(recipe.image_link)" alt="Recipe Image" class="w-full h-auto rounded-lg shadow-md mb-6" />
                
                <!-- Recipe Details Section -->
                <div class="mb-6">
                <p class="text-lg">{{ recipe.Description }}</p>
                <p class="mt-2 text-sm text-gray-600">Published on: {{ recipe.DatePublished }}</p>
                <p class="mt-2 text-sm text-gray-600">Recipe Category: {{ recipe.RecipeCategory }}</p>
                </div>
        
                <!-- Nutrition Facts Section -->
                <div class="mb-6">
                <h2 class="text-2xl font-semibold mb-2">Nutrition Facts:</h2>
                <ul class="list-inside space-y-1">
                    <li><strong>Calories:</strong> {{ recipe.Calories }} kcal</li>
                    <li><strong>Protein:</strong> {{ recipe.ProteinContent }} g</li>
                    <li><strong>Fat:</strong> {{ recipe.FatContent }} g</li>
                    <li><strong>Saturated Fat:</strong> {{ recipe.SaturatedFatContent }} g</li>
                    <li><strong>Cholesterol:</strong> {{ recipe.CholesterolContent }} mg</li>
                    <li><strong>Sodium:</strong> {{ recipe.SodiumContent }} mg</li>
                    <li><strong>Carbohydrates:</strong> {{ recipe.CarbohydrateContent }} g</li>
                    <li><strong>Fiber:</strong> {{ recipe.FiberContent }} g</li>
                    <li><strong>Sugar:</strong> {{ recipe.SugarContent }} g</li>
                </ul>
                </div>
        
                <!-- Recipe Instructions Section -->
                <div class="mb-6">
                <h2 class="text-2xl font-semibold mb-2">Recipe Instructions:</h2>
                <ol class="list-decimal pl-5 space-y-2">
                    <li v-for="(step, index) in recipe.RecipeInstructions" :key="index" class="text-lg">{{ step }}</li>
                </ol>
                </div>
        
                <!-- Time Section -->
                <div class="mb-6">
                    <h2 class="text-2xl font-semibold mb-2">Cooking Time:</h2>
                    <p><strong>Prep Time:</strong> {{ recipe.PrepTime }}</p>
                    <p><strong>Cook Time:</strong> {{ recipe.CookTime }}</p>
                    <p><strong>Total Time:</strong> {{ recipe.TotalTime }}</p>
                    </div>
            
                    <!-- Rating Section -->
                    <div class="mb-6">
                    <h2 class="text-2xl font-semibold mb-2">Recipe Rating:</h2>
                    <p><strong>Rating:</strong> {{ recipe.AggregatedRating }} / 5</p>
                    <p><strong>Reviews:</strong> {{ recipe.ReviewCount }} reviews</p>
                    </div>
            
                    <!-- Servings Section -->
                    <div class="mb-6">
                    <h2 class="text-2xl font-semibold mb-2">Servings:</h2>
                    <p>This recipe serves {{ recipe.RecipeServings }} people.</p>
                    </div>
                </div>
            </div>
            <div v-else class="text-center text-xl text-gray-500">
            <p>Loading...</p>
            </div>
    </div>
    
  </template>
  