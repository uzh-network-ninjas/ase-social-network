<script setup lang="ts">
import Navbar from '@/components/TopNav.vue'
import DecoStrip from '@/components/DecoStrip.vue'
import TogglePillGroup from '@/components/TogglePillGroup.vue'
import { computed, onMounted, ref } from 'vue'
import { userService } from '@/services/userService'
import type { DietaryCriteria } from '@/types/DietaryCriteria'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const restriction_options = ref<string[]>([])
const preferences_options = ref<string[]>([])

const restrictions = ref<string[]>(authStore.user?.restrictions ?? [])
const preferences = ref<string[]>(authStore.user?.preferences ?? [])

const page = ref<number>(0)

onMounted(() => {
  userService
    .getDietaryCriteria()
    .then((response: DietaryCriteria) => {
      restriction_options.value = response.restrictions
      preferences_options.value = response.preferences
    })
    .catch((error) => {
      console.log(error)
    })
})

const nextButtonEnabled = computed(() => {
  return preferences.value.length >= 5
})

const onBack = function () {
  if (page.value == 1) {
    page.value = 0
  }
}

const onNext = function () {
  if (page.value == 0) {
    page.value = 1
  } else if (page.value == 1) {
    onSave()
  }
}

const onSave = function () {
  authStore
    .updateUser({ restrictions: restrictions.value, preferences: preferences.value })
    .then(() => {
      router.push({ name: 'home' })
    })
}
</script>

<template>
  <header class="sticky top-0 z-20">
    <Navbar :titleTo="{ name: 'onboarding' }" />
  </header>
  <main class="md:pl-16 md:pr-1/4">
    <div
      class="mx-8 flex h-full flex-col items-center justify-start pb-8 pt-16 md:mx-4 md:justify-center md:pt-8"
    >
      <div class="flex flex-col gap-16 max-md:grow">
        <h1
          class="text-center text-2xl font-light uppercase tracking-widest text-secondary md:text-start md:text-5xl"
        >
          {{ $t('preferences') }}
        </h1>
        <div :class="['flex flex-col gap-4 max-md:grow', page === 1 ? 'max-md:hidden' : '']">
          <div class="flex flex-col">
            <h2
              class="mb-2 text-center text-lg font-light tracking-widest text-primary md:text-start md:text-xl"
            >
              {{ $t('dietary_restrictions') }}
            </h2>
            <span class="text-center font-light text-medium-emphasis md:text-start">{{
              $t('select_all_apply')
            }}</span>
          </div>

          <TogglePillGroup v-model="restrictions" :options="restriction_options" />
        </div>
        <div :class="['flex flex-col gap-4 max-md:grow', page === 0 ? 'max-md:hidden' : '']">
          <div class="flex flex-col">
            <h2
              class="mb-2 text-center text-lg font-light tracking-widest text-primary md:text-start md:text-xl"
            >
              {{ $t('culinary_preferences') }}
            </h2>
            <span
              v-if="preferences.length < 5"
              class="text-center font-light text-medium-emphasis md:text-start"
              >{{ $t('pick_at_least_five', { amount: 5 - preferences.length }) }}</span
            >
            <span v-else class="text-center font-light text-medium-emphasis md:text-start">{{
              $t('pick_all_like')
            }}</span>
          </div>

          <TogglePillGroup v-model="preferences" :options="preferences_options" />
        </div>
        <div class="flex gap-8 md:hidden md:w-fit">
          <Button
            outlined
            rounded
            :class="['w-fit grow md:invisible', page === 0 ? 'invisible' : '']"
            :label="$t('back')"
            @click="onBack"
          />
          <Button
            rounded
            class="grow"
            :label="$t('next')"
            :disabled="page === 1 && !nextButtonEnabled"
            @click="onNext"
          />
        </div>
        <Button
          rounded
          class="w-fit max-md:hidden"
          :label="$t('next')"
          :disabled="!nextButtonEnabled"
          @click="onSave"
        />
      </div>
    </div>
  </main>
  <DecoStrip class="fixed bottom-0 left-3/4 top-0 z-50 max-lg:invisible lg:visible" />
</template>

<style scoped>
main {
  height: calc(100vh - 64px);
}
</style>
