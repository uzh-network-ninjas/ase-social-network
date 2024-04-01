<script setup lang="ts">
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import { type IconType } from '@/icons/BaseIcon.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const signedIn = authStore.signedIn
console.log('signed in?: ', signedIn)
const name = authStore.user?.username ?? ''
console.log('username: ', name)

const topNavActions: MenuOption[] = [
  ...(signedIn
    ? [
        {
          labelKey: 'sign_out',
          icon: 'arrow-left-end-on-rectangle' as IconType,
          before: () => {
            authStore.signOut()
          },
          to: { name: 'sign-in' }
        }
      ]
    : [
        {
          labelKey: 'sign_up',
          to: { name: 'sign-up' }
        },
        {
          labelKey: 'sign_in',
          icon: 'arrow-left-start-on-rectangle' as IconType,
          to: { name: 'sign-in' }
        }
      ])
]
</script>

<template>
  <header class="sticky top-0 z-40">
    <Navbar :actions="topNavActions" iconPos="right" />
  </header>

  <main class="m-8">
    <div
      v-if="signedIn"
      class="text-center text-2xl font-light uppercase tracking-widest text-secondary md:text-start md:text-5xl"
    >
      Hello, {{ name }}!
    </div>
  </main>
</template>
