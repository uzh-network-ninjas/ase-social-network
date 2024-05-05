<script setup lang="ts">
import TopNav, { type MenuOption } from '@/components/TopNav.vue'
import { type IconType } from '@/icons/BaseIcon.vue'
import { useAuthStore } from '@/stores/auth'
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import SideMenu, { type SideMenuOption } from '@/components/SideMenu.vue'

const authStore = useAuthStore()

const topNavActions: MenuOption[] = [
  {
    labelKey: 'sign_up',
    to: { name: 'sign-up' }
  },
  {
    labelKey: 'sign_in',
    icon: 'arrow-left-start-on-rectangle' as IconType,
    to: { name: 'sign-in' }
  }
]

const sideNavActions: SideMenuOption[] = [
  {
    labelKey: 'map',
    icon: 'map',
    to: { name: 'map' }
  },
  {
    labelKey: 'search_user',
    icon: 'user-plus',
    to: { name: 'search-user' }
  }
]
</script>

<template>
  <header class="sticky top-0 z-40">
    <TopNav v-if="!authStore.signedIn" :actions="topNavActions" iconPos="right" />
    <SignedInTopNav v-else />
    <div
      v-if="authStore.signedIn"
      class="z-40 bg-white py-3 max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-2 sm:px-4"
    >
      <h1 class="ml-8 text-2xl font-extralight text-medium-emphasis">{{ $t('home') }}</h1>
    </div>
  </header>

  <main class="sm:mx-8 sm:my-4">
    <template v-if="authStore.signedIn">
      <div class="relative flex w-full flex-col gap-8">
        <div
          class="w-48 max-sm:w-full max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-4 max-sm:py-4 sm:fixed sm:z-30"
        >
          <SideMenu :actions="sideNavActions" />
        </div>
        <div class="grow pb-4 max-sm:w-full max-sm:px-4 sm:ml-56">
          <!-- FEED -->
        </div>
      </div>
    </template>
  </main>
</template>
