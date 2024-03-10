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
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    :stroke-width="strokeWidth"
    stroke="currentColor"
    class="h-5 w-5"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
    />
  </svg>
</template>

<style scoped></style>
