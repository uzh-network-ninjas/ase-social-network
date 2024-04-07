import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue'
import HomeView from '@/views/HomeView.vue'
import SignInView from '@/views/SignInView.vue'
import ProfileView from '@/views/ProfileView.vue'
import TestView from '@/views/TestView.vue'
import SettingsView from '@/views/SettingsView.vue'
import AccountSettingsView from '@/views/Settings/AccountSettingsView.vue'
import ProfileSettingsView from '@/views/Settings/ProfileSettingsView.vue'

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
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      redirect: { name: 'settings-profile' },
      children: [
        {
          path: 'account',
          name: 'settings-account',
          component: AccountSettingsView
        },
        {
          path: 'profile',
          name: 'settings-profile',
          component: ProfileSettingsView
        }
      ]
    },
    {
      path: '/test',
      name: 'test',
      component: TestView
    }
  ]
})



export default router
