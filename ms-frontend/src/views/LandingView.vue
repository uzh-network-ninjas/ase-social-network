<script setup lang="ts">
import TopNav, { type MenuOption } from '@/components/TopNav.vue'
import type { IconType } from '@/icons/BaseIcon.vue'
import Button from 'primevue/button'
import { onMounted, onUnmounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import SignedInTopNav from '@/components/SignedInTopNav.vue'

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

const atTopPage = ref<boolean>(true)

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleScroll = function () {
  if (window.scrollY > 5) {
    if (atTopPage.value) {
      atTopPage.value = false
    }
  } else if (!atTopPage.value) {
    atTopPage.value = true
  }
}
</script>

<template>
  <header :class="['sticky top-0 z-40 transition-shadow', atTopPage ? '' : 'shadow-lg']">
    <TopNav
      v-if="!authStore.signedIn"
      :titleTo="{ name: 'landing' }"
      :actions="topNavActions"
      iconPos="right"
    />
    <SignedInTopNav v-else />
  </header>
  <main>
    <div class="flex flex-col">
      <div class="parallax-image bg0 self-stretch" />
      <div class="relative self-stretch border-t-[.5rem] border-white bg-primary">
        <div class="relative flex w-full flex-col gap-12 px-12 pt-20">
          <div class="flex flex-col gap-8">
            <h1 class="text-3xl uppercase text-white antialiased md:text-5xl">
              {{ $t('landing_title') }}
            </h1>
            <div
              class="mx:max-w-[50%] flex flex-col gap-4 text-xl font-light text-medium-emphasis md:text-2xl"
            >
              <p>{{ $t('landing_text') }}</p>
              <p>{{ $t('landing_sign_up_appeal') }}</p>
            </div>
          </div>
          <router-link :to="{ name: 'sign-up' }" v-slot="{ navigate }">
            <Button
              class="w-fit !rounded-full bg-white py-2 text-xl !text-secondary md:text-3xl"
              rounded
              :label="$t('sign_up')"
              @click="navigate"
            />
          </router-link>
        </div>
        <div class="pointer-events-none absolute left-0 right-0 top-full h-[100vh] overflow-hidden">
          <div
            class="u-rot-left absolute bottom-full h-[200%] w-[200%] border-b-[.5rem] border-white bg-primary"
          ></div>
        </div>
      </div>
      <div class="parallax-image bg1 self-stretch" />
      <div class="relative self-stretch bg-background">
        <div
          class="pointer-events-none absolute bottom-full left-0 right-0 h-[100vh] overflow-hidden"
        >
          <div
            class="t-rot-right absolute top-full h-[200%] w-[200%] border-t-[.5rem] border-secondary bg-background"
          ></div>
        </div>
        <div class="relative flex w-full flex-col gap-16 px-12 py-20 text-center">
          <div class="flex flex-col gap-2 uppercase">
            <h1 class="text-5xl text-secondary">{{ $t('landing_discover') }}</h1>
            <h1 class="text-3xl text-primary">{{ $t('landing_discover_title') }}</h1>
          </div>

          <p class="text-xl font-light text-medium-emphasis md:text-2xl">
            {{ $t('landing_discover_text') }}
          </p>
        </div>
        <div class="pointer-events-none absolute left-0 right-0 top-full h-[100vh] overflow-hidden">
          <div
            class="u-rot-right absolute bottom-full h-[200%] w-[200%] border-b-[.5rem] border-secondary bg-background"
          ></div>
        </div>
      </div>
      <div class="parallax-image bg2 self-stretch" />
      <div class="relative self-stretch bg-background">
        <div
          class="pointer-events-none absolute bottom-full left-0 right-0 h-[100vh] overflow-hidden"
        >
          <div
            class="t-rot-left absolute top-full h-[200%] w-[200%] border-t-[.5rem] border-primary bg-background"
          ></div>
        </div>
        <div class="relative flex w-full flex-col gap-16 px-12 py-20 text-center">
          <div class="flex flex-col gap-2 uppercase">
            <h1 class="text-5xl text-secondary">{{ $t('landing_follow') }}</h1>
            <h1 class="text-3xl text-primary">{{ $t('landing_follow_title') }}</h1>
          </div>

          <p class="text-xl font-light text-medium-emphasis md:text-2xl">
            {{ $t('landing_follow_text') }}
          </p>
        </div>
        <div class="pointer-events-none absolute left-0 right-0 top-full h-[100vh] overflow-hidden">
          <div
            class="u-rot-left absolute bottom-full h-[200%] w-[200%] border-b-[.5rem] border-primary bg-background"
          ></div>
        </div>
      </div>
      <div class="parallax-image bg3 self-stretch" />
      <div
        class="flex flex-col gap-16 self-stretch border-t-[.5rem] border-secondary bg-primary px-16 py-28 text-center"
      >
        <h1 class="text-3xl uppercase text-white md:text-5xl">Review App</h1>
        <p class="text-xl font-light text-medium-emphasis md:text-2xl">
          {{ $t('landing_footer_text') }}
        </p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.parallax-image {
  background-attachment: fixed;
  background-repeat: no-repeat;
  background-size: cover;
}

.bg0 {
  background-image: url(@/assets/ExampleImageMain.png);
  background-position: center;
  height: 45vh;
}

.bg1 {
  background-image: url(@/assets/ExampleImageMap.png);
  height: 110vh;
  background-position: left;
}

.bg2 {
  background-image: url(@/assets/ExampleImageProfile.png);
  height: 110vh;
  background-position: left;
}

.bg3 {
  background-image: url(@/assets/ExampleImageFeed.png);
  height: 110vh;
  background-position: left;
}

.t-rot-right {
  transform: translate(-50%, -2rem) rotate(-6deg) translate(50%, 0);
}

.t-rot-left {
  right: 0;
  transform: translate(50%, -2rem) rotate(6deg) translate(-50%, 0);
}

.u-rot-right {
  transform: translate(-50%, 2rem) rotate(6deg) translate(50%, 0);
}

.u-rot-left {
  right: 0;
  transform: translate(50%, 2rem) rotate(-6deg) translate(-50%, 0);
}
</style>
