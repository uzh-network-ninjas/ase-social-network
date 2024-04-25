import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue'
import HomeView from '@/views/HomeView.vue'
import SignInView from '@/views/SignInView.vue'
import ProfileView from '@/views/ProfileView.vue'
import TestView from '@/views/TestView.vue'
import SettingsView from '@/views/SettingsView.vue'
import AccountSettingsView from '@/views/Settings/AccountSettingsView.vue'
import ProfileSettingsView from '@/views/Settings/ProfileSettingsView.vue'
import PreferenceSettingsView from '@/views/Settings/PreferenceSettingsView.vue'
import { useAuthStore } from '@/stores/auth'
import OnboardingView from '@/views/OnboardingView.vue'
import MapView from '@/views/MapView.vue'

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
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      redirect: { name: 'settings-profile' },
      meta: { requiresAuth: true },
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
        },
        {
          path: 'preferences',
          name: 'settings-preferences',
          component: PreferenceSettingsView
        }
      ]
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView,
      meta: { requiresAuth: true }
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
      props: (route) => ({ query: route.query.query, placeId: route.query.placeId }),
      meta: { requiresAuth: true }
    },
    {
      path: '/test',
      name: 'test',
      component: TestView
    },
    {
      path: '/:catchAll(.*)',
      redirect: { name: 'home' }
    }
  ]
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    return {
      name: 'sign-in'
    }
  }
})
export default router
