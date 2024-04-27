import apiClient from '@/services/axios'
import { Review } from '@/types/Review'

export const reviewService = {
  async getReview(reviewId: string) {
    const response = await apiClient.get(`reviews/${reviewId}`)
    return new Review(response.data)
  },

  async createReview(text: string, rating: number, location: { id: string, name: string, coordinates: { x: string, y: string } }) {
    const response = await apiClient.post('reviews', { text, rating, location })
    return new Review(response.data)
  },

  async updateReviewImage(reviewId: string, image: File) {
    const formData = new FormData()
    formData.append('review_id', reviewId)
    formData.append('image', image)

    const response = await apiClient.patch('reviews/image', formData)
    return new Review(response.data)
  },

  async getReviewsOfUser(userId: string): Promise<Review[]> {
    const response = await apiClient.get(`/reviews/users/?user_id=${userId}`)
    return response.data
  }
  
}
