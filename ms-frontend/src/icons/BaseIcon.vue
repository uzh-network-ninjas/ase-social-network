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
import ArrowUpIcon from '@/icons/ArrowUpIcon.vue'
import ProfileIcon from '@/icons/ProfileIcon.vue'

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
  | 'profile'
  | undefined

withDefaults(
  defineProps<{
    icon: IconType
    strokeWidth?: number
    imageUrl?: string
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
  <UserPlusIcon v-else-if="icon == 'user-plus'" v-bind="$attrs" />
  <ShareIcon v-else-if="icon == 'share'" v-bind="$attrs" />
  <BackIcon v-else-if="icon == 'back'" v-bind="$attrs" />
  <ThreeDotsIcon v-else-if="icon == 'three-dots'" v-bind="$attrs" />
  <MiniChevronDown v-else-if="icon == 'mini-down'" v-bind="$attrs" />
  <ArrowUpIcon v-else-if="icon == 'arrow-up'" v-bind="$attrs" />
  <ProfileIcon v-else-if="icon === 'profile' && imageUrl" v-bind="$attrs" :imageUrl="imageUrl" />
  <!-- Conditionally render ProfileIcon with imageUrl -->
</template>
