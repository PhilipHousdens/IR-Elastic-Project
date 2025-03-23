<script setup lang="ts">
import { onMounted, ref } from 'vue';
import HeadBar from '../components/HeadBar.vue';
import axios from 'axios';

interface Folder {
  folder_id: number;
  folder_name: string;
  description: string;
  created_at: string;
  average_rating: number;
}

const folders = ref<Folder[]>([]);
const folderName = ref('');
const folderDescription = ref('');
const showModal = ref(false); // Controls whether the modal is visible

const errorMessage = ref('')

// Fetch all folders
const fetchAllFolders = async () => {
  const token = localStorage.getItem('access_token');
  console.log('Token retrieved:', token);

  if (!token) {
    console.error('Token is missing, please log in.');
    errorMessage.value = 'Token is missing, please log in.';
    return;
  }

  try {
    const response = await axios.get('http://localhost:8000/folders/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    folders.value = response.data;
  } catch (error: any) {
    console.error('Error fetching folders:', error);
    errorMessage.value = 'Error fetching folders. Please try again later.';
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
        errorMessage.value = 'Sorry, this name already exists!';
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

    // Add the new folder to the list
    folders.value.push(request.data);

    // Close the modal after successful creation
    showModal.value = false;

    // Clear input fields
    folderName.value = '';
    folderDescription.value = '';
  } catch (error: any) {
    console.error('Error creating folder:', error);
  }
};

// Delete Folder
const deletFolder = async (id: number) => {
    const token = localStorage.getItem('access_token');
    console.log('Token retrieved:', token);

    if (!token) {
        console.error('Token is missing, please log in.');
        return;
    }

    try {
        await axios.delete(`http://localhost:8000/folders/${id}`, {
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        });

        folders.value = folders.value.filter(folder => folder.folder_id !== id);
    } catch (error: any) {
        console.error('Error deleting folders:', error);
    }
}

// Close modal
const closeModal = () => {
  showModal.value = false;
  folderName.value = '';
  folderDescription.value = '';
};

onMounted(() => {
  fetchAllFolders();
});
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <HeadBar />
    <div class="container mx-auto p-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-semibold mb-6">My Folders</h1>
        </div>
        <div>
          <!-- Open modal when button is clicked -->
          <button @click="showModal = true" class="p-2 px-3 text-center bg-gray-300 rounded-4xl shadow">
            + New Folder
          </button>
        </div>
      </div>

      <!-- Folders List -->
      <ul class="space-y-4">
        <li v-for="folder in folders" :key="folder.folder_id">
          <router-link :to="'/folder/' + folder.folder_id">
            <div class="flex items-center bg-white rounded-lg shadow p-4">
              <div class="flex-1">
                <h2 class="text-lg font-semibold">{{ folder.folder_name }}</h2>
                <p class="text-gray-600">{{ folder.description }}</p>
              </div>
              <div class="text-sm text-gray-500 ml-4 flex flex-col justify-end items-end">
                <p>Created at: {{ new Date(folder.created_at).toLocaleString() }}</p>
                <p>Average Rating: {{ folder.average_rating }}</p>
              </div>
            </div>
          </router-link>
            <button class="text-end text-red-400 w-full py-1 px-2" @click="deletFolder(folder.folder_id); $event.stopPropagation() ">
                DELETE
            </button>
        </li>
      </ul>
    </div>

    <!-- Modal (Popup) -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center">
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
        <div v-if="errorMessage" class="text-red-500 text-sm mt-2">
            {{ errorMessage }}
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
</template>

<style scoped>
/* Modal background (overlay) */
.fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

/* Modal content */
.bg-white {
  background-color: white;
}
</style>
