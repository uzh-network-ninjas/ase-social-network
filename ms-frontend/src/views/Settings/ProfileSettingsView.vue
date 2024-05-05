<script setup lang="ts">
import InputIcon from 'primevue/inputicon'
import IconField from 'primevue/iconfield'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import BaseIcon from '@/icons/BaseIcon.vue'
import { computed, ref } from 'vue'
import Button from 'primevue/button'
import { useAuthStore } from '@/stores/auth'
import FileUpload from '@/components/FileUpload.vue'
import LanguageSelection from '@/components/LanguageSelection.vue'

const authStore = useAuthStore()

const username = ref<string>(authStore.user?.username ?? '')
const profilePicture = ref<File | null>(null)

const usernameTaken = ref<boolean>(false)

const usernameChanged = ref<boolean>(false)
const profilePictureChanged = ref<boolean>(false)

const profilePictureChangeFailed = ref<boolean>(false)

const usernameError = computed(() => usernameTaken.value)

const updateUsernameEnabled = computed<boolean>(() => {
  return username.value != '' && username.value != authStore.user?.username
})

const updateProfilePictureEnabled = computed<boolean>(() => {
  return profilePicture.value !== null
})

const updateProfilePicture = function () {
  if (profilePicture.value === null) return
  profilePictureChanged.value = false
  authStore
    .updateProfilePicture(profilePicture.value)
    .then(() => {
      profilePictureChanged.value = true
    })
    .catch(() => {
      profilePictureChangeFailed.value = true
    })
}

const updateUsername = function () {
  usernameChanged.value = false
  usernameTaken.value = false
  authStore
    .updateUser({ username: username.value })
    .then(() => {
      usernameChanged.value = true
    })
    .catch((error) => {
      if (error.response?.status === 400) {
        usernameTaken.value = true
      }
    })
}
</script>

<template>
  <div class="flex w-full flex-col gap-8">
    <h1 class="text-2xl uppercase tracking-widest text-primary">{{ $t('profile') }}</h1>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">
          {{ $t('change_profile_picture') }}
        </h2>
      </div>
      <div class="relative">
        <FileUpload v-model="profilePicture" class="max-w-[600px]"> </FileUpload>
      </div>
      <Button
        class="sm:w-fit"
        :label="$t('update')"
        rounded
        :disabled="!updateProfilePictureEnabled"
        @click="updateProfilePicture"
      />
      <span v-if="profilePictureChanged" class="text-light w-full truncate text-secondary">
        {{ $t('profile_picture_change_success') }}
      </span>
      <span v-if="profilePictureChangeFailed" class="text-light w-full truncate text-error">
        {{ $t('profile_picture_change_fail') }}
      </span>
    </div>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">{{ $t('change_username') }}</h2>
      </div>
      <div class="relative">
        <FloatLabel class="sm:w-fit">
          <IconField iconPosition="right">
            <InputText id="username" type="text" v-model="username" :invalid="usernameError" />
            <InputIcon>
              <BaseIcon v-show="usernameError" icon="exclamation-circle" />
            </InputIcon>
          </IconField>
          <label for="username">{{ $t('username') }}</label>
        </FloatLabel>
        <small
          v-if="usernameTaken"
          class="absolute -bottom-4 left-0 right-0 truncate pl-4 text-xs text-error"
        >
          {{ $t('username_taken_error') }}
        </small>
      </div>
      <Button
        class="sm:w-fit"
        :label="$t('update')"
        rounded
        :disabled="!updateUsernameEnabled"
        @click="updateUsername"
      />
      <span v-if="usernameChanged" class="text-light w-full truncate text-secondary">
        {{ $t('username_change_success') }}
      </span>
    </div>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">{{ $t('language') }}</h2>
      </div>
      <FloatLabel class="sm:w-fit">
        <LanguageSelection id="language-selection" showFlag />
        <label for="language-selection">{{ $t('language') }}</label>
      </FloatLabel>
    </div>
  </div>
</template>
