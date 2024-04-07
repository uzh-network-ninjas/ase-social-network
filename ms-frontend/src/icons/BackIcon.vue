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
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M15.75 19.5L8.25 12L15.75 4.5" stroke="black" stroke-opacity="0.6" stroke-linecap="round"
            stroke-linejoin="round" />
    </svg>
</template>