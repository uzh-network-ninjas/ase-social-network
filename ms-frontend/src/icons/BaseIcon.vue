<script setup lang="ts">
import ExclamationCircleIcon from '@/icons/ExclamationCircleIcon.vue'
import EyeIcon from '@/icons/EyeIcon.vue'
import EyeSlashIcon from '@/icons/EyeSlashIcon.vue'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import SparklesIcon from '@/icons/SparklesIcon.vue'
import ArrowLeftEndOnRectangle from '@/icons/ArrowLeftEndOnRectangle.vue'
import ArrowLeftStartOnRectangle from '@/icons/ArrowLeftStartOnRectangle.vue'
import UserPlusIcon from '@/icons/UserPlusIcon.vue'
import ShareIcon from '@/icons/ShareIcon.vue'
import BackIcon from '@/icons/BackIcon.vue'
import ThreeDotsIcon from '@/icons/ThreeDotsIcon.vue'
import MiniChevronDown from '@/icons/MiniChevronDown.vue'
import ProfileIcon from '@/icons/ProfileIcon.vue'
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
  | 'user-plus'
  | 'share'
  | 'back'
  | 'three-dots'
  | 'mini-down'
  | 'profile'
  | 'arrow-up'
  | 'arrow-down'
  | undefined

withDefaults(
  defineProps<{
    icon: IconType
    strokeWidth?: number
    imageUrl?: string
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
  <UserPlusIcon v-else-if="icon == 'user-plus'" v-bind="$attrs" />
  <ShareIcon v-else-if="icon == 'share'" v-bind="$attrs" />
  <BackIcon v-else-if="icon == 'back'" v-bind="$attrs" />
  <ThreeDotsIcon v-else-if="icon == 'three-dots'" v-bind="$attrs" />
  <MiniChevronDown v-else-if="icon == 'mini-down'" v-bind="$attrs" />
  <ProfileIcon v-else-if="icon === 'profile' && imageUrl" v-bind="$attrs" :imageUrl="imageUrl" />
</template>
