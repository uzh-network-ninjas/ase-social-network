<script setup lang="ts">
import BaseIcon, { type IconType } from '@/icons/BaseIcon.vue'
import Button from 'primevue/button'
import router from '@/router'
import type { RouteLocationRaw } from 'vue-router'

export interface MenuOption {
  labelKey: string
  icon?: IconType
  iconPos?: 'left' | 'right' | 'top' | 'bottom'
  before?: () => void
  to: RouteLocationRaw
}

withDefaults(
  defineProps<{
    actions?: MenuOption[]
    iconPos?: 'left' | 'right' | 'top' | 'bottom'
  }>(),
  {
    actions: () => [],
    iconPos: 'left'
  }
)
</script>

<template>
  <nav class="bg-background">
    <ul class="flex gap-4 px-4 py-2">
      <li class="grow">
        <router-link
          class="flex w-fit items-center gap-2 rounded-lg text-primary outline-none ring-primary ring-offset-1 focus-visible:ring-1"
          to="/"
        >
          <BaseIcon icon="sparkles" :stroke-width="1.5" class="h-8 w-8" />
          <span class="text-xl font-medium uppercase tracking-widest">Review App</span>
        </router-link>
      </li>
      <li
        v-for="action in actions"
        :key="`${action.labelKey}:${action.to}`"
        class="flex items-center gap-2 text-primary"
      >
        <Button
          text
          rounded
          :label="$t(action.labelKey)"
          :iconPos="action.iconPos ?? iconPos"
          @click="
            () => {
              action.before?.()
              router.push(action.to)
            }
          "
        >
          <template #icon>
            <BaseIcon :icon="action.icon" />
          </template>
        </Button>
      </li>
    </ul>
  </nav>
</template>
