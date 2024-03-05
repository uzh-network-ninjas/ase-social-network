<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <h1>{{ $t('hello') }}</h1>
  </header>

  <RouterView />
</template>
