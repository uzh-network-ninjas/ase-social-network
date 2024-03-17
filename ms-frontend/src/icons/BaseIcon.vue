<script setup lang="ts">
import ExclamationCircleIcon from '@/icons/ExclamationCircleIcon.vue'
import EyeIcon from '@/icons/EyeIcon.vue'
import EyeSlashIcon from '@/icons/EyeSlashIcon.vue'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import SparklesIcon from '@/icons/SparklesIcon.vue'
import ArrowLeftEndOnRectangle from '@/icons/ArrowLeftEndOnRectangle.vue'
import ArrowLeftStartOnRectangle from '@/icons/ArrowLeftStartOnRectangle.vue'

export type IconType =
  | 'exclamation-circle'
  | 'eye'
  | 'eye-slash'
  | 'magnifying-glass'
  | 'sparkles'
  | 'arrow-left-end-on-rectangle'
  | 'arrow-left-start-on-rectangle'
  | undefined

withDefaults(
  defineProps<{
    icon: IconType
    strokeWidth?: number
  }>(),
  {
    strokeWidth: 1
  }
)

defineOptions({
  inheritAttrs: false
})
</script>

<template>
  <ExclamationCircleIcon v-if="icon == 'exclamation-circle'" v-bind="$attrs" />
  <EyeIcon v-else-if="icon == 'eye'" v-bind="$attrs" />
  <EyeSlashIcon v-else-if="icon == 'eye-slash'" v-bind="$attrs" />
  <MagnifyingGlassIcon v-else-if="icon == 'magnifying-glass'" v-bind="$attrs" />
  <SparklesIcon v-else-if="icon == 'sparkles'" v-bind="$attrs" />
  <ArrowLeftEndOnRectangle v-else-if="icon == 'arrow-left-end-on-rectangle'" v-bind="$attrs" />
  <ArrowLeftStartOnRectangle v-else-if="icon == 'arrow-left-start-on-rectangle'" v-bind="$attrs" />
</template>
