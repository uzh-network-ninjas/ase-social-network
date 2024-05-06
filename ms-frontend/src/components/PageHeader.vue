<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import Button from 'primevue/button'

defineProps<{
  label: string
}>()
</script>

<template>
  <div
    class="z-40 bg-white py-3 max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-2 sm:px-4"
  >
    <router-link :to="{ name: 'home' }" custom v-slot="{ navigate }">
      <Button text rounded :label="label" class="text-2xl !font-extralight" @click="navigate">
        <template #icon>
          <BaseIcon icon="chevron-left" />
        </template>
      </Button>
    </router-link>
  </div>
</template>
