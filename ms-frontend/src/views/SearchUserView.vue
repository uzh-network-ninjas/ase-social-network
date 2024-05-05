<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import PageHeader from '@/components/PageHeader.vue'
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import FloatLabel from 'primevue/floatlabel'
import IconField from 'primevue/iconfield'
import { ref, watch } from 'vue'
import BaseIcon from '@/icons/BaseIcon.vue'
import type { User } from '@/types/User'
import { userService } from '@/services/userService'

const searchTerm = ref<string>('')
const searchResults = ref<User[]>([])
const noUserFound = ref<boolean>(false)

const searchTermTimeout = ref<ReturnType<typeof setTimeout>>()

watch(searchTerm, () => {
  if (searchTermTimeout.value) {
    clearTimeout(searchTermTimeout.value)
  }
  searchTermTimeout.value = setTimeout(searchUser, 300)
})

const searchUser = async function () {
  if (!searchTerm.value) {
    searchResults.value = []
    noUserFound.value = false
    return
  }
  noUserFound.value = false
  await userService
    .findUser(searchTerm.value)
    .then((user: User) => {
      searchResults.value = [user]
      noUserFound.value = false
    })
    .catch((error) => {
      if (error.response.status === 404) {
        searchResults.value = []
        noUserFound.value = true
      }
    })
}

const clearSearchTerm = function () {
  searchTerm.value = ''
  searchResults.value = []
  noUserFound.value = false
}
</script>

<template>
  <header class="sticky top-0 z-20">
    <SignedInTopNav />
    <PageHeader :label="$t('search_user')" />
    <div class="w-full px-4">
      <FloatLabel class="mt-4">
        <IconField iconPosition="right">
          <InputText id="search_user_field" v-model="searchTerm"></InputText>
          <InputIcon>
            <BaseIcon
              v-if="searchTerm"
              icon="x-mark"
              :size="5"
              :stroke-width="1"
              class="cursor-pointer rounded-full outline-none ring-offset-1 hover:text-primary focus-visible:text-primary focus-visible:ring-1 focus-visible:ring-primary"
              @click="clearSearchTerm"
              @keyup.space="clearSearchTerm"
              tabindex="0"
            />
            <BaseIcon v-else icon="magnifying-glass" :size="5" />
          </InputIcon>
        </IconField>
        <label for="search_user_field">{{ $t('search_user') }}</label>
      </FloatLabel>
    </div>
    <div class="mx-4 mt-2 border-b border-b-medium-emphasis px-4 py-2">
      <span class="text-sm font-light text-medium-emphasis">{{
        `${$t('user')} - ${searchResults.length}`
      }}</span>
    </div>
  </header>
  <main class="my-4">
    <div class="mx-4 flex flex-col divide-y">
      <div
        v-if="searchResults.length == 0 && noUserFound"
        class="w-full text-center font-light text-medium-emphasis"
      >
        {{ $t('no_user_found') }}
      </div>
      <router-link
        v-for="user in searchResults"
        :key="user.id"
        :to="{ name: 'profile', params: { userId: user.id } }"
        class="group my-2 cursor-pointer rounded-lg hover:bg-selection-indicator hover:bg-opacity-5 focus-visible:bg-selection-indicator focus-visible:bg-opacity-5"
      >
        <div class="flex items-center gap-4 px-2 py-2">
          <div
            class="relative flex h-[40px] w-[40px] items-center justify-center overflow-hidden rounded-full"
          >
            <div class="absolute left-0 right-0 h-4 rotate-45 bg-primary"></div>
            <div class="z-10 h-[38px] w-[38px] overflow-hidden rounded-full bg-background">
              <div
                class="flex h-full w-full items-center justify-center group-hover:bg-selection-indicator group-hover:bg-opacity-5"
              >
                <div
                  v-if="user.image"
                  class="flex h-[34px] w-[34px] items-center justify-center overflow-hidden rounded-full"
                >
                  <img
                    :src="user.image"
                    class="h-[34px] w-[34px] rounded-full object-cover"
                    alt="of user"
                  />
                </div>
                <div
                  v-else
                  class="flex h-[34px] w-[34px] items-center justify-center rounded-full border border-medium-emphasis"
                >
                  <BaseIcon
                    icon="user"
                    :size="5"
                    :stroke-width="1.5"
                    class="text-medium-emphasis"
                  />
                </div>
              </div>
            </div>
          </div>
          <div>
            <span class="text-lg font-light text-medium-emphasis">{{ user.username }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </main>
</template>
