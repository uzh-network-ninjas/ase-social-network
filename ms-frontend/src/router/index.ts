import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue'
import HomeView from '@/views/HomeView.vue'
import SignInView from '@/views/SignInView.vue'
import ProfileView from '@/views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/sign-up',
      name: 'sign-up',
      component: SignUpView
    },
    {
      path: '/sign-in',
      name: 'sign-in',
      component: SignInView
    },
    {
      path: '/terms-and-conditions',
      name: 'terms-and-conditions',
      redirect: '/'
    },
    
    {
      path: '/profile/:userId',
      name: 'profile',
      component: ProfileView
    }
  ]
})



export default router
