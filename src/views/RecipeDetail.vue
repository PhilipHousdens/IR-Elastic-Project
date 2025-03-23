<script setup lang="ts">
import { ref, onMounted } from 'vue';
import HeadBar from '../components/HeadBar.vue';
import axios from 'axios';

// Define the Recipe interface and variables
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

interface Folder {
  folder_id: number;
  folder_name: string;
  description: string;
  created_at: string;
}

const recipe = ref<Recipe | null>(null);
const folders = ref<Folder[]>([]);  // Store the list of folders
const showModal = ref(false);  // Show modal flag
const showModelCF = ref(false);
const folderName = ref('');
const folderDescription = ref('');
const selectedFolderId = ref<number | null>(null);  // Store the selected folder ID
const rating = ref(1);  // Default rating

const errorMessage_book = ref('');
const errorMessage_folder = ref('');


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
    data.RecipeInstructions = cleanInstructions(data.RecipeInstructions)
    recipe.value = data;
    console.log("Fetched recipe:", recipe.value);
  } catch (error) {
    console.error("Error fetching recipe:", error);
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




// Fetch user folders from the API
const fetchUserFolders = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    console.error("Token is missing, please log in.");
    return;
  }

  try {
    const response = await axios.get("http://localhost:8000/folders/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    folders.value = response.data; // Store the user's folders
  } catch (error) {
    console.error("Error fetching folders:", error);
  }
};

// Create new folder
const createFolder = async () => {
  const token = localStorage.getItem('access_token');
  console.log('Token retrieved:', token);

  if (!token) {
    console.error('Token is missing, please log in.');
    return;
  }

  // Check if folder name already exists
  const folderExists = folders.value.some(folder => folder.folder_name === folderName.value);
  
  if (folderExists) {
      errorMessage_folder.value = 'Sorry, this name already exists!';
      return; // Stop execution if folder exists
  }

  try {
    const request = await axios.post('http://localhost:8000/folders/', 
        {
        folder_name: folderName.value,
        description: folderDescription.value,
        },
        {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        }

    );

    // Optionally, you could update the folders list with the new folder
    folders.value.push(request.data);
    // Close the modal after successful creation
    showModelCF.value = false;
    // Clear input fields
    folderName.value = '';
    folderDescription.value = '';
  } catch (error: any) {
    console.error('Error creating folder:', error);
  }
};

// Function to add bookmark
const addToBookmark = async (recipeId: number, folderId: number, rating: number) => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    console.error("Token is missing, please log in.");
    return;
  }

  try {
    const userId = localStorage.getItem("user_id"); // Assuming user_id is stored in localStorage
    const response = await axios.post(
      "http://localhost:8000/bookmarks/",
      {
        recipe_id: recipeId,
        folder_id: folderId,
        user_id: userId,
        rating: rating,
      },
      {
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      }
    );
    console.log("Bookmark added successfully:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error adding bookmark:", error);
    throw error;
  }
};

