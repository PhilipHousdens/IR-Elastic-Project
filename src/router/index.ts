import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'
import LoginPage from '../views/LoginPage.vue';
import Registerpage from '../views/Registerpage.vue';
import RecipeDetail from '../views/RecipeDetail.vue';
import Folderpage from '../views/Folderpage.vue';
import Bookmark from '../views/Bookmark.vue';

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
    },
    {
        path: '/recipe/:id', // Dynamic route for recipe details
        component: RecipeDetail,
        name: 'recipeDetail',
        props: true // Pass the route params as props to the component
    },
    {
        path:'/folder',
        name: 'bookmark-page',
        component: Folderpage
    },
    {
        path:'/folder/:id',
        name: 'bookmarkInFolder',
        component: Bookmark
    }
]

// Create Router instance
const router = createRouter({
    history: createWebHistory(),
    routes
  });
  
  export default router;