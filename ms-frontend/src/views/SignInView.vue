<script setup lang="ts">
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import FloatLabel from 'primevue/floatlabel'
import IconField from 'primevue/iconfield'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import { computed, ref } from 'vue'
import BaseIcon from '@/icons/BaseIcon.vue'
import DecoStrip from '@/components/DecoStrip.vue'
import { useAuthStore } from '@/stores/auth'
import { emailValidator } from '@/utils/validateEmail'

const authStore = useAuthStore()

const email = ref<string>('')
const username = ref<string>('')
const password = ref<string>('')
const confirmPassword = ref<string>('')

const acceptTermsAndConditions = ref<boolean>(false)

const showPassword = ref<boolean>(false)

const emailInvalid = ref<boolean>(false)
const emailTaken = ref<boolean>(false)
const usernameTaken = ref<boolean>(false)
const confirmPasswordMismatch = ref<boolean>(false)

const emailError = computed(() => emailInvalid.value || emailTaken.value)
const usernameError = computed(() => usernameTaken.value)
const confirmPasswordError = computed(() => confirmPasswordMismatch.value)

const topNavActions: MenuOption[] = [
    {
        labelKey: 'sign_up',
        to: '/sign-up'
    }
]

const toggleShowPassword = function (): void {
    showPassword.value = !showPassword.value
}

const signUpEnabled = computed<boolean>(() => {
    return (
        email.value !== '' &&
        username.value !== '' &&
        password.value !== '' &&
        confirmPassword.value != '' &&
        acceptTermsAndConditions.value &&
        !confirmPasswordMismatch.value &&
        !emailInvalid.value
    )
})

const validateEmail = function (): boolean {
    let result = emailValidator.validate(email.value)
    emailInvalid.value = !result
    return result
}

const validatePassword = function () {
    validateConfirmPassword()
}

const validateConfirmPassword = function () {
    confirmPasswordMismatch.value = password.value != confirmPassword.value
}

const signUp = function () {
    emailTaken.value = false
    usernameTaken.value = false
    authStore.signUp(email.value, username.value, password.value).catch((error) => {
        if (error.response?.status === 409) {
            if (error.response?.data?.detail == 'Username already exists') {
                usernameTaken.value = true
            } else if (error.response?.data?.detail == 'Email already in use') {
                emailTaken.value = true
            }
        }
    })
}
</script>

<template>
    <header class="sticky top-0 z-40">
        <Navbar :actions="topNavActions" iconPos="right" />
    </header>
    <main class="md:pl-16">
        <div class="mx-4 flex h-full items-center justify-center pt-8 md:justify-start">
            <div class="flex flex-col gap-8">
                <h1
                    class="text-center text-2xl font-light uppercase tracking-widest text-secondary md:text-start md:text-5xl">
                    {{ $t('sign_in') }}
                </h1>

                <div class="flex w-fit flex-col gap-8">

                    <div class="relative">
                        <FloatLabel>
                            <IconField iconPosition="right">
                                <InputText id="profile-name" type="text" v-model="username" :invalid="usernameError" />
                                <InputIcon>
                                    <BaseIcon v-show="usernameError" icon="exclamation-circle" />
                                </InputIcon>
                            </IconField>
                            <label for="profile-name">{{ $t('username') }}</label>
                        </FloatLabel>
                        <small v-if="usernameTaken" class="absolute -bottom-4 pl-4 text-xs text-error">
                            {{ $t('username_taken_error') }}
                        </small>
                    </div>

                    <div class="relative">
                        <FloatLabel>
                            <IconField iconPosition="right">
                                <InputText id="password" :type="showPassword ? 'text' : 'password'" v-model="password"
                                    @blur="validatePassword" />
                                <InputIcon
                                    class="cursor-pointer rounded outline-none ring-primary ring-offset-1 focus-visible:ring-1"
                                    @click="toggleShowPassword" @keyup.space="toggleShowPassword">
                                    <BaseIcon :icon="showPassword ? 'eye' : 'eye-slash'" />
                                </InputIcon>
                            </IconField>
                            <label for="password">{{ $t('password') }}</label>
                        </FloatLabel>
                    </div>

                    <div class="flex items-center">
                        <router-link class="outlined-none" to="/sign-in" tabindex="-1">
                            <Button class="mx-2" :label="$t('forgot_password')" link rounded />
                        </router-link>
                    </div>

                    <div class="w-full md:w-fit">
                        <Button class="w-full" :label="$t('sign_in')" rounded :disabled="!signUpEnabled"
                            @click="signUp" />
                    </div>
                </div>

                <div class="flex items-center">
                    <span class="text-medium-emphasis">{{ $t('no_account_yet') }}</span>
                    <router-link class="outlined-none" to="/sign-in" tabindex="-1">
                        <Button class="mx-2" :label="$t('sign_up_here')" link rounded />
                    </router-link>
                </div>
            </div>
        </div>
    </main>
    <DecoStrip class="fixed bottom-0 right-1/4 top-0 z-50 max-lg:invisible lg:visible" />
</template>

<style scoped>
main {
    height: calc(100vh - 48px);
}
</style>
