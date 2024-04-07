import apiClient from '@/services/axios'
import { User } from '@/types/User'
import type { UserUpdate } from '@/types/UserUpdate'
import type { DietaryCriteria } from '@/types/DietaryCriteria'

export const userService = {
  async getUser(userId: string) {
    const response = await apiClient.get(`users/${userId}`)
    return new User(response.data)
  },

  async updateUser(userId: string, update: UserUpdate) {
    const response = await apiClient.patch(`users`, update)
    return new User(response.data)
  },

  async updateProfilePicture(file: File) {
    const formData = new FormData()
    formData.append('image', file)
    const response = await apiClient.patch('users/image', formData)
    return new User(response.data)
  },

  async getDietaryCriteria() {
    const response = await apiClient.get('/users/dietary_criteria/');
    return response.data as DietaryCriteria;
  }
}
