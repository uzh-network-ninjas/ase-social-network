import apiClient from '@/services/axios'
import { User } from '@/types/User'

export const userService = {
  async getUser(userId: string) {
    const response = await apiClient.get(`users/${userId}`)
    return new User(response.data)
  }
}
