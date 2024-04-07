<script setup lang="ts">
import Button from 'primevue/button'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import BaseIcon from '@/icons/BaseIcon.vue'
import Menu from 'primevue/menu'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const menu = ref()
const items = ref<MenuOption[]>([
  {
    labelKey: 'profile',
    icon: 'user',
    to: { name: 'profile', params: { userId: authStore.user?.id } }
  },
  {
    labelKey: 'settings',
    icon: 'cog-6-tooth',
    to: { name: 'settings' }
  }
])

const toggleNavbarMenu = (event: Event) => {
  menu.value.toggle(event)
}
</script>

<template>
  <Navbar>
    <template #end>
      <Button
        outlined
        rounded
        class="!rounded-full"
        @click="toggleNavbarMenu"
        aria-haspopup="true"
        aria-controls="overlay_menu"
      >
        <template #icon>
          <BaseIcon icon="user" :size="5" />
        </template>
      </Button>
      <Menu ref="menu" id="overlay_menu" :model="items" :popup="true">
        <template #start>
          <div
            class="border-medium-emphasis\15 mb-2 gap-4 border-b px-4 py-2 text-center text-lg tracking-wider text-secondary"
          >
            {{ authStore.user?.username }}
          </div>
        </template>
        <template #item="{ item }">
          <router-link class="flex items-center gap-4" :to="item.to">
            <BaseIcon :icon="item.icon" />
            <span>{{ $t(item.labelKey) }}</span>
          </router-link>
        </template>
        <template #end>
          <div
            class="cursor-pointer rounded-lg text-medium-emphasis hover:bg-selection-indicator hover:bg-opacity-5"
            @click="() => authStore.signOut()"
          >
            <div class="relative flex items-center gap-4 px-4 py-2">
              <BaseIcon icon="arrow-left-start-on-rectangle" />
              <span>{{ $t('sign_out') }}</span>
            </div>
          </div>
        </template>
      </Menu>
    </template>
  </Navbar>
</template>
