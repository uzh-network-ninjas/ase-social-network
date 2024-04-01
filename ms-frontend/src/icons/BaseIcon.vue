<script setup lang="ts">
import ExclamationCircleIcon from '@/icons/ExclamationCircleIcon.vue'
import EyeIcon from '@/icons/EyeIcon.vue'
import EyeSlashIcon from '@/icons/EyeSlashIcon.vue'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import SparklesIcon from '@/icons/SparklesIcon.vue'
import ArrowLeftEndOnRectangle from '@/icons/ArrowLeftEndOnRectangle.vue'
import ArrowLeftStartOnRectangle from '@/icons/ArrowLeftStartOnRectangle.vue'
import ArrowUp from '@/icons/ArrowUp.vue'
import ArrowDown from '@/icons/ArrowDown.vue'

export type IconType =
  | 'exclamation-circle'
  | 'eye'
  | 'eye-slash'
  | 'magnifying-glass'
  | 'sparkles'
  | 'arrow-left-end-on-rectangle'
  | 'arrow-left-start-on-rectangle'
  | 'arrow-up'
  | 'arrow-down'
  | undefined

withDefaults(
  defineProps<{
    icon: IconType
    strokeWidth?: number
    size?: number
  }>(),
  {
    strokeWidth: 1,
    size: 6
  }
)

defineOptions({
  inheritAttrs: false
})
</script>

<template>
  <ExclamationCircleIcon
    v-if="icon == 'exclamation-circle'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <EyeIcon v-else-if="icon == 'eye'" v-bind="$attrs" :size="size" :strokeWidth="strokeWidth" />
  <EyeSlashIcon
    v-else-if="icon == 'eye-slash'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <MagnifyingGlassIcon
    v-else-if="icon == 'magnifying-glass'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <SparklesIcon
    v-else-if="icon == 'sparkles'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <ArrowLeftEndOnRectangle
    v-else-if="icon == 'arrow-left-end-on-rectangle'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <ArrowLeftStartOnRectangle
    v-else-if="icon == 'arrow-left-start-on-rectangle'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <ArrowUp v-else-if="icon == 'arrow-up'" v-bind="$attrs" :size="size" :strokeWidth="strokeWidth" />
  <ArrowDown
    v-else-if="icon == 'arrow-down'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
</template>
