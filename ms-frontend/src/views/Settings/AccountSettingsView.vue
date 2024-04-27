<script setup lang="ts">
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import BaseIcon from '@/icons/BaseIcon.vue'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import { computed, ref } from 'vue'
import { emailValidator } from '@/utils/validateEmail'
import Button from 'primevue/button'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const email = ref<string>(authStore.user?.email ?? '')
const currentPassword = ref<string>('')
const newPassword = ref<string>('')
const confirmNewPassword = ref<string>('')

const emailInvalid = ref<boolean>(false)
const emailTaken = ref<boolean>(false)

const confirmNewPasswordMismatch = ref<boolean>(false)
const currentPasswordWrong = ref<boolean>(false)
const newPasswordIdentical = ref<boolean>(false)

const showNewPassword = ref<boolean>(false)
const showCurrentPassword = ref<boolean>(false)

const emailChanged = ref<boolean>(false)
const passwordChanged = ref<boolean>(false)

const validateEmail = function (): boolean {
  let result = emailValidator.validate(email.value)
  emailInvalid.value = !result
  return result
}

const emailError = computed(() => emailInvalid.value || emailTaken.value)
const confirmNewPasswordError = computed(() => confirmNewPasswordMismatch.value)
const currentPasswordError = computed(() => currentPasswordWrong.value)
const newPasswordError = computed(() => newPasswordIdentical.value)

const validateCurrentPassword = function () {
  newPasswordIdentical.value =
    currentPassword.value === newPassword.value &&
    currentPassword.value !== '' &&
    newPassword.value !== ''
}

const validateNewPassword = function () {
  validateConfirmNewPassword()
  validateCurrentPassword()
}

const validateConfirmNewPassword = function () {
  confirmNewPasswordMismatch.value = newPassword.value != confirmNewPassword.value
}

const toggleShowNewPassword = function (): void {
  showNewPassword.value = !showNewPassword.value
}

const toggleShowCurrentPassword = function (): void {
  showCurrentPassword.value = !showCurrentPassword.value
}

const updateEmail = function () {
  emailChanged.value = false
  authStore
    .updateUser({ email: email.value })
    .then(() => {
      emailChanged.value = true
    })
    .catch((error) => {
      if (error.response?.status === 400) {
        emailTaken.value = true
      }
    })
}

const updatePassword = function () {
  currentPasswordWrong.value = false
  passwordChanged.value = false
  authStore
    .updatePassword(currentPassword.value, newPassword.value)
    .then(() => {
      passwordChanged.value = true
      currentPassword.value = ''
      newPassword.value = ''
      confirmNewPassword.value = ''
    })
    .catch((error) => {
      if (error.response?.status === 401) {
        currentPasswordWrong.value = true
      } else if (error.response?.status === 400) {
        newPasswordIdentical.value = true
      }
    })
}

const updatePasswordEnabled = computed<boolean>(() => {
  return (
    !confirmNewPasswordMismatch.value &&
    !newPasswordIdentical.value &&
    newPassword.value !== '' &&
    confirmNewPassword.value !== '' &&
    currentPassword.value !== ''
  )
})

const updateEmailEnabled = computed<boolean>(() => {
  return !emailInvalid.value && email.value !== '' && email.value !== authStore.user?.email
})
</script>

