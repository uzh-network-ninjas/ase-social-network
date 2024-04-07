import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { authService } from '@/services/authService'
import { User } from '@/types/User'
import router from '@/router'
import { jwtDecode } from 'jwt-decode'
import { userService } from '@/services/userService'
import type { UserUpdate } from '@/types/UserUpdate'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User>()
  const token = ref<string>()

  const signedIn = computed<boolean>(() => {
    return token.value !== undefined
  })

  const storedUserData = localStorage.getItem('user')
  const storedToken = sessionStorage.getItem('token')
  if (storedUserData && storedToken) {
    const parsedUserData = JSON.parse(storedUserData)
    const parsedToken = JSON.parse(storedToken)
    user.value = new User(parsedUserData)
    token.value = parsedToken
  }

  const signUp = async function (email: string, username: string, password: string) {
    return authService.signUp(email, username, password).then(() => {
      return signIn(username, password)
    })
  }

  const signIn = async function (username: string, password: string) {
    return authService.signIn(username, password).then(async (response: string) => {
      token.value = response
      // Fixme: JWT Token should not be stored in storage, change if refresh token gets implemented
      sessionStorage.setItem('token', JSON.stringify(response))
      const decodedToken = jwtDecode(response)
      if (typeof decodedToken.sub !== 'string') {
        throw new Error('JWT does not contain user Id.')
      }
      return await userService.getUser(decodedToken.sub).then((response: User) => {
        user.value = response
        localStorage.setItem('user', JSON.stringify(user.value))
        if (user.value?.preferences.length >= 5) {
          router.push({ name: 'home' })
        } else {
          router.push({ name: 'onboarding' })
        }
      })
    })
  }

  const signOut = async function () {
    user.value = undefined
    token.value = undefined
    localStorage.removeItem('user')
    await router.push({ name: 'sign-in' })
  }

  const updatePassword = async function (currentPassword: string, newPassword: string) {
    return authService.updatePassword(currentPassword, newPassword)
  }

  const updateUser = async function (update: UserUpdate) {
    if (!user.value) return Promise.reject(new Error('User is not set.'))
    return userService.updateUser(update).then((response) => {
      user.value = response
      localStorage.setItem('user', JSON.stringify(user.value))
    })
  }

  const updateProfilePicture = async function (file: File) {
    if (!user.value) return Promise.reject(new Error('User is not set.'))
    return userService.updateProfilePicture(file).then((response) => {
      user.value = response
      localStorage.setItem('user', JSON.stringify(user.value))
    })
  }

  return {
    user,
    signUp,
    signIn,
    signOut,
    updatePassword,
    updateUser,
    updateProfilePicture,
    signedIn,
    token
  }
})
