<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Define a reactive reference to hold the username
const username = ref('');

// When the component is mounted, fetch the username from localStorage
onMounted(() => {
  const storedUsername = localStorage.getItem('username');
  if (storedUsername) {
    username.value = storedUsername;
  }
});

// Log out function: remove username and token from localStorage
const logout = () => {
  localStorage.removeItem('username');
  localStorage.removeItem('access_token');
  username.value = ''; // Clear the username ref
  window.location.href = '/'; // Redirect to home or login page
};
</script>

<template>
    <div class="w-full h-16 bg-amber-400 flex items-center justify-between px-10">
      <div>
        <p class="text-2xl">Food<b class="text-white">YUMYUM</b></p>
      </div>
      <div class="space-x-4 text-lg">
        <router-link to="/">Home</router-link>
        <router-link to="/">Folder</router-link>
        <router-link to="/">Bookmark</router-link>
        <router-link to="/">Recommendation</router-link>
      </div>
  
      <div>
        <div v-if="username">
          <!-- Show Username and Log Out Button if user is logged in -->
          <span class="mr-4 text-white">{{ username }}</span>
          <button @click="logout" class="bg-white px-3 py-2 rounded-3xl text-black">
            Log Out
          </button>
        </div>
        <div v-else>
          <!-- Show Sign In and Sign Up Buttons if user is not logged in -->
          <div class="flex space-x-4">
            <div class="bg-white px-3 py-2 rounded-3xl">
              <router-link to="/login">
                Sign In
              </router-link>
            </div>
            <router-link to="/register">
                <div class="bg-white px-3 py-2 rounded-3xl">
                    <p>
                        Sign up
                    </p>
                </div>
            </router-link>
            
          </div>
        </div>
      </div>
    </div>
</template>
  