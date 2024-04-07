<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import PageHeader from '@/components/PageHeader.vue'
import SideMenu, { type SideMenuOption } from '@/components/SideMenu.vue'
import { RouterView } from 'vue-router'

const topNavActions: SideMenuOption[] = [
  {
    labelKey: 'profile',
    icon: 'user',
    to: { name: 'settings-profile' }
  },
  {
    labelKey: 'account',
    icon: 'cog-6-tooth',
    to: { name: 'settings-account' }
  },
  {
    labelKey: 'preferences',
    icon: 'face-smile',
    to: { name: 'settings-preferences' }
  }
]
</script>

<template>
  <header class="sticky top-0 z-20">
    <SignedInTopNav />
    <PageHeader label="Settings" />
  </header>
  <main class="sm:mx-8 sm:my-4">
    <div class="relative flex w-full flex-col gap-8">
      <div
        class="w-48 max-sm:w-full max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-4 max-sm:py-4 sm:fixed sm:z-30"
      >
        <SideMenu :actions="topNavActions" />
      </div>
      <div class="grow pb-4 max-sm:w-full max-sm:px-4 sm:ml-56">
        <RouterView />
      </div>
    </div>
  </main>
</template>
