<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import SideMenu, { type SideMenuOption } from '@/components/SideMenu.vue'

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
    <SignedInTopNav />
    <div
      class="z-40 bg-white py-3 max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-2 sm:px-4"
    >
      <h1 class="ml-8 text-2xl font-extralight text-medium-emphasis">Home</h1>
    </div>
  </header>
  <main class="sm:mx-8 sm:my-4">
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
  </main>
</template>
