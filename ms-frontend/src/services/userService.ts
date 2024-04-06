import apiClient from '@/services/axios'
import { User } from '@/types/User'
import type { UserUpdate } from '@/types/UserUpdate'

export const userService = {
  async getUser(userId: string) {
    const response = await apiClient.get(`users/${userId}`)
    return new User(response.data)
  },

  async updateUser(userId: string, update: UserUpdate) {
    const response = await apiClient.patch(`users`, update)
    return new User(response.data)
  }
}
