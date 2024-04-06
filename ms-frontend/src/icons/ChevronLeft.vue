<script setup lang="ts">
withDefaults(
  defineProps<{
    strokeWidth?: number
    size?: number
  }>(),
  {
    strokeWidth: 1,
    size: 6
  }
)
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    :stroke-width="strokeWidth"
    stroke="currentColor"
    :class="`w-${size} h-${size}`"
  >
    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
  </svg>
</template>
