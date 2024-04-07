<script setup lang="ts">
import ExclamationCircleIcon from '@/icons/ExclamationCircleIcon.vue'
import EyeIcon from '@/icons/EyeIcon.vue'
import EyeSlashIcon from '@/icons/EyeSlashIcon.vue'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import ArrowLeftEndOnRectangleIcon from '@/icons/ArrowLeftEndOnRectangleIcon.vue'
import ArrowLeftStartOnRectangleIcon from '@/icons/ArrowLeftStartOnRectangleIcon.vue'
import Cog6ToothIcon from '@/icons/Cog6ToothIcon.vue'
import FriendsIcon from '@/icons/FriendsIcon.vue'
import UserIcon from '@/icons/UserIcon.vue'
import ChevronLeftIcon from '@/icons/ChevronLeftIcon.vue'
import ArrowUpIcon from '@/icons/ArrowUpIcon.vue'
import ArrowDownIcon from '@/icons/ArrowDownIcon.vue'
import UserPlusIcon from '@/icons/UserPlusIcon.vue'
import SparklesIcon from '@/icons/SparklesIcon.vue'
import ShareIcon from '@/icons/ShareIcon.vue'
import ThreeDotsIcon from '@/icons/ThreeDotsIcon.vue'
import MiniChevronDownIcon from '@/icons/MiniChevronDownIcon.vue'
import PhotoIcon from '@/icons/PhotoIcon.vue'
import FaceSmileIcon from '@/icons/FaceSmileIcon.vue'
import ArrowUpTrayIcon from '@/icons/ArrowUpTrayIcon.vue'
import PencilSquareIcon from '@/icons/PencilSquareIcon.vue'

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
  | 'photo'
  | 'arrow-up-tray'
  | 'face-smile'
  | 'pencil-square'
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
  <ArrowLeftEndOnRectangleIcon
    v-else-if="icon == 'arrow-left-end-on-rectangle'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ArrowLeftStartOnRectangleIcon
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
  <Cog6ToothIcon
    v-else-if="icon == 'cog-6-tooth'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ChevronLeftIcon
    v-else-if="icon == 'chevron-left'"
    v-bind="$attrs"
    :strokeWidth="strokeWidth"
    :size="size"
  />
  <ArrowUpIcon
    v-else-if="icon == 'arrow-up'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <ArrowDownIcon
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
  <MiniChevronDownIcon
    v-else-if="icon == 'mini-down'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <PhotoIcon v-else-if="icon == 'photo'" v-bind="$attrs" :size="size" :strokeWidth="strokeWidth" />
  <ArrowUpTrayIcon
    v-else-if="icon == 'arrow-up-tray'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <FaceSmileIcon
    v-else-if="icon == 'face-smile'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
  <PencilSquareIcon
    v-else-if="icon == 'pencil-square'"
    v-bind="$attrs"
    :size="size"
    :strokeWidth="strokeWidth"
  />
</template>
