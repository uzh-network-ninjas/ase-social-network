<script setup lang="ts">
import ExclamationCircleIcon from '@/icons/ExclamationCircleIcon.vue'
import EyeIcon from '@/icons/EyeIcon.vue'
import EyeSlashIcon from '@/icons/EyeSlashIcon.vue'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import SparklesIcon from '@/icons/SparklesIcon.vue'
import ArrowLeftEndOnRectangle from '@/icons/ArrowLeftEndOnRectangleIcon.vue'
import ArrowLeftStartOnRectangle from '@/icons/ArrowLeftStartOnRectangleIcon.vue'
import UserPlusIcon from '@/icons/UserPlusIcon.vue'
import ShareIcon from '@/icons/ShareIcon.vue'
import ThreeDotsIcon from '@/icons/ThreeDotsIcon.vue'
import MiniChevronDown from '@/icons/MiniChevronDownIcon.vue'
import UserIcon from '@/icons/UserIcon.vue'
import Cog6Tooth from '@/icons/Cog6ToothIcon.vue'
import FriendsIcon from '@/icons/FriendsIcon.vue'
import ChevronLeft from '@/icons/ChevronLeftIcon.vue'
import ArrowUp from '@/icons/ArrowUpIcon.vue'
import ArrowDown from '@/icons/ArrowDownIcon.vue'

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
  <UserPlusIcon
    v-else-if="icon == 'user-plus'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <ShareIcon v-else-if="icon == 'share'" v-bind="$attrs" :size="size" :strokeWidth="strokeWidth" />
  <ThreeDotsIcon
    v-else-if="icon == 'three-dots'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <MiniChevronDown
    v-else-if="icon == 'mini-down'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
</template>
