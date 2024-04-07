<template>
  <img :src="imageUrl" alt="Icon Image" :style="{ width: size, height: size }" />
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  imageUrl: String, // Prop for the image URL
  size: {
    type: String,
    default: '1.5rem' // Default size for the icon
  }
})
</script>

<style scoped>
/* Add any custom styling for the image */
</style>
