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
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
            d="M2.5 13.75V15.625C2.5 16.1223 2.69754 16.5992 3.04917 16.9508C3.40081 17.3025 3.87772 17.5 4.375 17.5H15.625C16.1223 17.5 16.5992 17.3025 16.9508 16.9508C17.3025 16.5992 17.5 16.1223 17.5 15.625V13.75M6.25 6.25L10 2.5M10 2.5L13.75 6.25M10 2.5V13.75"
            stroke="black" stroke-opacity="0.6" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
</template>