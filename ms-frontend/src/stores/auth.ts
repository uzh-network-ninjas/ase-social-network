import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const signUp = function (email: string, username: string, password: string) {
    console.log(`[sign up] email: ${email}, username: ${username}, password: ${password}`)
  }

  return { signUp }
})
