import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'

// Define routes
const routes = [
    {
        path: '/',
        name: 'home-page',
        component: Homepage
    }
]

// Create Router instance
const router = createRouter({
    history: createWebHistory(),
    routes
  });
  
  export default router;