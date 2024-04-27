<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import { computed } from 'vue'
const props = withDefaults(
  defineProps<{
    rating?: number
  }>(),
  {
    rating: 0
  }
)

const totalStart = computed<number>(() => {
  return Math.floor(Math.min(Math.max(props.rating, 0), 5) ?? 0)
})
</script>

<template>
  <div class="flex gap-1">
    <BaseIcon
      v-for="i in totalStart"
      class="!h-4 !w-4"
      icon="star-solid"
      :strokeWidth="1"
      :key="i"
    />
    <BaseIcon
      v-for="i in 5.0 - totalStart"
      class="!h-4 !w-4 text-medium-emphasis"
      icon="star"
      :strokeWidth="1"
      :key="i"
    />
  </div>
</template>