// Fetch all bookmarks for the selected folder
const fetchBookmarksForFolder = async (folderId: number) => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    console.error("Token is missing, please log in.");
    return [];
  }

  try {
    const response = await axios.get(`http://localhost:8000/folders/${folderId}/bookmarks/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data; // Return existing bookmarks
  } catch (error) {
    console.error("Error fetching bookmarks:", error);
    return [];
  }
};

// Handle adding to bookmark by selecting a folder
const handleAddToBookmark = async () => {
    if (recipe.value && selectedFolderId.value && selectedFolderId.value !== null) {
        
        try {
            const existingBookmarks = await fetchBookmarksForFolder(selectedFolderId.value);
    
            // Check if the recipe is already in the selected folder
            const alreadyBookmarked = existingBookmarks.some(bookmark => bookmark.recipe_id === recipe.value.RecipeId);

            if (alreadyBookmarked) {
            errorMessage_book.value = 'This recipe is already in the selected folder.'
            return; // Prevent duplicate bookmarks
            }

            const result = await addToBookmark(recipe.value.RecipeId, selectedFolderId.value, rating.value);
            console.log('Bookmark operation result:', result);
            showModal.value = false; // Close the modal
        } catch (error) {
        console.error('Failed to add bookmark:', error);
        }
    } else {
        console.error('No folder selected or recipe details are missing.');
    }
};

// Close modal
const closeModal = () => {
  showModelCF.value = false;
  folderName.value = '';
  folderDescription.value = '';
};

// Fetch recipe details and folders on mounted
onMounted(() => {
  const recipeId = (window.location.pathname.split('/').pop() as string);
  fetchRecipeDetails(recipeId);
  fetchUserFolders(); // Fetch user folders when the component mounts
});
</script>

<template>
    <div>
      <HeadBar />
      <div class="max-w-4xl mx-auto p-4" v-if="recipe">
        <div>
          <!-- Button to open the modal -->
          <div class="flex items-end justify-end">
            <button
              class="text-white bg-amber-400 p-2 rounded-3xl font-bold px-3"
              @click="showModal = true"
            >
              Add To Bookmark
            </button>
          </div>
          <h1 class="text-4xl font-bold text-start mb-4">{{ recipe.Name }}</h1>
          <img :src="cleanImageUrls(recipe.image_link)" alt="Recipe Image" class="w-1/2 mx-auto h-auto rounded-lg shadow-md mb-6" />
          
          <!-- Recipe Details Section -->
          <div class="mb-6">
            <p class="text-lg">{{ recipe.Description }}</p>
            <p class="mt-2 text-sm text-gray-600 underline">Published on: {{ recipe.DatePublished }}</p>
            <p class="mt-2 text-sm text-gray-600 underline">Recipe Category: {{ recipe.RecipeCategory }}</p>
          </div>

          <hr class="text-gray-300">
  
          <!-- Nutrition Facts Section -->
          <div class="my-6">
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

          <hr class="text-gray-300">

          <!-- Recipe Instructions Section -->
          <div class="my-6">
            <h2 class="text-2xl font-semibold mb-2">Recipe Instructions:</h2>
            <ol class="list-decimal pl-5 space-y-2">
              <li v-for="(step, index) in recipe.RecipeInstructions" :key="index" class="text-lg">{{ step }}</li>
            </ol>
          </div>

          <hr class="text-gray-300">
  
          <!-- Time Section -->
          <div class="my-6">
            <h2 class="text-2xl font-semibold mb-2">Cooking Time:</h2>
            <p><strong>Prep Time:</strong> {{ recipe.PrepTime }}</p>
            <p><strong>Cook Time:</strong> {{ recipe.CookTime }}</p>
            <p><strong>Total Time:</strong> {{ recipe.TotalTime }}</p>
          </div>

          <hr class="text-gray-300">
          
          <!-- Rating Section -->
          <div class="my-6">
            <h2 class="text-2xl font-semibold mb-2">Recipe Rating:</h2>
            <p><strong>Rating:</strong> {{ recipe.AggregatedRating }} / 5</p>
            <p><strong>Reviews:</strong> {{ recipe.ReviewCount }} reviews</p>
          </div>

          <hr class="text-gray-300">
          
          <!-- Servings Section -->
          <div class="my-6">
            <h2 class="text-2xl font-semibold mb-2">Servings:</h2>
            <p>This recipe serves {{ recipe.RecipeServings }} people.</p>
          </div>
        </div>
  
        <!-- Modal for Folder Selection -->
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div class="bg-white p-6 rounded-lg w-96">
            <h2 class="text-xl font-semibold mb-4">Add to Bookmark</h2>
  
            <!-- List of Folders -->
            <div class="mb-4">
              <h3 class="text-sm font-medium">Choose a Folder:</h3>
              <ul class="space-y-2 mt-2">
                <li v-for="folder in folders" :key="folder.folder_id">
                    <button
                        class="block w-full text-left p-2 border rounded hover:bg-gray-100"
                        @click="selectedFolderId = folder.folder_id; console.log(selectedFolderId)"
                        :class="{'bg-blue-200': selectedFolderId === folder.folder_id}" 
                    >
                        {{ folder.folder_name }}
                    </button>
                </li>
              </ul>
            </div>
            <div class="flex justify-end items-center pb-2">
                <button @click="showModelCF = true" class="p-2 px-3 text-center bg-gray-300 rounded-4xl shadow cursor-pointer ">
                    + New Folder
                </button>
            </div>
            
  
            <!-- Rating Input Section -->
            <div class="mb-4">
              <label for="rating" class="block text-sm font-medium">Rating (1-5)</label>
              <input
                v-model.number="rating"
                id="rating"
                type="number"
                min="1"
                max="5"
                step="1"
                class="mt-2 block w-full p-2 border border-gray-300 rounded"
                placeholder="Rate 1-5"
              />
            </div>
            <div v-if="errorMessage_book" class="text-red-500 text-sm mt-2">
                {{ errorMessage_book }}
            </div>
  
            <div class="flex justify-between mt-4">
              <button @click="showModal = false" class="text-gray-500">Cancel</button>
              <button @click="handleAddToBookmark" class="bg-blue-500 text-white p-2 rounded-lg">Add Bookmark</button>
            </div>
          </div>
        </div>

        <!-- + New folder -->
        <div v-if="showModelCF" class="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center z-50">
            <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
                <h2 class="text-xl font-semibold mb-4">Create New Folder</h2>
                <div class="mb-4">
                <label for="folderName" class="block text-sm font-medium text-gray-700">Folder Name</label>
                <input
                    id="folderName"
                    v-model="folderName"
                    type="text"
                    class="mt-1 p-2 w-full border border-gray-300 rounded-md"
                    placeholder="Enter folder name"
                />
                </div>
                <div v-if="errorMessage_folder" class="text-red-500 text-sm mt-2">
                    {{ errorMessage_folder }}
                </div>
                <div class="mb-4">
                <label for="folderDescription" class="block text-sm font-medium text-gray-700">Folder Description</label>
                <input
                    id="folderDescription"
                    v-model="folderDescription"
                    type="text"
                    class="mt-1 p-2 w-full border border-gray-300 rounded-md"
                    placeholder="Enter folder description"
                />
                </div>
                <div class="flex justify-between">
                <button @click="closeModal" class="text-gray-600 hover:text-gray-900">Cancel</button>
                <button @click="createFolder" class="bg-blue-500 text-white px-4 py-2 rounded-md">Create Folder</button>
                </div>
            </div>
        </div>
      </div>
    </div>
  </template>
  