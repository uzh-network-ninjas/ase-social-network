<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import { computed } from 'vue'
const props = withDefaults(
  defineProps<{
    rating?: number
    size?: 'normal' | 'small'
  }>(),
  {
    rating: 0,
    size: 'normal'
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
      :class="[size === 'normal' ? '!h-4 !w-4' : '!h-3 !w-3']"
      icon="star-solid"
      :strokeWidth="1"
      :key="i"
    />
    <BaseIcon
      v-for="i in 5.0 - totalStart"
      :class="['text-medium-emphasis', size === 'normal' ? '!h-4 !w-4' : '!h-3 !w-3']"
      icon="star"
      :strokeWidth="1"
      :key="i"
    />
  </div>
</template>
