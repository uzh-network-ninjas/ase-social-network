<script setup lang="ts">
import ExclamationCircleIcon from '@/icons/ExclamationCircleIcon.vue'
import EyeIcon from '@/icons/EyeIcon.vue'
import EyeSlashIcon from '@/icons/EyeSlashIcon.vue'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import SparklesIcon from '@/icons/SparklesIcon.vue'
import ArrowLeftEndOnRectangle from '@/icons/ArrowLeftEndOnRectangle.vue'
import ArrowLeftStartOnRectangle from '@/icons/ArrowLeftStartOnRectangle.vue'
import UserIcon from '@/icons/UserIcon.vue'
import Cog6Tooth from '@/icons/Cog6Tooth.vue'
import FriendsIcon from '@/icons/FriendsIcon.vue'
import ChevronLeft from '@/icons/ChevronLeft.vue'
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
  | 'user'
  | 'friends'
  | 'cog-6-tooth'
  | 'chevron-left'
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
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <EyeIcon v-else-if="icon == 'eye'" v-bind="$attrs" :strokeWidth="strokeWidth" :size="size" />
  <EyeSlashIcon
    v-else-if="icon == 'eye-slash'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <MagnifyingGlassIcon
    v-else-if="icon == 'magnifying-glass'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <SparklesIcon
    v-else-if="icon == 'sparkles'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ArrowLeftEndOnRectangle
    v-else-if="icon == 'arrow-left-end-on-rectangle'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ArrowLeftStartOnRectangle
    v-else-if="icon == 'arrow-left-start-on-rectangle'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <UserIcon v-else-if="icon == 'user'" v-bind="$attrs" :strokeWidth="strokeWidth" :size="size" />
  <FriendsIcon
    v-else-if="icon == 'friends'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <Cog6Tooth
    v-else-if="icon == 'cog-6-tooth'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ChevronLeft
    v-else-if="icon == 'chevron-left'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ArrowUp v-else-if="icon == 'arrow-up'" v-bind="$attrs" :size="size" :strokeWidth="strokeWidth" />
  <ArrowDown
    v-else-if="icon == 'arrow-down'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
</template>
