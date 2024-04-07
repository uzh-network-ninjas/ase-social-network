import apiClient from '@/services/axios'
import { User } from '@/types/User'
import type { UserUpdate } from '@/types/UserUpdate'
import type { DietaryCriteria } from '@/types/DietaryCriteria'

let updateAbortController: AbortController

export const userService = {
  async getUser(userId: string) {
    const response = await apiClient.get(`users/${userId}`)
    return new User(response.data)
  },

  async updateUser(update: UserUpdate) {
    if (updateAbortController) {
      updateAbortController.abort()
    }
    updateAbortController = new AbortController()
    const response = await apiClient.patch(`users`, update, {
      signal: updateAbortController.signal
    })
    return new User(response.data)
  },

  async updateProfilePicture(file: File) {
    const formData = new FormData()
    formData.append('image', file)
    const response = await apiClient.patch('users/image', formData)
    return new User(response.data)
  },

  async getDietaryCriteria() {
    const response = await apiClient.get('/users/dietary_criteria/')
    return response.data as DietaryCriteria
  },

  async followUser(userId: string): Promise<void> {
    await apiClient.patch(`users/following/${userId}`)
  },

  async unfollowUser(userId: string): Promise<void> {
    await apiClient.delete(`users/following/${userId}`)
  },

  async getUserFollowers(userId: string): Promise<User[]> {
    try {
      const response = await apiClient.get(`/users/${userId}/followers`)
      // Assuming the response contains an object with a 'users' property
      return response.data.users
    } catch (error) {
      console.error('Error fetching user followers:', error)
      return [] // Return an empty array if there's an error
    }
  },

  async getUserFollowing(userId: string): Promise<User[]> {
    try {
      const response = await apiClient.get(`/users/${userId}/following`)
      return response.data // Assuming the response contains an array of User objects
    } catch (error) {
      console.error('Error fetching user followers:', error)
      return [] // Return an empty array if there's an error
    }
  },

  async findUser(username: string) {
    const response = await apiClient.get(`users/?username=${username}`)
    return new User(response.data)
  }
}