<template>
  <div class="flex w-full flex-col gap-8">
    <h1 class="text-2xl uppercase tracking-widest text-primary">{{ $t('account') }}</h1>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">{{ $t('change_email') }}</h2>
      </div>
      <div class="relative">
        <FloatLabel class="sm:w-fit">
          <IconField iconPosition="right">
            <InputText
              id="email"
              type="email"
              v-model="email"
              :invalid="emailError"
              @blur="validateEmail"
            />
            <InputIcon>
              <BaseIcon v-show="emailError" icon="exclamation-circle" />
            </InputIcon>
          </IconField>
          <label for="email">{{ $t('email') }}</label>
        </FloatLabel>
        <small
          v-if="emailInvalid"
          class="absolute -bottom-4 left-0 right-0 truncate pl-4 text-xs text-error"
          >{{ $t('valid_email_error') }}</small
        >
        <small
          v-else-if="emailTaken"
          class="absolute -bottom-4 left-0 right-0 truncate pl-4 text-xs text-error"
          >{{ $t('email_taken_error') }}</small
        >
      </div>
      <Button
        class="sm:w-fit"
        :label="$t('update')"
        rounded
        :disabled="!updateEmailEnabled"
        @click="updateEmail"
      />
      <span v-if="emailChanged" class="text-light w-full truncate text-secondary">
        {{ $t('email_change_success') }}
      </span>
    </div>
    <div class="flex flex-col gap-8">
      <div class="w-full border-b border-b-medium-emphasis">
        <h2 class="mb-2 text-xl font-light text-medium-emphasis">{{ $t('change_password') }}</h2>
      </div>
      <div class="relative">
        <FloatLabel class="sm:w-fit">
          <IconField iconPosition="right">
            <InputText
              id="password"
              :type="showCurrentPassword ? 'text' : 'password'"
              v-model="currentPassword"
              :invalid="currentPasswordError"
              @blur="validateCurrentPassword"
            />
            <InputIcon
              class="cursor-pointer rounded outline-none ring-primary ring-offset-1 focus-visible:ring-1"
              @click="toggleShowCurrentPassword"
              @keyup.space="toggleShowCurrentPassword"
            >
              <BaseIcon :icon="showCurrentPassword ? 'eye' : 'eye-slash'" />
            </InputIcon>
          </IconField>
          <label for="password">{{ $t('current_password') }}</label>
        </FloatLabel>
        <small
          v-if="currentPasswordWrong"
          class="absolute -bottom-4 left-0 right-0 truncate pl-4 text-xs text-error"
        >
          {{ $t('current_password_wrong') }}
        </small>
      </div>

      <div class="relative">
        <FloatLabel class="sm:w-fit">
          <IconField iconPosition="right">
            <InputText
              id="password"
              :type="showNewPassword ? 'text' : 'password'"
              v-model="newPassword"
              :invalid="newPasswordError"
              @blur="validateNewPassword"
            />
            <InputIcon
              class="cursor-pointer rounded outline-none ring-primary ring-offset-1 focus-visible:ring-1"
              @click="toggleShowNewPassword"
              @keyup.space="toggleShowNewPassword"
            >
              <BaseIcon :icon="showNewPassword ? 'eye' : 'eye-slash'" />
            </InputIcon>
          </IconField>
          <label for="password">{{ $t('new_password') }}</label>
        </FloatLabel>
        <small
          v-if="newPasswordIdentical"
          class="absolute -bottom-4 left-0 right-0 truncate pl-4 text-xs text-error"
        >
          {{ $t('new_password_identical') }}
        </small>
      </div>

      <div class="relative">
        <FloatLabel class="sm:w-fit">
          <IconField iconPosition="right">
            <InputText
              id="confirm-password"
              :type="showNewPassword ? 'text' : 'password'"
              v-model="confirmNewPassword"
              :invalid="confirmNewPasswordError"
              @blur="validateConfirmNewPassword"
              @input="validateConfirmNewPassword"
            />
            <InputIcon
              class="cursor-pointer rounded outline-none ring-primary ring-offset-1 focus-visible:ring-1"
              @click="toggleShowNewPassword"
              @keyup.space="toggleShowNewPassword"
            >
              <BaseIcon :icon="showNewPassword ? 'eye' : 'eye-slash'" />
            </InputIcon>
          </IconField>
          <label for="confirm-password">{{ $t('confirm_new_password') }}</label>
        </FloatLabel>
        <small
          v-if="confirmNewPasswordMismatch"
          class="absolute -bottom-4 left-0 right-0 truncate pl-4 text-xs text-error"
          >{{ $t('confirm_password_mismatch') }}</small
        >
      </div>
      <Button
        class="sm:w-fit"
        :label="$t('update')"
        rounded
        :disabled="!updatePasswordEnabled"
        @click="updatePassword"
      />
      <span v-if="passwordChanged" class="text-light w-full truncate text-secondary">
        {{ $t('password_change_success') }}
      </span>
    </div>
  </div>
</template>
