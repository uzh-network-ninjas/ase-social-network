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
    <ul class="flex flex-col gap-2">
      <li v-for="action in actions" :key="action.labelKey">
        <router-link :to="action.to" class="group outline-none">
          <div
            v-ripple="{
              pt: {
                root: { style: 'transform: scale(0); background: #fff;' }
              }
            }"
            :class="[
              'flex gap-4 rounded-lg px-4 py-2 ring-offset-1 group-focus-visible:ring-1',
              isTargetRoute(action.to)
                ? 'bg-secondary text-white ring-secondary'
                : 'bg-white text-medium-emphasis ring-medium-emphasis hover:bg-selection-indicator hover:bg-opacity-5 '
            ]"
          >
            <BaseIcon :icon="action.icon" :strokeWidth="1" class="min-h-6 min-w-6" />
            <span class="text-nowrap pr-2 font-light">{{ $t(action.labelKey) }}</span>
          </div>
        </router-link>
      </li>
    </ul>
  </nav>
</template>
