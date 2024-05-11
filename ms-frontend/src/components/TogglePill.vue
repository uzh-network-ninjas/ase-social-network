<script setup lang="ts">
defineProps<{
  labelKey: string
  active: boolean
}>()
</script>

<template>
  <button
    v-ripple="{
      pt: {
        root: { style: 'transform: scale(0); background: #fff;' }
      }
    }"
    :class="[
      ' align-center flex w-fit cursor-pointer justify-center rounded-full border px-3 py-0 outline-none ring-offset-1 focus-visible:ring-1',
      active
        ? 'border-primary bg-primary text-white  ring-primary'
        : 'border-medium-emphasis bg-white text-medium-emphasis ring-medium-emphasis'
    ]"
  >
    <span class="select-none text-center font-light tracking-widest">{{
      labelKey ? $t(labelKey.replace(/ /g, '_').toLowerCase()) : 'Label'
    }}</span>
  </button>
</template>
