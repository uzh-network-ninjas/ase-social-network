import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authService } from '@/services/authService'
import { User } from '@/types/User'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User>()

  const storedUserData = localStorage.getItem('user')
  if (storedUserData) {
    const parsedUserData = JSON.parse(storedUserData)
    user.value = new User(parsedUserData)
  }

  const signUp = async function (email: string, username: string, password: string) {
    return authService.signUp(email, username, password).then((response: User) => {
      user.value = response
      localStorage.setItem('user', JSON.stringify(user.value))
      router.push({ name: 'home' })
    })
  }

  return { user, signUp }
})
