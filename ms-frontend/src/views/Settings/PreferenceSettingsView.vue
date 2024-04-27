<script setup lang="ts">
import TogglePillGroup from '@/components/TogglePillGroup.vue'
import { onMounted, ref, watch } from 'vue'

import { userService } from '@/services/userService'
import type { DietaryCriteria } from '@/types/DietaryCriteria'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const restriction_options = ref<string[]>([])
const preferences_options = ref<string[]>([])

const restrictions = ref<string[]>(authStore.user?.restrictions ?? [])
const preferences = ref<string[]>(authStore.user?.preferences ?? [])

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

const updateCriteria = function () {
  authStore.updateUser({ restrictions: restrictions.value, preferences: preferences.value })
}

watch(
  [restrictions, preferences],
  () => {
    updateCriteria()
  },
  { deep: true }
)
</script>

<template>
  <div class="flex w-full flex-col gap-8">
    <h1 class="text-2xl uppercase tracking-widest text-primary">{{ $t('preferences') }}</h1>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">
          {{ $t('dietary_restrictions') }}
        </h2>
      </div>
      <TogglePillGroup v-model="restrictions" :options="restriction_options" />
    </div>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">
          {{ $t('culinary_preferences') }}
        </h2>
      </div>
      <TogglePillGroup v-model="preferences" :options="preferences_options" />
    </div>
  </div>
</template>
