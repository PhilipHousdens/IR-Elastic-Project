<script setup lang="ts">
import { onMounted, ref } from 'vue';
import HeadBar from '../components/HeadBar.vue';
import axios from 'axios';

interface Folder {
  folder_id: number;
  folder_name: string;
  description: string;
  created_at: string;
}

const folders = ref<Folder[]>([]);

const fetchAllFolders = async () => {
  const token = localStorage.getItem("access_token");
  console.log("Token retrieved:", token);

  if (!token) {
    console.error("Token is missing, please log in.");
    return;
  }
  try {
    const response = await axios.get('http://localhost:8000/folders', {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });
    folders.value = response.data;
  } catch (error: any) {
    console.error('Error fetching folders:', error);
  }
};

onMounted(() => {
  fetchAllFolders();
});
</script>

<template>
    <div class="min-h-screen bg-gray-100">
      <HeadBar />
      <div class="container mx-auto p-4">
        <h1 class="text-3xl font-semibold mb-6">My Folders</h1>
        <ul class="space-y-4">
          <li v-for="folder in folders" :key="folder.folder_id">
            <router-link :to="'/folder/' + folder.folder_id" >
                <div class="flex items-center bg-white rounded-lg shadow p-4">
                    <div class="flex-1">
                        <h2 class="text-lg font-semibold">{{ folder.folder_name }}</h2>
                        <p class="text-gray-600">{{ folder.description }}</p>
                    </div>
                    <div class="text-sm text-gray-500 ml-4">
                        Created at: {{ new Date(folder.created_at).toLocaleString() }}
                    </div>
                </div>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </template>