import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'
import LoginPage from '../views/LoginPage.vue';

// Define routes
const routes = [
    {
        path: '/',
        name: 'home-page',
        component: Homepage
    },
    {
        path: '/login',
        name: 'login-page',
        component: LoginPage
    }
]

// Create Router instance
const router = createRouter({
    history: createWebHistory(),
    routes
  });
  
  export default router;