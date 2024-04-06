<script setup lang="ts">
import InputIcon from 'primevue/inputicon'
import IconField from 'primevue/iconfield'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import BaseIcon from '@/icons/BaseIcon.vue'
import { computed, ref } from 'vue'
import Button from 'primevue/button'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const username = ref<string>(authStore.user?.username ?? '')

const usernameTaken = ref<boolean>(false)

const usernameChanged = ref<boolean>(false)

const usernameError = computed(() => usernameTaken.value)

const updateUsernameEnabled = computed<boolean>(() => {
  return username.value != '' && username.value != authStore.user?.username
})

const updateUsername = function () {
  usernameChanged.value = false
  authStore
    .updateEmail({ username: username.value })
    .then(() => {
      usernameChanged.value = true
    })
    .catch((error) => {
      // TODO: Handle username already taken error
    })
}
</script>

<template>
  <div class="flex w-full flex-col gap-8">
    <h1 class="text-2xl tracking-widest text-primary">{{ $t('profile') }}</h1>
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
  </div>
</template>

<style scoped></style>
