<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import Button from 'primevue/button'

defineProps<{
  label: string
}>()
</script>

<template>
  <div
    class="z-40 bg-white py-3 max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-2 sm:px-6"
  >
    <Button text rounded :label="label" class="text-2xl">
      <template #icon>
        <BaseIcon icon="chevron-left" />
      </template>
    </Button>
  </div>
</template>
