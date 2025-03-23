import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'
import LoginPage from '../views/LoginPage.vue';
import Registerpage from '../views/Registerpage.vue';

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
    },
    {
        path: '/register',
        name: 'register-page',
        component: Registerpage
    }
]

// Create Router instance
const router = createRouter({
    history: createWebHistory(),
    routes
  });
  
  export default router;