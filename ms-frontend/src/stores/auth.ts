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
  if (storedUserData) {
    const parsedUserData = JSON.parse(storedUserData)
    user.value = new User(parsedUserData)
  }

  const signUp = async function (email: string, username: string, password: string) {
    return authService.signUp(email, username, password).then(() => {
      return signIn(username, password)
    })
  }

  const signIn = async function (username: string, password: string) {
    return authService.signIn(username, password).then(async (response: string) => {
      token.value = response
      const decodedToken = jwtDecode(response)
      if (typeof decodedToken.sub !== 'string') {
        throw new Error('JWT does not contain user Id.')
      }
      return await userService.getUser(decodedToken.sub).then((response: User) => {
        user.value = response
        localStorage.setItem('user', JSON.stringify(user.value))
        router.push({ name: 'home' })
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
    return userService.updateUser(user.value.id, update).then((response) => {
      user.value = response
      localStorage.setItem('user', JSON.stringify(user.value))
    })
  }

  return { user, signUp, signIn, signOut, updatePassword, updateUser, signedIn, token }
})
