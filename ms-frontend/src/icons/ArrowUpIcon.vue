<script setup lang="ts">
withDefaults(
  defineProps<{
    strokeWidth?: number
  }>(),
  {
    strokeWidth: 1
  }
)
</script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path
      d="M3.75 8.75L10 2.5M10 2.5L16.25 8.75M10 2.5V17.5"
      stroke="black"
      stroke-opacity="0.6"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>
