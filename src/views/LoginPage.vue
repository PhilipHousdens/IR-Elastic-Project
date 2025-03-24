<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

// Define refs for form input values
const username = ref('');
const password = ref('');

// Define a ref to store the error message (if any)
const errorMessage = ref('');

// Handle form submission
const handleLogin = async (e: Event) => {
  e.preventDefault();  // Prevent the default form submission

  // Reset the error message
  errorMessage.value = '';

  try {
    // Make POST request to backend for login
    const response = await axios.post(
      'http://localhost:8000/login', 
      {
        username: username.value,
        password: password.value,
      },
      {
        headers: {
          'Content-Type': 'application/json', // Ensure the content type is JSON
        }
      }
    );

    // Log the response to inspect the token
    console.log("Login response:", response.data);

    // If successful, store the token (or handle success)
    const token = response.data.access_token;
    localStorage.setItem('access_token', token);
    localStorage.setItem('username', username.value)

    // Redirect or update UI (optional)
    window.location.href = '/';
  } catch (error: any) {
    // Handle error response
    if (error.response && error.response.status === 401) {
      errorMessage.value = 'Incorrect username or password';
    } else {
      errorMessage.value = 'An error occurred. Please try again later.';
    }
  }
};
</script>

<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h1 class="text-3xl text-center"><b>Food</b><b class="text-amber-400">YUMYUM</b></h1>
        <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Sign in to your account</h2>
      </div>
  
      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6" @submit="handleLogin">
          <div>
            <label for="username" class="block text-sm/6 font-medium text-gray-900">Username</label>
            <div class="mt-2">
              <input type="text" v-model="username" id="username" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>
  
          <div>
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm/6 font-medium text-gray-900">Password</label>
              <div class="text-sm">
                <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
              </div>
            </div>
            <div class="mt-2">
              <input type="password" v-model="password" id="password" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>
  
          <!-- Show error message if any -->
          <div v-if="errorMessage" class="text-red-500 text-sm mt-2">
            {{ errorMessage }}
          </div>
  
          <div>
            <button type="submit" class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
          </div>

          <div>
            <p class="text-center">Don't have a account? <router-link to="/register" class="underline text-indigo-600">join us</router-link></p>
          </div>
        </form>
      </div>
    </div>
  </template>
  