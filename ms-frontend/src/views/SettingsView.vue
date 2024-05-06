<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import PageHeader from '@/components/PageHeader.vue'
import SideMenu, { type SideMenuOption } from '@/components/SideMenu.vue'
import { RouterView } from 'vue-router'
import { onMounted, onUnmounted, ref } from 'vue'

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

const sideMenuContainer = ref<HTMLElement>()
const sideBarHeight = ref<number>(0)
const previousPageOffset = ref<number>(0)
const scrollingDown = ref<boolean>(false)

onMounted(() => {
  sideBarHeight.value = sideMenuContainer.value?.clientHeight ?? 0
  window.addEventListener('scroll', onScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

const test = ref<number>(0)

const onScroll = function () {
  const currentPageOffset = window.scrollY
  scrollingDown.value = previousPageOffset.value < currentPageOffset
  previousPageOffset.value = currentPageOffset
  test.value = test.value + (previousPageOffset.value - currentPageOffset)
}
</script>

<template>
  <header class="sticky top-0 z-20">
    <SignedInTopNav />
    <PageHeader :label="$t('settings')" />
  </header>
  <main class="sm:mx-8 sm:my-4">
    <div class="relative flex w-full flex-col gap-8 sm:flex-row">
      <div
        ref="sideMenuContainer"
        :style="`--side-bar-top: ${128 - (scrollingDown ? sideBarHeight : 0)}px;`"
        class="top-transition sticky top-[8rem] z-10 w-48 bg-background max-sm:w-full max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-4 max-sm:py-4 max-sm:transition-[top] max-sm:duration-500 sm:top-[9rem] sm:z-30 sm:h-auto sm:self-start"
      >
        <SideMenu :actions="topNavActions" />
      </div>
      <div class="grow pb-4 max-sm:w-full max-sm:px-4">
        <RouterView />
      </div>
    </div>
  </main>
</template>

<style scoped>
@media (max-width: 640px) {
  .top-transition {
    top: var(--side-bar-top, 0px);
  }
}
</style>
