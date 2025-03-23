<script setup lang="ts">
import { onMounted, ref } from 'vue';
import HeadBar from '../components/HeadBar.vue';
import axios from 'axios';

interface Bookmark {
  recipe_id: number;
  folder_id: string;
  user_id: string;
  rating: string;
  recipeDetails: any;
}

const bookmarks = ref<Bookmark[]>([]);

const fetchBookmark = async (id: string) => {
  const token = localStorage.getItem("access_token");
  console.log("Token retrieved:", token);

  if (!token) {
    console.error("Token is missing, please log in.");
    return;
  }
  try {
    const response = await axios.get(`http://localhost:8000/folders/${id}/bookmarks/`, {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    const bookmarksData = response.data;

    // Fetch recipe details for each bookmark
    const bookmarksWithRecipes = await Promise.all(
      bookmarksData.map(async (bookmark: Bookmark) => {
        try {
          const recipeResponse = await axios.get(`http://localhost:8000/recipes/${bookmark.recipe_id}`);
          return { ...bookmark, recipeDetails: recipeResponse.data };
        } catch (recipeError) {
          console.error(`Error fetching recipe ${bookmark.recipe_id}:`, recipeError);
          return { ...bookmark, recipeDetails: null }; // Handle recipe fetch error
        }
      })
    );

    bookmarks.value = bookmarksWithRecipes;
  } catch (error: any) {
    console.error('Error fetching bookmarks:', error);
  }
};

const fetchAllBookmarks = async () => {
  const token = localStorage.getItem("access_token");
  console.log("Token retrieved:", token);

  if (!token) {
    console.error("Token is missing, please log in.");
    return;
  }

  try {
    const response = await axios.get("http://localhost:8000/bookmarks/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const bookmarksData = response.data;

    // Fetch recipe details for each bookmark
    const bookmarksWithRecipes = await Promise.all(
      bookmarksData.map(async (bookmark: Bookmark) => {
        try {
          const recipeResponse = await axios.get(
            `http://localhost:8000/recipes/${bookmark.recipe_id}`
          );
          return { ...bookmark, recipeDetails: recipeResponse.data };
        } catch (recipeError) {
          console.error(
            `Error fetching recipe ${bookmark.recipe_id}:`,
            recipeError
          );
          return { ...bookmark, recipeDetails: null }; // Handle recipe fetch error
        }
      })
    );

    bookmarks.value = bookmarksWithRecipes;
  } catch (error: any) {
    console.error("Error fetching all bookmarks:", error);
  }
};

onMounted(() => {
  const bookmarkId = window.location.pathname.split('/').pop(); 

  if (bookmarkId && !isNaN(Number(bookmarkId))) {
    // If an ID exists and is a valid number, fetch bookmarks for that specific folder
    fetchBookmark(bookmarkId);
  } else {
    // If no ID in the URL, fetch all bookmarks
    fetchAllBookmarks();
  }
});

</script>

<template>
    <div class="min-h-screen bg-gray-100">
      <HeadBar />
      <div class="container mx-auto p-4">
        <h1 class="text-3xl font-semibold mb-6">My Bookmarks</h1>
        <ul class="space-y-4">
          <li v-for="book in bookmarks" :key="book.recipe_id">
            <router-link :to="'/recipe/' + book.recipe_id">
                <div class="flex items-center bg-white rounded-lg shadow p-4">
                    <div class="flex-1">
                        <h2 class="text-lg font-semibold" v-if="book.recipeDetails">
                        {{ book.recipeDetails.Name }}
                        </h2>
                        <p class="text-gray-600" v-if="book.recipeDetails">
                        {{ book.recipeDetails.Description }}
                        </p>
                        <p v-else>Recipe details not available.</p>
                    </div>
                    <div class="text-sm text-gray-500 ml-4">
                        Rating: {{ book.rating }}
                    </div>
                </div>
            </router-link>
            
          </li>
        </ul>
      </div>
    </div>
  </template>