<script setup lang="ts">
import BaseIcon, { type IconType } from '@/icons/BaseIcon.vue'
import { type RouteLocationRaw, useRoute } from 'vue-router'

export interface SideMenuOption {
  labelKey: string
  icon: IconType
  to: RouteLocationRaw
}

const route = useRoute()

withDefaults(
  defineProps<{
    actions?: SideMenuOption[]
  }>(),
  {
    actions: () => []
  }
)

const isTargetRoute = function (targetRoute: RouteLocationRaw) {
  if (typeof targetRoute == 'string') {
    return targetRoute === route.path
  } else if (typeof targetRoute === 'object') {
    if ('name' in targetRoute && targetRoute.name) {
      return targetRoute.name === route.name
    } else {
      return targetRoute.path === route.path
    }
  }
  return false
}
</script>

<template>
  <nav>
    <ul>
      <li v-for="action in actions" :key="action.labelKey">
        <div
          :class="[
            'rounded-lg',
            'px-4',
            'py-2',
            isTargetRoute(action.to)
              ? 'bg-secondary text-white'
              : 'bg-white text-medium-emphasis hover:bg-selection-indicator hover:bg-opacity-5'
          ]"
        >
          <router-link :to="action.to" class="flex gap-4 outline-none">
            <BaseIcon :icon="action.icon" :strokeWidth="1.5" />
            <span class="pr-2">{{ $t(action.labelKey) }}</span>
          </router-link>
        </div>
      </li>
    </ul>
  </nav>
</template>
