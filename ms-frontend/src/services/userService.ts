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
