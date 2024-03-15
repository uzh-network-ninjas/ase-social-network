import apiClient from '@/services/axios'
import { User } from '@/types/User'

export const authService = {
  async signUp(email: string, username: string, password: string): Promise<User> {
    const response = await apiClient.post('/authenticator/user', {
      username: username,
      email: email,
      password: password
    })
    return new User(response.data)
  }
}
